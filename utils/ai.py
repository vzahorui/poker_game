from collections import Counter
from enum import IntEnum
from itertools import combinations

from utils.cards import PlayingCard


class PokerHand(IntEnum):
    """Ranks of different hands."""
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10


CARD_RANKS_TO_INT_ACE_FIRST = {'ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
                               'jack': 11, 'queen': 12, 'king': 13}
CARD_RANKS_TO_INT_ACE_LAST = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
                              'jack': 11, 'queen': 12, 'king': 13, 'ace': 14}
ROYAL_FLUSH_RANKS = [10, 11, 12, 13, 14]
MAX_CARDS_IN_HAND = 5


class Mind:
    """Holder of the logic which players use when performing acts."""

    def __init__(self, cards: list[PlayingCard]):
        self.cards = cards

    @staticmethod
    def _is_straight(cards) -> bool:
        ranks_ace_first = sorted(set(CARD_RANKS_TO_INT_ACE_FIRST[card.rank] for card in cards))
        ranks_ace_last = sorted(set(CARD_RANKS_TO_INT_ACE_LAST[card.rank] for card in cards))
        is_straight = False
        for ranks in [ranks_ace_first, ranks_ace_last]:
            if len(ranks) == MAX_CARDS_IN_HAND and ranks[-1] - ranks[0] == (MAX_CARDS_IN_HAND - 1):
                is_straight = True
        return is_straight

    def evaluate_hand_strength(self) -> PokerHand:
        rank_counts = Counter(CARD_RANKS_TO_INT_ACE_FIRST[card.rank] for card in self.cards)
        max_ranks = max(rank_counts.values())
        if max_ranks == 4:
            return PokerHand.FOUR_OF_A_KIND
        elif max_ranks == 3 and 2 in rank_counts.values():
            return PokerHand.FULL_HOUSE
        elif self.cards >= MAX_CARDS_IN_HAND:
            all_card_combinations = combinations(self.cards, MAX_CARDS_IN_HAND)
            for combination in all_card_combinations:
                if len(set(card.suit for card in combination)) == 1:  # is flush
                    ranks_ace_last = sorted(set(CARD_RANKS_TO_INT_ACE_LAST[card.rank] for card in combination))
                    if ranks_ace_last == ROYAL_FLUSH_RANKS:
                        return PokerHand.ROYAL_FLUSH
                    if self._is_straight(combination):
                        return PokerHand.STRAIGHT_FLUSH
                    else:
                        return PokerHand.FLUSH
                elif self._is_straight(combination):  # no flush but straight
                    return PokerHand.STRAIGHT
        elif max_ranks == 3:
            return PokerHand.THREE_OF_A_KIND
        elif list(rank_counts.values()).count(2) == 2:
            return PokerHand.TWO_PAIR
        elif max_ranks == 2:
            return PokerHand.ONE_PAIR
        else:
            return PokerHand.HIGH_CARD
