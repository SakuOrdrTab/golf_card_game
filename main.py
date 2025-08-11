'''Entry for the Golf card game'''

from src.game import Game

# import numpy as np
import pandas as pd

# "Stupid...", "RL Agent...", "Comput...", "Advanc...", "Human..."
BENCHMARK_PLAYER_DESC = "Stupid player"


if __name__ == '__main__':
    results = pd.DataFrame(columns=['winner', 'turns', 'advanced'])
    for i in range(100):
        game = Game(2, 
                    human_player=False, 
                    silent_mode=False, 
                    stupid_player=True,
                    advanced_player=False,
                    rl_player=True)
        turns, score_dict, winner = game.play_game()
        benchmark_row = winner.startswith(BENCHMARK_PLAYER_DESC[:6])
        new_row = pd.DataFrame(
            {
                'winner': [winner], 
                'turns': [turns], 
                BENCHMARK_PLAYER_DESC: [benchmark_row]
            }
        )
        results = pd.concat([results, new_row], ignore_index=True)

    print("Turns quartiles:")
    quartiles = results['turns'].quantile([0.25, 0.5, 0.75, 1.0])
    print(quartiles)
    print(f"{BENCHMARK_PLAYER_DESC} winning percentage: {results[BENCHMARK_PLAYER_DESC].mean() * 100}")
