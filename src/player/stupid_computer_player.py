'''Very stupid computer player class. In practice random choosing of action'''

from random import choice, randint, random
from .player import Player

class StupidComputerPlayer(Player):
    """
    A very stupid computer player. Useful for initial training of RL players as this
    computer player in effect chooses randomly the game actions.
    """

    def __init__(self):
        super().__init__()

    def get_player_name(self) -> str:
        scp_name = choice(["M$-DOS", "Kommodore K64", "Zinclair XZ", "Victor-20", 
                           "Mc Birdbucket", "IPM 701", "UNIWAC 1101"])
        return scp_name + " " + str(randint(1,3)) + "." + str(randint(1,9))

    def get_draw_action(self, game_status: dict) -> str:
        """
        Decide whether to draw from the (d)eck or from the (p)layed pile.
        The logic is:
        randomly return 'd'eck or 'p'layed pile
        """
        return choice(['d', 'p'])

    def get_play_action(self, game_status: dict) -> tuple:
        """
        Randomly returns either ("p", None) or a tuple containing a valid index
        at table cards.
        """
        choices = [("p", None)]
        for row, _ in enumerate(range(1, len(game_status['player'])+1)):
            for column in range(1, 4):
                choices.append((row, column))
        return choice(choices)

    def turn_initial_cards(self, initial_table_cards):
        """
        Flip random card from each row
        """
        result = []
        for r, row in enumerate(initial_table_cards):
            flip_col = randint(1, len(row))
            result.append((r + 1, flip_col))
        return result
       
    def inform_game_result(self, win: bool, relative_score: int) -> None:
        """
        Inform the player about the game result.
        """
        return None