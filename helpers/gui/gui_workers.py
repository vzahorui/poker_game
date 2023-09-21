from collections import deque

import streamlit as st
import pandas as pd

from helpers.player import Player
from helpers.game import Game
from helpers.config import ROUND_STAGES
from helpers.gui.image_workers import draw_table_cards, draw_your_cards


def manipulate_css():
    """Fix the sidebar width, center the image, expand the width of the main canvas, and set up custom font size."""
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
            .big-font {
            font-size:30px !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def create_game_layout(new_game=True):
    """This function creates and recreates the whole game layout."""
    if new_game:
        create_new_game()
    if 'game' not in st.session_state:
        return

    # create upper row
    col1_outer, col2_outer = st.columns([3, 1])
    # in upper left corner
    with col1_outer:
        with st.container():
            # create game flow indicators
            col1, col2, col3, col4 = st.columns(4, gap='small')
            game_round_stage = ROUND_STAGES[st.session_state['round'].stage_idx]
            col1.markdown(f"Current stage:<p class='big-font'>**{game_round_stage}**</p>",
                          unsafe_allow_html=True)
            active_player_name = st.session_state['round'].players[0].name
            col2.markdown(f"Active player:<p class='big-font'>**{active_player_name}**</p>",
                          unsafe_allow_html=True)
            st.session_state['round'].determine_next_event()
            action_on_next = st.session_state['round'].next_action
            col3.markdown(f"Action on next:<p class='big-font'>**{action_on_next}**</p>",
                          unsafe_allow_html=True)
            bank_amount = st.session_state['round'].bank
            col4.markdown(f"Bank amount:<p class='big-font'>**{bank_amount}**</p>",
                          unsafe_allow_html=True)

            st.button('Next', key='next_button', on_click=perform_next_action)

            display_table()  # display game table

            # display your cards
            col1_your_cards, col2_your_cards, col3_your_cards = st.columns([1, 3, 2])
            col1_your_cards.header("Your cards:")
            with col2_your_cards:
                display_your_cards()
            if st.session_state['round'].players[0] == st.session_state['you']:
                col3_your_cards.button('Check', on_click=perform_next_action)
                col3_your_cards.button('Fold', on_click=perform_next_action)
                col3_your_cards.button('Bet', on_click=perform_next_action)
                col3_your_cards.number_input('Your bet amount', min_value=0, max_value=st.session_state['you'].funds,
                                             step=1, key='your_bet_amount_input',
                                             on_change=create_game_layout, args=(False,))
    # in upper right corner
    with col2_outer:
        if new_game:
            create_players_table()
        else:
            display_players_table()


def create_new_game():
    """Initialize a new game provided the input information about the opponents
    and about the blinds. Store the game in a Streamlit session state.
    """
    # if no change to the opponents table applied (no opponents)
    if not st.session_state['opponents_table']['edited_rows']:
        st.error('No opponents in the game. Select at least one.', icon="🚨")
        return

    if 'game' in st.session_state:
        del st.session_state['game']

    edited_rows = st.session_state['opponents_table']['edited_rows']
    players = deque()
    for r in edited_rows.items():
        opponent_idx, opponent_changed_values = r[0], r[1]
        # if there is an opponent without the sufficient funds
        if opponent_changed_values.get('Funds', 0) < st.session_state['big_blind_input']:
            continue
        opponent_funds = opponent_changed_values['Funds']
        opponent_name = opponent_changed_values.get('Opponents', f'Opponent {opponent_idx + 1}')
        opponent_behavior = opponent_changed_values.get('Behavior', f'Standard')
        opponent = Player(opponent_name, opponent_behavior, opponent_funds)
        players.append(opponent)
        if not players:
            st.error('No opponents in the game. Select at least one.', icon="🚨")
            return
    # Adding your player to the list of opponents in the game
    min_funds = min([r['Funds'] for r in edited_rows.values() if r['Funds'] >= st.session_state['big_blind_input']])
    your_player = Player('You', 'You', min_funds)
    players.append(your_player)
    st.session_state['you'] = your_player

    game = Game(players=players,
                small_blind=st.session_state['small_blind_input'],
                big_blind=st.session_state['big_blind_input'])
    game_round = game.play_round()
    st.session_state['game'] = game
    st.session_state['round'] = game_round

    if len(game.initial_players) == 2:
        st.session_state['players_statuses'] = {0: 'active', 1: 'in'}
    else:
        st.session_state['players_statuses'] = {index: 'in' if index != 3 else 'active'
                                                for index in range(len(game.initial_players))}


def create_players_table():
    """Create a non-editable table containing information about the players within a game."""
    game = st.session_state['game']
    all_players = game.initial_players
    all_players_names = [p.name for p in all_players]
    all_players_funds = [p.funds for p in all_players]
    all_players_ids = [p.id for p in all_players]
    blinds = ['Small', 'Big'] + [None for i in range(len(all_players)-2)]

    players_df = pd.DataFrame({
        'Player': all_players_names,
        'Funds': all_players_funds,
        'Blinds': blinds
    }, index=all_players_ids)
    st.session_state['players_table'] = players_df

    display_players_table()


def style_players_table():
    active_player_id = st.session_state['round'].players[0].id
    players_table = st.session_state['players_table']
    idx = pd.IndexSlice
    slice_ = idx[idx[active_player_id], idx[:]]
    styled_table = players_table.style.set_properties(
        **{'background-color': '#ffffb3'}, subset=slice_
    )
    return styled_table


def display_players_table():
    styled_players_table = style_players_table()
    st.dataframe(styled_players_table, hide_index=True)


def display_table():
    """Show a table with community cards."""
    img_community_cards = draw_table_cards()
    st.image(img_community_cards)


def display_your_cards():
    """Show the cards in your hand."""
    your_cards = st.session_state['you'].cards
    img_your_cards = draw_your_cards(your_cards)
    st.image(img_your_cards)


def perform_next_action():
    st.session_state['round'].next_event() # invoke next event
    create_game_layout(new_game=False)
