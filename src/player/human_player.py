'''submodule for human player'''

from .player import Player

class HumanPlayer(Player):
    """Subclass of abstract class Player. A human player.
    Controller for the class implementing the interface, but not
    model or view

    Args:
        Player (): Abstract Player class
    """    
    def get_player_name(self) -> str:
        """Asks for player name and returns it

        Returns:
            str: Human player name
        """        
        return input("Please input you name: ")
    
    def get_draw_action(self, game_status : dict) -> str:
        """Human player interface for asking whether player wants to
        draw from the dealing deck or the played cards

        Args:
            game_status (dict): to be agnostic about whether player is
            human or other, this is passed.

        Returns:
            str: 'd' is drawing deck and 'p' is played cards
        """        
        print("Do you want to draw from the (d)eck or (p)layed cards? ")
        while True:
            answer = input().lower()
            if answer in ['d', 'p']:
                return answer
            else:
                print("Invalid command, please input 'd' or 'p'")
    
    def get_play_action(self, game_status : dict) -> tuple:
        """A Human player interface returning whether the player wants
        to play the drawn card to table or the played deck.

        Args:
            game_status (dict): to be agnostic about whether player is
            human or other, this is passed.     

        Returns:
            tuple: either ('p', None) for playing to the played deck, or
                   the coordinates (row, column) where the card is placed
        """        
        print("Where do you want to play the card? ")
        print("(P)layed card deck, place it in table (row, column): ")
        while True:
            answer = input().lower()
            if answer == "p":
                return ("p", None)
            else:
                try:
                    row, column = [int(x.strip()) for x in answer.split(",")]
                    # print("After split: ", row, column)
                    return (row, column)
                except:
                    print("Invalid input")
            print("Please either state 'p' to place the card in your hand")
            print("to the played deck, or give a coordinate separated by ',' to place")
            print("the card in your table and that card goes to the played deck.")
            print("Coordinates are for example 1,2 where 1 is rrrrrrrrrthe first row and 2 is")
            print("the second column")

    def turn_initial_cards(self, initial_table_cards):
        """At the beginning of the game, Game() constructor calls this to turn one
        card for each row. Human interface

        Args:
            initial_table_cards (list): two dimensional list of Cards

        Returns:
            list: list of tuples of turned cards coordinates
        """        
        result = []
        for r, row in enumerate(initial_table_cards):
            print(f"Which card do you want to turn for row {row}")
            while True:
                try:
                    ans = int(input())
                    if ans < 1 or ans > len(row):
                        raise ValueError(f"Card number must be between 1 and {len(row)}!")
                    break
                except:
                    print("Try again...")
            result.append((r + 1, ans))
        return result
