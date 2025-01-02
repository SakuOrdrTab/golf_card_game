'''Module for displaying the Golf card game state'''

# from src.card import Card
# from src.game import Game

class View():
    def __init__(self, game) -> None:
        self._game = game

    def _display_rows(self, row : list) -> None:
        print(row)

    def show_for_player(self, player) -> None:
        print("other players:")
        for iter_players in self._game.players:
            if iter_players is player:
                continue
            else:
                print(f"{iter_players.name}:")
                for row in iter_players.table_cards:
                    self._display_rows(row)
        print("Player's cards: ")
        for row in player.table_cards:
            self._display_rows(row)
        print("last played card: ", self._game.deck.played_cards[-1])
        print("Cards in dealing deck: ", len(self._game.deck.drawing_deck))
