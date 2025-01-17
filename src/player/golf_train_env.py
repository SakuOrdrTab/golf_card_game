'''Gymnasium training environment for the reinforcement learning agent.'''

import numpy as np
from random import randint
from collections import Counter
import gymnasium as gym
from gymnasium import spaces

from src.game import Game
from src.card_deck import Card
from src.player import AdvancedComputerPlayer, ComputerPlayer, RLPlayer

class GolfTrainEnv(gym.Env):
    """Gymnasium environment to train RL agent to play 'Golf' card game. """    
    def __init__(self):
        super().__init__()
        
        # The golf card game play turn has two distinct steps, or phases in each
        # player's turn.
        # In this branch the RL agent playes only phase 2

        self.action_space = spaces.Discrete(10)

        # The observation space consists of all information available to the player;
        # possible hand card, played deck top card, visible table cards of the 
        # player and others. Thus, with two players, 20 variables from 1 to 22
        self.observation_space = spaces.MultiDiscrete([22]*20)

        self.game = None
        self.done = False
        self.num_players = 2  # Train with two players, seat [0] will be the trainee RL

        self._last_drawn_card = None

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.turn = 0

        # Player [0] will be the seat of RL agent and the game steps will be overridden
        # manually
        self.game = Game(num_players=self.num_players,
                         human_player=False,
                         rl_player=False,   # RL player opponent seems to screw environment
                         stupid_player=True,
                         rl_training_mode=True, # never discard rows
                         silent_mode=True)
        
        # for i, p in enumerate(self.game.players):
        #     print(f"Seat {i}: {p.name}, type = {type(p)}")

        self.done = False

        # This emulates manually former phase 1
        draw_action = self.get_algorhitmic_draw_action(self.game.get_game_status_for_player(self.game.players[0]))
        if draw_action == "d":
            hand_card = self.game.deck.draw_from_deck()
            hand_card.visible = True
        else:
            hand_card = self.game.deck.draw_from_played()
            hand_card.visible = True
        self._last_drawn_card = hand_card

        observation = self._get_observation()
        return observation, {}
    
    def step(self, action):
        """
        Each step is a single sub-action for the RL seat:
          - If phase=1 => 'draw' action
          - If phase=2 => 'place' action
        Then, if phase=2, we let the other seat(s) do their full turn.
        """

        self.turn += 1

        # Temporary measure for agent learning: limit turns to 45
        if self.game.turn > 45:
            self.done = True

        if self.done:
            # If the episode is over, we can either raise or return the same
            return self._get_observation(), 0.0, True, {}, {}

        # Intermediate reward: the change of own score
        last_turn_score = self.game.player_score(self.game.players[0])

        # We'll track reward separately for final
        reward = 0.0
        info = {}

        # phase 1 is shown in last_card_drawn

        # PHASE 2: "play" (action in [0..9])
        if action == 9:
            # discard to played deck
            self.game.deck.add_to_played(self._last_drawn_card)
        else:
            row = action // 3 + 1
            col = action % 3 + 1
            # place card on own table and discard what was there
            replaced_card = self.game.players[0].table_cards[row-1][col-1]
            self.game.deck.add_to_played(replaced_card)
            self.game.players[0].table_cards[row-1][col-1] = self._last_drawn_card

        self.game.check_full_rows(self.game.players[0])

        # Other players play their turn
        for i in range(1, self.num_players):
            self.game.player_plays_turn(self.game.players[i])

        if self.game.check_game_over():
            self.done = True

        if self.done:
            # negative final score
            # score = self.game.player_score(self.game.players[0])
            # reward = -float(score)

            # zero for loss, one for victory
            # reward = 1.0 if self.game.player_score(self.game.players[0]) < self.game.player_score(self.game.players[1]) else 0.0
            # relative score
            print("Complete at ", self.turn, " turns.")
            reward = -self.game.player_score(self.game.players[0]) + self.game.player_score(self.game.players[1])
            
            if reward > 0.0:
                print(f"REWARD: {reward}!")

            # Calculate the intermediate reward
            current_turn_score = self.game.player_score(self.game.players[0])
            intermediate_reward = (-last_turn_score + current_turn_score) / 10

            reward += intermediate_reward
                                   
            obs = self._get_observation()
            done = self.done
            return obs, reward, done, False, info
        
        else:
            # Not done yet => return normal step
            obs = self._get_observation()
            current_turn_score = self.game.player_score(self.game.players[0])
            intermediate_reward = (-last_turn_score + current_turn_score) / 10
            return obs, intermediate_reward, False, False, info
        

        
    def _get_observation(self):
        """
        Build the RL seat's observation by calling 
        self.game.get_game_status_for_player(...),
        then encode with 'game_status_to_multidiscrete'.
        """
        rl_player = self.game.players[0]

        hand_card = self._last_drawn_card

        game_status = self.game.get_game_status_for_player(
            rl_player, 
            hand_card=hand_card
        )

        obs = game_status_to_multidiscrete(game_status)
        return obs
    
    def get_algorhitmic_draw_action(self, game_status : dict) -> str:
        """For one phase algorhitmic RL, this function is an algorhitmic version
        of the draw from deck or played cards, so RL agent can play only 'play
        card' phase. Copied from RLPlayer methods

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
            
def game_status_to_multidiscrete(game_status : dict):
    """
    Convert game status to an array-like object.
    Then produce a MultiDiscrete or np.array of the appropriate length.
    """
    def conv_value(card_str : str) -> int:
        # Convert card string to numeric value.
        if card_str.startswith("X"):
            return 20 # nonvisible card
        else:
            return int(card_str[1:]) # omit suit and convert

    def table_cards_to_list(table_cards : list) -> list:
        """
        Convert (3,3) table cards to a flat list
        """
        rows_missing = 3 - len(table_cards)
        res = []
        for row in table_cards:
            # row is a list of card strings
            res.extend([conv_value(card) for card in row])
        # For any removed rows, just fill with 3 zeroes each
        for _ in range(rows_missing):
            print("Filling rows inside table_cards_to_list, this should not happen!")
            res.extend([0, 0, 0])
        return res

    observation_array = []

    # 1) Hand card (if any)
    if "hand_card" in game_status and game_status['hand_card'] is not None:
        observation_array.append(game_status['hand_card'].value)
    else:
        observation_array.append(20) # no hand card

    # 2) Top of discard (played_top_card)
    #  Missing top card, can happen in some strange situations, when card is 
    # taken from played deck when it has only one and no other card has yet been placed to it.
    top_card_value = 20
    if "played_top_card" in game_status and game_status['played_top_card'] is not None:
        top_card_value = game_status['played_top_card'].value
    observation_array.append(top_card_value)

    # 3) Current player's table cards
    observation_array.extend(table_cards_to_list(game_status['player']))

    # 4) Opponent's table (assuming exactly 1 opponent for training)
    if len(game_status['other_players']) > 0:
        observation_array.extend(table_cards_to_list(game_status['other_players'][0]))
    else:
        print("No other player, this should not happen!")
        observation_array.extend([0]*9)

    # Shift all values +1 so they become strictly positive => 1 .. 21
    # MultiDiscrete requires [1..n] in this case
    observation_array = [val + 1 for val in observation_array]

    # return as numpy array
    # print(f"OBSERVATION ARRAY:{observation_array}")
    return np.array(observation_array, dtype=np.int32)