'''Game controller for card game "Golf"'''

from src.card_deck import CardDeck, Card, Suit
from src.player import HumanPlayer, ComputerPlayer, Player

class Game():
    '''Game controller for card game "Golf"'''
    def __init__(self, num_players: int, human_player: bool = True) -> None:
        self.deck = CardDeck()
        if num_players < 2:
            raise ValueError('Number of players must be at least 2')
        self.players = []
        if human_player:
            self.players.append(HumanPlayer())
        for _ in range(1, num_players):
            self.players.append(ComputerPlayer())
        for player in self.players:
            # Deal 9 cards for each player and place them in shape of 3x3
            table_cards = self.deal_initial_cards()
            for i in range(len(table_cards)//3):
                player.table_cards.append(table_cards[i*3:(i+1)*3])
            print(f'player {player.name} has been dealt the following cards:')
            print(table_cards)
            # Turn the initial cards of the player    
            turned_cards = player.turn_initial_cards(player.table_cards)
            for row, column in turned_cards:
                player.table_cards[row-1][column-1].visible = True

        print("Complete init")

    def deal_initial_cards(self) -> list:
        '''Deal initial cards to the a player'''
        return [self.deck.draw_from_deck() for _ in range(9)]

    def player_gets_card(self, player: Player) -> None:
        '''Player gets a playing card from either deck'''
        pass

    def player_plays_card(self, player: Player) -> None:
        '''Player plays a card from their hand'''
        pass

    def player_plays_turn(self, player: Player) -> None:
        '''Play a turn of the game'''
        for player in self.players:
            self.player_gets_card(player)
            self.player_plays_card(player)

    def check_full_rows(self, player: Player) -> None:
        '''Check if the player has a full row and remove'''
        for row in player.table_cards:
            if all([card.visible for card in row]):
                player.table_cards.remove(row)

    def check_game_over(self) -> bool:
        '''Check if the game is over'''
        for player in self.players:
            all_visible = all([card.visible for row in player.table_cards for card in row])
            if all_visible:
                return True
        return False

    def player_score(self, player: Player) -> int:
        '''Calculate the score of the player'''
        return sum([card.value for row in player.table_cards for card in row])

    def play_game(self) -> None:
        '''Play the game'''
        pass
