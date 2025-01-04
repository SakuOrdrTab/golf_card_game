'''Entry for the Golf card game'''

from src.game import Game

import numpy as np
import pandas as pd

if __name__ == '__main__':
    game = Game(num_players=2, human_player=True)
    results = game.play_game()
    print(results)
