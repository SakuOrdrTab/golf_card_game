'''Module for displaying the Golf card game state'''

# from src.card import Card
from src.game import Game

class View():
    def __init__(self, game : Game):
        self._game = game

    def show_player(self, player):
        print("Player's cards: ")
        print(player.table_cards)
