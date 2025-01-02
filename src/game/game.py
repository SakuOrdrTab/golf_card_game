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
        # Turn initial card from the drawing deck to the played cards
        self.deck.deal_first_card()
        print("Complete init")
        print(f"gamestatus for humanplayer:", self.get_game_status_for_player(self.players[0]))
        print("Playing a turn for human player:")
        self.player_plays_turn(self.players[0])
        print("Gamestatus after:")
        print(f"gamestatus for humanplayer:", self.get_game_status_for_player(self.players[0]))

    def deal_initial_cards(self) -> list:
        '''Deal initial cards to the a player'''
        return [self.deck.draw_from_deck() for _ in range(9)]

    def player_gets_card(self, player: Player) -> Card:
        '''Player gets a playing card from either deck'''
        action = player.get_draw_action(self.get_game_status_for_player(player))
        print("Got action: ", action)
        if action == "d": # d is drawing deck
            card = self.deck.draw_from_deck()
            card.visible = True
            return card
        elif action == "p": # p is played cards deck
            card = self.deck.draw_from_played()
            card.visible = True
            return card
        else:
            raise ValueError("Got invalid return from Player.get_draw_action()")

    def player_plays_card(self, player: Player, hand_card : Card) -> None:
        '''Player plays a card from their hand'''
        action = player.get_play_action(self.get_game_status_for_player(player, hand_card))
        print("Got action: ", action)
        if action[0] == "p": # p means play card away from hand to played deck
            self.deck.add_to_played(hand_card)
        else: # should be a tuple (row, column) for play to table
            self.deck.add_to_played(player.table_cards[action[0]-1][action[1]-1])
            player.table_cards[action[0]-1][action[1]-1] = hand_card

    def player_plays_turn(self, player: Player) -> None:
        '''Play a turn of the game'''
        for player in self.players:
            hand_card = self.player_gets_card(player)
            self.player_plays_card(player, hand_card)

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

    def get_game_status_for_player(self, player : Player, hand_card = None) -> dict:
        '''Getter method for game status from a players perspective'''
        def table_cards_list(pl : Player) -> list:
            # helper function for getting only visible information to pass
            res = []
            for row in pl.table_cards:
                for card in row:
                    res.append(str(card))
            return res
        game_status = {}
        game_status['player'] = list(table_cards_list(player))
        game_status['other_players'] = []
        for iter_player in self.players:
            if iter_player is player:
                # print("Not adding the actual player")
                continue
            else:
                game_status['other_players'].append(table_cards_list(iter_player))
        if hand_card:
            game_status['hand_card'] = hand_card
        
        if len(self.deck.played_cards) > 0:
            game_status['played_top_card'] = self.deck.get_last_played_card()
        else:
            game_status['played_top_card'] = None
        return game_status
