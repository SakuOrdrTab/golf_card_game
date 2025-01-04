'''Abstract player class for parenting different classes of players'''

from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self) -> None:
        self.name = self.get_player_name()
        self.table_cards = []

    @abstractmethod
    def get_player_name(self) -> str:
        pass

    @abstractmethod
    def get_draw_action(self, game_status : dict) -> str:
        '''game_status = dict({
        'other_players' = [table_cards1, table_cards2 ...],
        'player' = [table_cards],
        'played_top_card' = Card
        })'''
        pass

    @abstractmethod
    def get_play_action(self, game_status : dict) -> tuple:
        '''game_status = dict({
        'other_players' = [table_cards1, table_cards2 ...],
        'player' = [table_cards],
        'played_top_card' = Card,
        'hand_card' = Card
        })'''
        pass

    @abstractmethod
    def turn_initial_cards(self, initial_table_cards : list) -> list:
        pass
