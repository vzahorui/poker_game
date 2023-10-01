import random
from dataclasses import dataclass, field


RANKS = '2 3 4 5 6 7 8 9 10 jack queen king ace'.split()
SUITS = 'clubs diamonds hearts spades'.split()


@dataclass(frozen=True)
class PlayingCard:
    rank: str
    suit: str


def make_french_deck():
    """Make a shuffled deck of cards."""
    deck = [PlayingCard(r, s) for s in SUITS for r in RANKS]
    random.shuffle(deck)
    return deck


@dataclass
class Deck:
    """A deck of cards class with some added behavior."""
    cards: list[PlayingCard] = field(default_factory=make_french_deck)

    def deal(self, num_cards=1):
        """Get cards out of the deck."""
        if num_cards <= len(self.cards):
            dealt_cards = self.cards[:num_cards]
            self.cards = self.cards[num_cards:]
            return dealt_cards
        else:
            raise ValueError('There are less cards in the deck than you want to take.')
