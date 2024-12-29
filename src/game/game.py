'''Game controller for card game "Golf"'''

class Player():
    pass

from src.card_deck import CardDeck, Card, Suit

class Game():
    '''Game controller for card game "Golf"'''
    def __init__(self, num_players: int, human_player: bool = True) -> None:
        self.deck = CardDeck()
        if num_players < 2:
            raise ValueError('Number of players must be at least 2')
        self.players = []
        if human_player:
            self.players.append(Player())
        for i in range(1, num_players):
            self.players.append(Player())
        for player in self.players:
            table_cards = self.deal_initial_cards()
            print(f'player has been dealt the following cards:')
            print(table_cards)
        
    def deal_initial_cards(self) -> list:
        '''Deal initial cards to the a player'''
        return [self.deck.draw_from_deck() for _ in range(9)]
    

