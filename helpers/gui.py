from collections import deque

import streamlit as st
import pandas as pd

from helpers.player import Player
from helpers.game import Game


def create_new_game():
    """Initialize a game provided the input information about the opponents
    and about the blinds. Store the game in a Streamlit session state.
    Call the function creating a players table.
    """
    # if no change to the opponents table applied (no opponents)
    if not st.session_state['opponents_table']['edited_rows']:
        st.error('No opponents in the game. Select at least one.', icon="🚨")
        return
    else:
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
        min_funds = min([r['Funds'] for r in edited_rows.values() if r['Funds'] >= st.session_state['big_blind_input']])
        your_player = Player('You', 'You', min_funds)
        players.append(your_player)

        st.session_state['game'] = Game(players=players,
                                        small_blind=st.session_state['small_blind_input'],
                                        big_blind=st.session_state['big_blind_input'])

        make_players_table(new_game=True)


def make_players_table(small_blind_idx: int = 0, big_blind_idx: int = 1, new_game: bool = True):
    """Create a non-editable table containing information about the players within a game."""
    if new_game:
        game = st.session_state['game']
        all_players = game.players
        # TODO: determine the blind holders and the current players based on the order and the number of players
        players_df = pd.DataFrame([(p.name, p.funds) for p in all_players], columns=['Player', 'Funds'])
        st.dataframe(players_df)  # TODO: place it inside and "st.sempty" container so that it could be cleaned and a
                                  #  new table recreated
    else:
        pass
        # TODO make use of Round object within a game in order to understand who has blinds and who is still active
# TODO: separate new game usage and new round within a game. Different flows because if the are players who are no
#  longer in the game then they still need to be shown in the table
