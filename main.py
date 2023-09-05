from collections import deque

import streamlit as st
from PIL import Image
import pandas as pd

from helpers.player import Player
from helpers.game import Game
from helpers import gui
from helpers.config import MAX_PLAYERS


# st.button('click', on_click=gui.display_your_cards())


# fix the sidebar width, center the image, expand the width of the main canvas
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 420px !important; # Set the width to your desired value
        }
        div[data-testid="stImage"] {
            margin: auto 
        }
        .css-1y4p8pa {
            max-width: 76rem
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    with st.form("input_form"):
        st.title('Game options')
        st.header(f'Opponents (up to {MAX_PLAYERS - 1})')
        st.text('Only players with funds greater than\nthe value of the big blind are included.')
        behavior_options = ['Standard', 'Risky', 'Conservative']
        opponents_table_config = {
            'Opponent name': st.column_config.TextColumn('Opponent name'),
            'Behavior': st.column_config.SelectboxColumn('Behavior', options=behavior_options,
                                                         default='Standard', required=True),
            'Funds': st.column_config.NumberColumn('Funds', min_value=0, default=0),
        }

        opponents_table = st.data_editor(
            {'Opponents': [f'Opponent {i}' for i in range(1, MAX_PLAYERS)],
             'Behavior': ['Standard'] * (MAX_PLAYERS - 1),
             'Funds': [0] * (MAX_PLAYERS - 1)},
            num_rows="fixed", column_config=opponents_table_config, key='opponents_table')

        col1, col2 = st.columns(2)
        with col1:
            small_blind_input = st.number_input('Small blind value', min_value=0, value=1, key='small_blind_input')
        with col2:
            big_blind_input = st.number_input('Big blind value', min_value=0, value=2, key='big_blind_input')

        new_game_button = st.form_submit_button("Start a new game", on_click=gui.create_new_game)

#table_image_placeholder = st.empty()

#empty_table_img = Image.open('assets/table.jpg')
#table_image_placeholder.image(empty_table_img, width=900)

if 'hide' not in st.session_state:
    st.session_state.hide = False


def show_hide():
    st.session_state.hide = not st.session_state.hide


st.button('Show/Hide', on_click=show_hide)

if st.session_state.hide:
    secret = st.container()
    with secret:
        st.write('hi')

# print(new_game.community_cards)
# print(new_game.players)
# print('----')
# new_game.deal_cards('pre-flop')
# print(new_game.community_cards)
# print(new_game.players[0].cards)
# print('----')
# new_game.deal_cards('flop')
# print(new_game.community_cards)
# print('----')
# new_game.deal_cards('turn')
# print(new_game.community_cards)
# print('----')
# new_game.deal_cards('river')
# print(new_game.community_cards)
