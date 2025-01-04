'''Module for displaying the Golf card game state'''

class View():
    def __init__(self, game) -> None:
        """Text based view functionality. Does not take part in controls,
        all that functionality is in the Player calsses

        Args:
            game (Game): reference to the game model
        """        
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
