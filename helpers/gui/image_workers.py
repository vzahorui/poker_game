import pathlib

from PIL import Image, ImageOps

from helpers.config import BACK_PLAYING_CARD
from helpers.cards import PlayingCard


def draw_table_cards(
        cards: tuple[pathlib.Path] = (BACK_PLAYING_CARD, BACK_PLAYING_CARD, BACK_PLAYING_CARD,
                                      BACK_PLAYING_CARD, BACK_PLAYING_CARD)
):
    """Draw five cards side by side.
    By default, all of them are drawn face-down."""
    first_ind_image = Image.open(cards[0])
    ind_width, ind_height = first_ind_image.size
    # Define the spacing between individual cards
    spacing = round(ind_width * 0.4)
    # Create a new blank image to hold the row of cards
    row_width = (ind_width + spacing) * len(cards) - spacing
    row_height = ind_height*2
    row_image = Image.new('RGB', (row_width, row_height), color='white')
    # Paste the cards into the row image with spacing
    for i in range(len(cards)):
        ind_image = Image.open(cards[i])
        position = (i * (ind_width + spacing), round(row_height*0.25))  # Position to paste the image
        row_image.paste(ind_image, position)
    return row_image.reduce(7)


def draw_your_cards(cards: tuple[PlayingCard]):
    """Draw your two cards side by side."""

    def get_card_image(card: PlayingCard):
        rank, suit = card.rank, card.suit
        path_to_img = pathlib.Path('assets') / 'deck' / f'{suit}_{rank}.jpg'
        ind_image = Image.open(path_to_img)
        img_with_border = ImageOps.expand(ind_image, border=10, fill='#9b908e')  # add a thin line around the image
        return img_with_border

    first_ind_image = get_card_image(cards[0])
    ind_width, ind_height = first_ind_image.size
    spacing = round(ind_width * 0.1)
    # Create a new blank image to hold the row of cards
    row_width = (ind_width + spacing) * len(cards) - spacing
    row_image = Image.new('RGB', (row_width, ind_height), color='white')

    second_ind_image = get_card_image(cards[1])

    for i, img in enumerate([first_ind_image, second_ind_image]):
        position = (i * (ind_width + spacing), 0)
        row_image.paste(img, position)
    return row_image.reduce(9)
