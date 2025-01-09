'''Gymnasium training environment for the reinforcement learning agent.'''

import numpy as np
import gymnasium as gym
from gymnasium import spaces

from src.game import Game
from src.card_deck import Card
from src.player import AdvancedComputerPlayer, ComputerPlayer

class GolfTrainEnv(gym.Env):
    def __init__(self):
        super().__init__()
        
        # PHASE 1 action space: draw from deck (0) or discard (1)
        self.action_space_phase1 = spaces.Discrete(2)
        # PHASE 2 action space: place the card on table positions 0..8 or discard (9)
        self.action_space_phase2 = spaces.Discrete(10)

        # We'll unify them by just picking the "largest" possible:
        # 0..9 => 10 discrete actions
        # In step(), if self.phase=1, we only interpret 0 or 1
        self.action_space = spaces.Discrete(10)

        # For observation space, let's assume we have 1 hand_card + 1 top_discard
        # + 9 for RL player table + 9 for opponent table = 20 integers total.
        # Each integer is in [1..21] (since we shift +1).
        # => spaces.MultiDiscrete([21]*20)
        self.observation_space = spaces.MultiDiscrete([22]*20)

        self.game = None
        self.phase = 1  # 1 = draw, 2 = play
        self.done = False
        self.num_players = 2  # For training, let's do 2-player game:
                              # RL seat is index 0, opponent seat is index 1

        self._last_drawn_card = None  # Store the card the RL seat drew in phase 1

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # Create a new game with 2 players: seat0= RL seat, seat1= Computer or Advanced AI
        # We'll let the game think it's:
        #   - (human_player=False => that means seat0 is "some" player, but we skip that)
        #   - We won't rely on the seat0's logic, we handle it ourselves.
        self.game = Game(num_players=self.num_players,
                         human_player=False,
                         rl_player=False,   # We'll bypass anyway for seat 0
                         rl_training_mode=True, # never discard rows
                         silent_mode=True)
        
        # # Optionally replace seat[1] with a better AI if you want
        # # For example:
        # self.game.players[1] = AdvancedComputerPlayer()

        self.phase = 1
        self.done = False
        self._last_drawn_card = None

        # Return observation
        observation = self._get_observation()
        # Gymnasium requires (obs, info) on reset
        return observation, {}
    
    def step(self, action):
        """
        Each step is a single sub-action for the RL seat:
          - If phase=1 => 'draw' action
          - If phase=2 => 'place' action
        Then, if phase=2, we let the other seat(s) do their full turn.
        """
        if self.done:
            # If the episode is over, we can either raise or return the same
            return self._get_observation(), 0.0, True, {}, {}

        # We'll track reward separately for final
        reward = 0.0
        info = {}

        ############################
        # PHASE 1: "draw" (action in [0..9], but only 0 or 1 matter)
        ############################
        if self.phase == 1:
            # decode 0 => "d" (deck), 1 => "p" (discard)
            # if action > 1 => we can clamp or ignore
            if action == 0:
                draw_choice = "d"
            else:
                draw_choice = "p"

            # Actually draw the card:
            if draw_choice == "d":
                self._last_drawn_card = self.game.deck.draw_from_deck()
                self._last_drawn_card.visible = True
            else:
                self._last_drawn_card = self.game.deck.draw_from_played()
                self._last_drawn_card.visible = True

            # Move to phase 2
            self.phase = 2
            obs = self._get_observation()
            return obs, reward, False, False, info

        ############################
        # PHASE 2: "play" (action in [0..9])
        ############################
        elif self.phase == 2:
            if action == 9:
                # discard
                self.game.deck.add_to_played(self._last_drawn_card)
            else:
                row = action // 3 + 1
                col = action % 3 + 1
                # We place the new card on RL seat's table,
                # discarding whatever was there
                replaced_card = self.game.players[0].table_cards[row-1][col-1]
                self.game.deck.add_to_played(replaced_card)
                self.game.players[0].table_cards[row-1][col-1] = self._last_drawn_card

            # Possibly check full rows for the RL seat, since the turn is done
            self.game.check_full_rows(self.game.players[0])

            # Now let the other seat(s) do their entire turn normally
            for i in range(1, self.num_players):
                self.game.player_plays_turn(self.game.players[i])

            # Check if the game ended
            if self.game.check_game_over():
                self.done = True

            # Possibly compute final reward
            if self.done:
                # negative final score
                # score = self.game.player_score(self.game.players[0])
                # reward = -float(score)

                # zero for loss, one for victory
                # reward = 1.0 if self.game.player_score(self.game.players[0]) < self.game.player_score(self.game.players[1]) else 0.0
                # relative score
                reward = -self.game.player_score(self.game.players[0]) + self.game.player_score(self.game.players[1])
                
                if reward > 0.0:
                    print(f"REWARD: {reward}!")

            # Move back to phase=1 (draw) for the next RL turn
            if not self.done:
                self.phase = 1

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

        # print(f"SELF PHASE: {self.phase}")

        # If we're in phase=2, we have a drawn card
        if self.phase == 2 and self._last_drawn_card is not None:
            hand_card = self._last_drawn_card
        else:
            hand_card = None

        game_status = self.game.get_game_status_for_player(
            rl_player, 
            hand_card=hand_card
        )
        
        # Now convert that status dict to a numeric observation
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
            # Face-down or hidden card
            return 20  # 20 is "nonvisible" placeholder
        else:
            # card_str might look like "C7", "D12", etc.
            # We'll parse the numeric portion after the suit char
            # Example: 'C7' => 7
            return int(card_str[1:])

    def table_cards_to_list(table_cards : list) -> list:
        """
        Convert table_cards (like [[C2, D2, X12], [...], ...]) 
        into a flat list of integers (with row placeholders).
        We'll assume up to 3 rows of 3 cards each.
        If a row is removed, we simulate with [0,0,0].
        """
        rows_missing = 3 - len(table_cards)
        res = []
        for row in table_cards:
            # row is a list of card strings
            res.extend([conv_value(card) for card in row])
        # For any removed rows, just fill with 3 zeroes each
        for _ in range(rows_missing):
            res.extend([0, 0, 0])
        return res

    observation_array = []

    # 1) Hand card (if any)
    if "hand_card" in game_status and game_status['hand_card'] is not None:
        # 'hand_card' is a Card object, so let's take its .value
        # or we could do int(card_str[1:])
        observation_array.append(game_status['hand_card'].value)
    else:
        # No hand card currently
        observation_array.append(20)

    # 2) Top of discard (played_top_card)
    top_card_value = 20 # Missing top card, can happen in some strange situations, when card is taken from played deck when it has only one and no other card has yet been placed to it.
    if "played_top_card" in game_status and game_status['played_top_card'] is not None:
        top_card_value = game_status['played_top_card'].value
    observation_array.append(top_card_value)

    # 3) RL player's table cards
    #    game_status['player'] is a list of rows => each row is a list of strings
    observation_array.extend(table_cards_to_list(game_status['player']))

    # 4) Opponent's table (assuming exactly 1 opponent for training)
    #    If there's more than 1, you'd adapt accordingly.
    if len(game_status['other_players']) > 0:
        # 'other_players' is a list of each other player's table layout
        # for training with 2 players total, we only have index 0
        observation_array.extend(table_cards_to_list(game_status['other_players'][0]))
    else:
        # No other players? fill with 9 zeroes
        observation_array.extend([0]*9)

    # Shift all values +1 so they become strictly positive
    # (MultiDiscrete requires [0..n] or [1..n], depending on usage)
    # If your max raw value is 20, then +1 => up to 21.
    observation_array = [val + 1 for val in observation_array]

    # Return it as a standard Python list or NumPy array.
    # For the environment's observation, we'll often do a np.array(...).
    # print(f"OBSERVATION ARRAY:{observation_array}")
    return np.array(observation_array, dtype=np.int32)