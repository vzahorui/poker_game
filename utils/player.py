import itertools
from typing import Optional

from utils.ai import PokerHand
from utils.cards import PlayingCard


class Player:
    id_iter = itertools.count() # in order to assign new id to each new class instance

    def __init__(self, name, behavior='Standard', funds=200):
        self.name = name
        self.id = next(self.id_iter)
        self.behavior = behavior
        self.funds = funds
        self.cards = []

    def receive_card(self, cards: list[PlayingCard]):
        """Add a card to a hand."""
        self.cards.extend(cards)

    def evaluate_poker_hand(self, community_cards: list[Optional[PlayingCard]]) -> PokerHand:
        """Determine the current stance in terms of the available cards."""
        all_cards = self.cards + community_cards

    def show_cards(self):
        """Showing cards when finishing game."""
        return ', '.join(map(str, self.cards))

    def do_bet(self, amount: int):
        """Match of increase the current open bet; do blinds."""
        self.funds -= amount
        return amount

    @staticmethod
    def fold():
        """Push cards into the middle of the table and surrender."""
        return -1

    @staticmethod
    def check():
        """Pass the action to the next player. Do not bet."""
        return 0

    def analyze_and_act(self, community_cards):
        # TODO: define some logic here the factors are: community cards, player cards, other players' actions (bets
        #  of the round, how impulsive some of them were)
        action_from_analysis = self.check()
        return action_from_analysis


