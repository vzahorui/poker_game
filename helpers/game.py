from typing import Optional
import random
from collections import deque

from helpers.cards import Deck
from helpers.player import Player
from helpers.config import ROUND_STAGES


class Game:
    """The whole game container class.

    Attributes
    ----------
    n_players : int
        number of players in the game
    players : Optional[deque[Player]]
        List of players. Takes precedence over n_players if provided.
        If not provided then generated based on n_players
    """

    def __init__(self, n_players=3, players=None, limits=None,
                 small_blind=1, big_blind=2, antes=None):
        self.big_blind = big_blind
        self.antes = antes
        self.small_blind = small_blind
        self.limits = limits
        if players is None:
            assert n_players > 1, 'There should be at least 2 players.'
            self.n_players = n_players
            players = deque([Player('You')] + [Player(f'Player {i}') for i in range(1, n_players)])
        else:
            self.n_players = len(players)
            players = players

        # the current set of players may be different from the initial one because
        # some may lose all their money and be out of the game
        self.initial_players = players.copy()

        # pick the player who will be a dealer at the beginning and rotate the list
        # so that the dealer is also first
        first_dealer_idx = random.choice(range(len(players)))
        players.rotate(-first_dealer_idx)
        self.players = players

    def play_round(self):
        if len(self.players) > 1:
            game_round = Round(players=self.players,
                               small_blind=self.small_blind,
                               big_blind=self.big_blind)
            return game_round
        else:
            print('No more opponents are left.')


class Round:
    """A round is a single game which consists of four stages:
    pre-flop, flop, turn and river.

    Attributes
    ----------
    players : deque[Player]
        The list of players in the round.

    Methods
    -------
    deal_cards(stage)
        Deal cards to the table or to the players.
    """

    def __init__(self, players: deque[Player],
                 small_blind: int = 1,
                 big_blind: int = 2):
        self.deck = Deck()
        self.community_cards = []
        self.players = players
        self.first_player = self.players[0]  # the one from which each post flop stage starts
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.bank = 0
        self.stage_idx = 0
        self.active_players_bets = {}
        self.do_blinds()  # place blinds to the bank

        # the current set of players may be different from the initial one because
        # some may fold
        self.initial_players = self.players.copy()

    def deal_cards(self, stage: str):
        """Deal cards to the table or to the players based on the stage of the game.

        Attributes
        ----------
        stage : str
            Stage of the game. Can have values "pre-flop", "flop", "turn", "river".
        """
        if stage == 'pre-flop':
            for player in self.players:
                player.receive_card(self.deck.deal(num_cards=2))
        elif stage == 'flop':
            self.community_cards.extend(self.deck.deal(num_cards=3))
        elif stage in ("turn", "river"):
            self.community_cards.extend(self.deck.deal(num_cards=1))

    def do_blinds(self):
        """Players with blinds give their blinds, and the queue of players is rotated."""
        self.make_single_bet(self.small_blind)
        self.make_single_bet(self.big_blind)

    def make_single_bet(self, amount):
        """Active player bets by giving a given amount of money to the bank.
        The bet is recorded into active_players_bets dict.
        The turn is passed onto the next player.
        """
        self.bank += self.players[0].do_bet(amount)
        if self.players[0] in self.active_players_bets:
            self.active_players_bets[self.players[0]] += amount
        else:
            self.active_players_bets[self.players[0]] = amount
        self.players.rotate(-1)

    def make_a_turn(self):
        """The player action and the response of the game to it. Return next player to act."""
        current_player = self.players[0]
        player_action = current_player.analyze_and_act(self.community_cards)

        if player_action == -1:  # if folded
            if current_player in self.active_players_bets:
                del self.active_players_bets[current_player]
            if current_player == self.first_player:
                self.first_player = self.players[1]  # next player becomes the first
            self.players.popleft()

        else:  # if made a bet or checked
            self.make_single_bet(amount=player_action)
        return self.players[0]  # will be used to display in the table of players

    def next_event(self):
        """One of the following:
         - an action of a player;
         - dealing of community cards;
         - proclaiming the victor;
         - start a new round of game.
         """
        if not self.active_players_bets:  # this happens at the beginning of flop, turn and river stages
            return self.make_a_turn()

        all_bet_values = list(self.active_players_bets.values())
        if all_bet_values.count(all_bet_values[0]) == len(all_bet_values) == len(self.players):
            # this happens if the stage is over (all players made bets or left, bets are the same)
            if self.stage_idx != 3:
                # go to the next stage
                self.stage_idx += 1
                self.active_players_bets = {}
                current_position_of_first_player = self.players.index(self.first_player)
                self.players.rotate(-current_position_of_first_player)
                return self.stage_idx  # will be used later to change the image of the table
            else:
                # open up
                # TODO: return the combinations of each player remaining in the game and evaluate whether win or not
                pass
        else:  # if it is a middle of a certain stage
            return self.make_a_turn()

    # TODO: provide validation of funds mechanism so that the bets can't go over
    #  the lowest available fund of any player in the game


class Limit:
    """Custom limit rules"""
    # which round should allow the increase of limit, by how much
    # maximum limit
    # probably should relly of small and big blinds
    # rules for the increase of stakes (antes, blinds) after a certain number of games
    pass
