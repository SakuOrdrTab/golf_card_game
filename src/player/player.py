'''Abstract player class for parenting different classes of players'''

from abc import ABC, abstractmethod

class Player(ABC):
    """Abstract class to define different player subclasses to be instantiated.
    Game status need to be passed to different actual subclasses. The data structture is:
    game_status = dict({
        'other_players' = [table_cards1, table_cards2 ...],
        'player' = [table_cards],
        'played_top_card' = Card,
        <'hand_card' = Card # if there is a hand card>
        })
    """    
    def __init__(self) -> None:
        """Should not be instantiated!
        """        
        self.name = self.get_player_name()
        self.table_cards = []

    @abstractmethod
    def get_player_name(self) -> str:
        """Gets player name

        Returns:
            str: player name
        """        
        pass

    @abstractmethod
    def get_draw_action(self, game_status : dict) -> str:
        """Draws from either deck or played cards

        Args:
            game_status (dict): the game status information for current 
                                player

        Returns:
            str: 'd' for deck, 'p' for played cards
        """        
        pass

    @abstractmethod
    def get_play_action(self, game_status : dict) -> tuple:
        """Plays card to the table or played deck

        Args:
            game_status (dict): game status information for current player

        Returns:
            tuple: ("p", None) for played deck, (row, col) for tables
        """
        pass

    @abstractmethod
    def turn_initial_cards(self, initial_table_cards : list) -> list:
        """Called by Game() constructor, turns one card for each row

        Args:
            initial_table_cards (list): 2d list of Cards

        Returns:
            list: list of tuples containing coordinates for cards to be
            turned
        """        
        pass
    
    @abstractmethod
    def inform_game_result(self, win : bool, relative_score : int) -> None:
        """Informs the player about the game result

        Args:
            win (bool): True if the player wins the game
            relative_score (int): relative score of the player
        """        
        pass