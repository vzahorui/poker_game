import streamlit as st

from utils.gui import gui_workers


MAX_PLAYERS = 14

col1_outer, col2_outer = st.columns([3, 1])

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

        new_game_button = st.form_submit_button("Start a new game", on_click=gui_workers.create_game_layout)

gui_workers.manipulate_css()