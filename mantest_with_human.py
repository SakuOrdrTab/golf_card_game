'''Entry for the Golf card game'''

from src.game import Game

if __name__ == '__main__':
    game = Game(num_players=2, human_player=True, rl_player=True, silent_mode=False)
    results = game.play_game()
    print(results)
