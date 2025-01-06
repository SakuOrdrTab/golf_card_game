'''Gymnasium training environment for the reinforcement learning agent.'''

import gymnasium as gym
from gymnasium import spaces

from src.game import Game

class GolfTrainEnv(gym.Env):
    def __init__(self):
        super().__init__()
        
        # PHASE 1 action space: draw from deck or discard
        #   => e.g. Discrete(2) with 0 = deck, 1 = discard
        # PHASE 2 action space: place the card in one of the (row, col) spots or discard
        #   => e.g. Discrete(10) for 9 table positions + 1 discard
        #
        # But we’ll set a single "max" action space, and switch depending on phase.
        # Alternatively, we can store two separate spaces and switch them with
        # the built-in method: self.action_space = ...
        #
        # For demonstration, let's define the largest possible Discrete we need:
        
        self.action_space_phase1 = spaces.Discrete(2)   # 0 = deck, 1 = discard
        self.action_space_phase2 = spaces.Discrete(10)  # 0..8 => (row,col), 9 => discard

        # We will set self.action_space dynamically in reset() or step().

        # Similarly, define your observation space (size depends on game representation).
        self.observation_space = ...  # e.g. spaces.Box(...)

        self.game = None
        self.phase = 1  # Start in "draw" phase
        self.done = False

    def reset(self):
        # Initialize the game, shuffle players, etc.
        self.game = Game(num_players=3, human_player=False)
        self.phase = 1
        self.done = False
        return self._get_observation()

    def step(self, action):
        if self.done:
            # If the game is over but SB3 calls step again, you could either
            # raise an exception or just return the same thing.
            return self._get_observation(), 0.0, True, {}
        
        if self.phase == 1:
            # Phase 1: agent chooses "deck" or "discard"
            # action in {0,1}
            draw_choice = "d" if action == 0 else "p"

            # Force the RL player's draw action
            self._force_draw_for_rl(draw_choice)

            # Move to phase 2 so the agent can decide how to place the drawn card
            self.phase = 2

            # Build observation that now includes the "hand card"
            obs = self._get_observation()
            reward = 0.0
            done = False  # we’re not finishing the turn or game yet
            info = {}
            return obs, reward, done, info

        elif self.phase == 2:
            # Phase 2: agent places the card (0..8 => which table spot, 9 => discard)
            if action == 9:
                play_choice = ("p", None)  # discard
            else:
                row = action // 3 + 1
                col = action % 3 + 1
                play_choice = (row, col)

            # Force the RL player's play action
            self._force_play_for_rl(play_choice)

            # Now the RL player's turn is finished. Let the other players take their turns
            self._let_other_players_play()

            # Check if the game is done
            if self.game.check_game_over():
                self.done = True

            # Compute reward
            reward = 0.0
            if self.done:
                # Example: final reward = -score
                rl_player = self.game.players[0]  # if index 0 is RL seat
                score = self.game.player_score(rl_player)
                reward = -float(score)

            # Move back to phase 1 for the next turn (if not done)
            if not self.done:
                self.phase = 1

            obs = self._get_observation()
            done = self.done
            info = {}
            return obs, reward, done, info
