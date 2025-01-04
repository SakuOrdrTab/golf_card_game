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
        played_card_value = game_status['played_top_card'].value
        if played_card_value < 3:
            deck_choice = "p"
        elif played_card_value < 7:
            deck_choice = choice(["p", "d"])
        else:
            deck_choice = "d"
        print(f"{self.name} draws a card from {'deck' if deck_choice=='d' else 'played cards'}.")
        return deck_choice

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
                parsed = int(card_str[1:])
            except:
                parsed = randint(4,6) # assume nonvisible has this value
            return parsed
        for r, row in enumerate(self.table_cards):
            for c, card in enumerate(row):
                card_value = parse_value(str(card))
                # don't allow 0
                if card_value == 0:
                    card_value = 0.1
                # get some odds to play to table
                # low relation near 0 is really good while large value (like 12)
                # is bad
                card_value_relation = game_status['hand_card'].value / card_value
                play_to_table_chance = 100 - (card_value_relation*50)
                if randint(0, 100) < play_to_table_chance:
                    card.visible = True
                    return (r + 1, c + 1)
        return ("p", None)

    def turn_initial_cards(self, initial_table_cards):
        result = []
        for r, row in enumerate(initial_table_cards):
            result.append(((r + 1), randint(1, len(row))))
        print(f"{self.name} turns the initial cards visible.")
        return result
