'''Entry for the Golf card game'''

from src.game import Game

import numpy as np
import pandas as pd

if __name__ == '__main__':
    results = pd.DataFrame(columns=['winner', 'turns', 'advanced'])
    for i in range(5000):
        game = Game(2, human_player=False)
        turns, score_dict, winner = game.play_game()
        advanced = winner.startswith("Advanced")
        new_row = pd.DataFrame(
            {
                'winner': [winner], 
                'turns': [turns], 
                'advanced': [advanced]
            }
        )
        results = pd.concat([results, new_row], ignore_index=True)

    print("Turns quartiles:")
    quartiles = results['turns'].quantile([0.25, 0.5, 0.75, 1.0])
    print(quartiles)
    print(f"Advanced winning percentage: {results['advanced'].mean() * 100}")
