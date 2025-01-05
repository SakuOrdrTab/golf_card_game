'''Game controller for card game "Golf"'''

from random import shuffle

from src.card_deck import CardDeck, Card
from src.player import HumanPlayer, ComputerPlayer, AdvancedComputerPlayer, Player
from src.view import View

class Game():
    """class for the game logic or 'controller' of card game 'Golf'

    Raises:
        ValueError: Number of players must be 2-4
        ValueError: Invalid return of internal game logic at player action
    """
    def __init__(self, num_players: int, human_player: bool = True, silent_mode: bool = False) -> None:
        """instantiates a golf card game. Sets players, turns initial cards
        and deals the first card to the table

        Args:
            num_players (int): number of players, 2-4
            human_player (bool, optional): Check to True to add a human player. Defaults to True.

        Raises:
            ValueError: Invalid number of players
        """        
        self.deck = CardDeck()
        self._silent_mode = silent_mode
        self.view = View(self, silent_mode=self._silent_mode)
        if num_players < 2 or num_players > 4:
            raise ValueError('Number of players must be 2-4')
        self.players = []
        self.players.append(HumanPlayer()) if human_player else self.players.append(ComputerPlayer())
        for _ in range(1, num_players):
            self.players.append(AdvancedComputerPlayer())
        for player in self.players:
            # Deal 9 cards for each player and place them in shape of 3x3
            table_cards = self.deal_initial_cards()
            for i in range(len(table_cards)//3):
                player.table_cards.append(table_cards[i*3:(i+1)*3])
            turned_cards = player.turn_initial_cards(player.table_cards)
            if not isinstance(player, HumanPlayer):
                self.view.output(f"{player.name} turns the initial cards visible.")
            for row, column in turned_cards:
                player.table_cards[row-1][column-1].visible = True
        # Turn initial card from the drawing deck to the played cards
        self.deck.deal_first_card()
        shuffle(self.players)
        self.view.output(f"Players shuffled, player {self.players[0].name} starts...")
        self.view.output("Complete init")

    def deal_initial_cards(self) -> list:
        """Deals initial 9 cards from the drawing deck

        Returns:
            list: nine Card instances in a list
        """
        return [self.deck.draw_from_deck() for _ in range(9)]

    def player_gets_card(self, player: Player) -> Card:
        """Passes control to corresponding controller, a computer or human
        player. Gets the result of whether it is wanted to draw from drawing
        deck or the played cards deck

        Args:
            player (Player): Human or other Player class instance

        Raises:
            ValueError: invalid response from the controller

        Returns:
            Card: The drawn card from either deck
        """
        action = player.get_draw_action(self.get_game_status_for_player(player))
        if action == "d": # d is drawing deck
            card = self.deck.draw_from_deck()
            card.visible = True
            self.view.output(f"{player.name} draws from the drawing deck.")
            return card
        elif action == "p": # p is played cards deck
            card = self.deck.draw_from_played()
            card.visible = True
            self.view.output(f"{player.name} draws {card} from the played deck.")
            return card
        else:
            raise ValueError("Got invalid return from Player.get_draw_action()")

    def player_plays_card(self, player: Player, hand_card : Card) -> None:
        """A player plays the card from their hand, whether human or other Player.
        The action is gotten from the actual controller in the Player class. Card is
        played either to the table or the played deck.

        Args:
            player (Player): Human or other Player
            hand_card (Card): the current hand card to be played
        """        
        action = player.get_play_action(self.get_game_status_for_player(player, hand_card))
        if action[0] == "p": # p means play card away from hand to played deck
            self.view.output(f"{hand_card} is placed in the played deck by {player.name}.")
            self.deck.add_to_played(hand_card)
        else: # should be a tuple (row, column) for play to table
            self.deck.add_to_played(player.table_cards[action[0]-1][action[1]-1])
            print_later = f"{player.table_cards[action[0]-1][action[1]-1]} is placed on the played deck from the table by {player.name}"
            player.table_cards[action[0]-1][action[1]-1] = hand_card
            self.view.output(f"{player.name} puts {hand_card} on the table at {action[0]}. row, {action[1]}. place")
            self.view.output(print_later)

    def player_plays_turn(self, player: Player) -> None:
        """Completes the drawing and playing of for one player, which constitutes
        a complete turn for that player. Also, if full rows are present,
        they are removed.

        Args:
            player (Player): human or other Player
        """        
        if isinstance(player, HumanPlayer):
            self.view.show_for_player(player)
        hand_card = self.player_gets_card(player)
        if isinstance(player, HumanPlayer):
            self.view.output(f"You got the card: {hand_card}")
        self.player_plays_card(player, hand_card)
        self.check_full_rows(player)

    def check_full_rows(self, player: Player) -> None:
        """Checks if full rows are present and removes them if so

        Args:
            player (Player): Player whose turn it is
        """
        for row in player.table_cards:
            if all([card.visible for card in row]) and len(set([card.value for card in row])) == 1:
                self.view.output(f"{player.name}'s row of cards is complete and is removed.\n{row}")
                player.table_cards.remove(row)

    def check_game_over(self) -> bool:
        """Checks if game over condition is reached. (All cards of one player visible on table)

        Returns:
            bool: Game over conditions met
        """        
        for player in self.players:
            all_visible = all([card.visible for row in player.table_cards for card in row])
            if all_visible:
                return True
        return False

    def player_score(self, player: Player) -> int:
        """Returns the player's score of card values in the table

        Args:
            player (Player): human or other player

        Returns:
            int: Sum of table Card values
        """
        return sum([card.value for row in player.table_cards for card in row])

    def play_game(self) -> tuple:
        """Runner for the golf game. Runs the turns until victory conditions are met
        Returns some data that might be needed for reinforcement learning or other
        purposes.

        Returns:
            tuple: (turns played, scores dict, winner_name)
        """
        turn = 0
        last_round = False  # Flag to indicate whether the extra round is active

        while not last_round or not self.check_game_over():
            turn += 1
            self.view.output('------------')
            self.view.output(f'Turn {turn}:')

            for player in self.players:
                self.player_plays_turn(player)

                if not last_round and self.check_game_over():
                    # Start the extra round once game-over conditions are met
                    last_round = True

            if last_round and self.check_game_over():
                break  # Exit the loop after completing the extra round

        print(f"Game over in {turn} rounds!")
        print("Scores:")
        scores = {}
        for player in self.players:
            print(f'{player.name}: {self.player_score(player)}')
            scores[player.name] = self.player_score(player)
        winner_name = list(scores.keys())[0]
        for name in scores.keys():
            if scores[name] < scores[winner_name]:
                winner_name = name
        return (turn, scores, winner_name)

    def get_game_status_for_player(self, player : Player, hand_card = None) -> dict:
        """Getter method for the game status. This can and will be passed to each player,
        so player can assess the situation for the right action. The game status does not
        reveal any information that is not available through the game's rules (nonvisible
        cards, deck, etc)

        Args:
            player (Player): human or other player, whose perspective is current
            hand_card (Card, optional): If the purpose is not to draw but to actually
            play a card, this should have the hand card. Defaults to None.

        Returns:
            dict: _game_status = dict({
                                'other_players' = [table_cards1, table_cards2 ...],
                                'player' = [table_cards],
                                'played_top_card' = Card,
                                <'hand_card' = Card>
                                })
        """        
        def table_cards_list(pl : Player) -> list:
            # helper function for getting only visible information to pass
            res = []
            for row in pl.table_cards:
                res.append(list(map(lambda x: str(x), row)))
            return res
        game_status = {}
        game_status['player'] = list(table_cards_list(player))
        game_status['other_players'] = []
        for iter_player in self.players:
            if iter_player is player:
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
