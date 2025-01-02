'''Entry for the Golf card game'''

# from src#  import Card, CardDeck, Suit
from src.game import Game

if __name__ == '__main__':
    game = Game(3, human_player=False)
    game.play_game()
