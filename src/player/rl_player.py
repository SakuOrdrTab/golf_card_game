'''Reinforcement Learning Player for Golf'''

import numpy as np
from stable_baselines3 import DQN
from gymnasium import spaces
from .player import Player

class RLPlayer(Player):
    def __init__(self, model_path: str):
        super().__init__()
        # Load the trained RL model
        # (You trained it in a separate training script/notebook)
        self.model = DQN.load(model_path)
        self.internal_phase = 1  # keep track if you use a sub-step approach
        self.last_obs = None     # store the last observation from "phase 1"

    def get_player_name(self) -> str:
        return "RL Agent"

    def get_draw_action(self, game_status: dict) -> str:
        """
        1) Convert `game_status` into the same observation vector
           the model saw in training (same encoding).
        2) Use `model.predict(obs)` to get an action.
        3) Decode the action into "d" (deck) or "p" (discard).
        """
        # We are in "draw" step => interpret the model's output accordingly.
        obs = self._encode_observation(game_status, phase=1)
        action, _ = self.model.predict(obs, deterministic=True)

        # Decode the 'action' to "d" or "p" (depending on your training scheme)
        # For instance, if action==0 => "d", action==1 => "p"
        draw_choice = "d" if action == 0 else "p"

        # Save any needed internal state if you do phase-based logic
        self.internal_phase = 2
        self.last_obs = obs

        return draw_choice

    def get_play_action(self, game_status: dict) -> tuple:
        """
        Similar to get_draw_action, but now we are in the 'placement' step.
        Convert the updated game_status (which now includes the newly drawn card)
        into an observation, call `model.predict()`, decode the action, and return.
        """
        obs = self._encode_observation(game_status, phase=2)
        action, _ = self.model.predict(obs, deterministic=True)

        # action -> either table position or discard
        if action == 9:
            play_choice = ("p", None)
        else:
            row = (action // 3) + 1
            col = (action % 3) + 1
            play_choice = (row, col)

        self.internal_phase = 1
        self.last_obs = obs

        return play_choice

    def _encode_observation(self, game_status: dict, phase: int):
        """
        Must replicate the EXACT same feature encoding you used
        in your GolfTrainEnv during training. 
        For example, turn the table cards + top discard + 'hand_card' if needed
        into a numeric vector. 
        If you used sub-step phases in training, incorporate that logic here.
        """
        # e.g., create a numpy array of length 10 (or whatever shape).
        def conv_value(card_str : str) -> int:
            # Convert card string to numeric value.
            if card_str[0] == "X":
                return 20 # 20 is nonvisible card
            else:
                return int(card_str[1:])
        def  table_card_stack_to_list(table_cards : list) -> list:
            # Convert table card stacks to a list of integers.
            rows_missing = 3 - len(table_cards)
            res = []
            for row in table_cards:
                print(row)
                res.extend([conv_value(card) for card in row])
            for row in range(rows_missing):
                res.extend([0,0,0]) # simulate removed row with kings
            return res
        observation_array = []
        if "hand_card" in game_status:
            observation_array.append(game_status['hand_card'].value)
        else:
            observation_array.append(-6) # no hand card
        observation_array.append(game_status['played_top_card'].value)
        observation_array.extend(table_card_stack_to_list(game_status['player']))
        observation_array.extend(table_card_stack_to_list(game_status['other_players'][0]))
        # It seems like multiDiscrete only accepts positive integers, so we need to shift the values by 1. (king = 0)
        observation_array = [x+1 for x in observation_array]
        return spaces.MultiDiscrete(observation_array)
        # TODO: add Suit as a attribute to the observation
        # For future use, missing third player can be ones?
