'''Very simple computer player class'''

from random import choice, randint
from .player import Player

class ComputerPlayer(Player):
    '''Computer player class, very simple game logics'''
    def get_player_name(self) -> str:
        prefix = choice(["TPU-", "CPU-", "GPU-", "Azure", "Docker"])
        postfix = choice(["cruncher", "grinder", "calculator", "calcinator",
                          "abacus", "tron", "unit", "machina"])
        return prefix+postfix

    def get_draw_action(self, game_status : dict) -> str:
        '''game_status = dict({
        'other_players' = [table_cards1, table_cards2 ...],
        'player' = [table_cards],
        'played_top_card' = Card
        })'''
        print("Do you want to draw from the (d)eck or (p)layed cards? ")
        print(f"{self.name} draws a card...")
        return choice(["p", "d"])

    def get_play_action(self, game_status : dict) -> tuple:
        '''game_status = dict({
        'other_players' = [table_cards1, table_cards2 ...],
        'player' = [table_cards],
        'played_top_card' = Card,
        'hand_card' = Card
        })'''
        def parse_value(card_str : str) -> int:
            # helper func parsing card value
            try:
                parsed = int(card_str)
            except:
                parsed = randint(3,5) # assume nonvisible has this value
            return parsed
        print(f"{self.name} plays a card...")
        table_cards = game_status['player']
        for r, row in enumerate(table_cards):
            for c, card in enumerate(row):
                card_value = parse_value(card)
                if card_value > game_status['hand_card'].value:
                    print(f"Computer returning {r+1}, {c+1}")
                    return (r + 1, c + 1)
        return ("p", None)

    def turn_initial_cards(self, initial_table_cards):
        result = []
        for r, row in enumerate(initial_table_cards):
            result.append(((r + 1), randint(1, len(row))))
        print("Computer turns initial cards: ", result)
        return result
