from player import Player
from random import choice

class ComputerPlayer(Player):
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
        print(f"{self.name} plays a card...")
        table_cards = game_status['player']
        for r, row in enumerate(table_cards):
            for c, card in enumerate(row):
                if card.value > game_status['hand_card'].value:
                    print(f"Computer returning {r+1}, {c+1}")
                    return (r + 1, c + 1)
        return ("p", None)
    