'''Gymnasium training environment for the reinforcement learning agent.'''

import numpy as np
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
        # First, you either draw from deck or played cards, phase 1
        self.action_space_phase1 = spaces.Discrete(2)
        # Then you either play it to the played deck (1 option) or table (9 options),
        # phase 2
        self.action_space_phase2 = spaces.Discrete(10)

        # Unify both phases to one actual action phase
        self.action_space = spaces.Discrete(10)

        # The observation space consists of all information available to the player;
        # possible hand card, played deck top card, visible table cards of the 
        # player and others. Thus, with two players, 20 variables from 1 to 22
        self.observation_space = spaces.MultiDiscrete([22]*20)

        self.game = None
        self.phase = 1
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

        self.phase = 1 # Start from draw phase
        self.done = False
        self._last_drawn_card = None

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

        # PHASE 1: "draw" (action in [0..9], but only 0 or 1 matter)
        if self.phase == 1:
            # decode 0 => "d" (deck), 1 => "p" (discard)
            # if action > 1 => we can clamp or ignore
            if action == 0:
                draw_choice = "d"
            else:
                draw_choice = "p"

            if draw_choice == "d":
                self._last_drawn_card = self.game.deck.draw_from_deck()
                self._last_drawn_card.visible = True
            else:
                self._last_drawn_card = self.game.deck.draw_from_played()
                self._last_drawn_card.visible = True

            self.phase = 2
            obs = self._get_observation()
            return obs, reward, False, False, info

        # PHASE 2: "play" (action in [0..9])
        elif self.phase == 2:
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

            # Move back to phase=1 (draw) for the next RL turn
            if not self.done:
                self.phase = 1

            # Calculate the intermediate reward
            current_turn_score = self.game.player_score(self.game.players[0])
            intermediate_reward = (-last_turn_score + current_turn_score) / 10

            reward += intermediate_reward
                                   
            obs = self._get_observation()
            done = self.done
            return obs, reward, done, False, info
        
    def _get_observation(self):
        """
        Build the RL seat's observation by calling 
        self.game.get_game_status_for_player(...),
        then encode with 'game_status_to_multidiscrete'.
        """
        rl_player = self.game.players[0]

        if self.phase == 2 and self._last_drawn_card is not None:
            hand_card = self._last_drawn_card
        else:
            hand_card = None

        game_status = self.game.get_game_status_for_player(
            rl_player, 
            hand_card=hand_card
        )

        obs = game_status_to_multidiscrete(game_status)
        return obs    
        

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