'''Reinforcement Learning Player for Golf'''

import numpy as np
from random import randint
from collections import Counter

from stable_baselines3 import DQN
# from gymnasium import spaces
from .player import Player

class RLPlayer(Player):
    def __init__(self):
        super().__init__()
        # Load the trained RL model , use cpu for compability
        self.model = DQN.load("golf_agent_1000000ep_DQN", device="cpu")
        self.internal_phase = 1  # keep track if you use a sub-step approach
        self.last_obs = None     # store the last observation from "phase 1"

    def get_player_name(self) -> str:
        return "RL Agent " + str(randint(1,10000))
    
    def get_algorhitmic_draw_action(self, game_status : dict) -> str:
        """For one phase algorhitmic RL, this function is an algorhitmic version
        of the draw from deck or played cards, so RL agent can play only 'play
        card' phase.

        Args:
            game_status (dict): game status passed from Game()

        Returns:
            str: "p" for played deck, "d" for drawing deck
        """
        if game_status['played_top_card'] != None:
            played_card_value = game_status['played_top_card'].value
        else:
            print("[DEBUG] No played cards")
            return "d" # no played cards
        
        # keep score which seems better option, initial values
        inclination_d = 1
        inclination_p = 1
        
        current_table_cards = []
        for card in (c for row in game_status['player'] for c in row):
            if str(card) != "XX":
                current_table_cards.append(int(card[1:]))
        
        print("[DEBUG] table card values: ", current_table_cards)
        print("[DEBUG] played card value: ", played_card_value)

        # Increase "p" inclination if p card is better than biggest table card
        # Otherwise increase "d" inclination
        biggest_table_card = max(current_table_cards)
        if biggest_table_card >= played_card_value:
            inclination_p += biggest_table_card - played_card_value
        else:   
            inclination_d += played_card_value - biggest_table_card

        # if played card is really good, increase inclination, otherwise "d"
        if played_card_value < 3:
            inclination_p += (3 - played_card_value) * 2
        elif played_card_value >= 10:
            inclination_d += (played_card_value - 9) * 2

        # If there are almost complete rows, increase "p" inclination
        if str(played_card_value) in self._pairs_in_own_tablecards(game_status['player']):
            inclination_p += 20

        # Do the randomization and return value
        inclination_p *= inclination_p # add to 2nd power to reduce randomness
        inclination_d *= inclination_d
        total_inclination = inclination_p + inclination_d
        draw_from_deck = randint(1, total_inclination) <= inclination_d
        print(f"[DEBUG] Did lottery: deck_inc: {inclination_d} played_inc: {inclination_p} total: {total_inclination} res: {draw_from_deck}")
        return "d" if draw_from_deck else "p"
        

    def _pairs_in_own_tablecards(self, table_cards : list) -> list:
        res = []
        for row in table_cards:
            strs = [item[1:] for item in row if item != "XX"]
            counts = Counter(strs)
            res.append([item for item, count in counts.items() if count > 1])
        return res
        
    def get_draw_action(self, game_status: dict) -> str:
        """
        1) Convert `game_status` into the same observation vector
           the model saw in training (same encoding).
        2) Use `model.predict(obs)` to get an action.
        3) Decode the action into "d" (deck) or "p" (discard).
        """
        # We are in "draw" step => interpret the model's output accordingly.
        # obs = self._encode_observation(game_status, phase=1)
        # print("[DEBUG]Next doing model predict draw, player:", self.name)
        # action, _ = self.model.predict(obs, deterministic=True)

        # Decode the 'action' to "d" or "p" (depending on your training scheme)
        # For instance, if action==0 => "d", action==1 => "p"
        draw_choice = self.get_algorhitmic_draw_action(game_status=game_status)

        # Save any needed internal state if you do phase-based logic
        # self.internal_phase = 2
        # self.last_obs = obs

        return draw_choice

    def get_play_action(self, game_status: dict) -> tuple:
        """
        Similar to get_draw_action, but now we are in the 'placement' step.
        Convert the updated game_status (which now includes the newly drawn card)
        into an observation, call `model.predict()`, decode the action, and return.
        """
        obs = self._encode_observation(game_status, phase=2)
        # print("[DEBUG]Next doing model predict play, player:", self.name)
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
        def table_card_stack_to_list(table_cards : list) -> list:
            # Convert table card stacks to a list of integers.
            rows_missing = 3 - len(table_cards)
            res = []
            for row in table_cards:
                # print(row)
                res.extend([conv_value(card) for card in row])
            for row in range(rows_missing):
                res.extend([0,0,0]) # simulate removed row with kings
            return res
        observation_array = []
        if "hand_card" in game_status:
            observation_array.append(game_status['hand_card'].value)
        else:
            observation_array.append(20) # no hand card
        
        # 2) Top of discard (played_top_card)
        top_card_value = 20 # Missing top card, can happen in some strange situations, when card is taken from played deck when it has only one and no other card has yet been placed to it.
        if "played_top_card" in game_status and game_status['played_top_card'] is not None:
            top_card_value = game_status['played_top_card'].value
        observation_array.append(top_card_value)

        observation_array.extend(table_card_stack_to_list(game_status['player']))
        observation_array.extend(table_card_stack_to_list(game_status['other_players'][0]))
        # It seems like multiDiscrete only accepts positive integers, so we need to shift the values by 1. (king = 0)
        observation_array = [x+1 for x in observation_array]
        # print("OBS ARRAY: ", observation_array)
        return np.array(observation_array, dtype=np.int32)
        # TODO: add Suit as a attribute to the observation
        # For future use, missing third player can be ones?

    def inform_game_result(self, win: bool, relative_score: int) -> None:
        """
        Inform the player about the game result.
        """
        return None
    
    def turn_initial_cards(self, initial_table_cards):
        """
        Same as AdvancedComputerPlayer, just random card from each row.
        """
        result = []
        for r, row in enumerate(initial_table_cards):
            flip_col = randint(1, len(row))
            result.append((r + 1, flip_col))

        return result  