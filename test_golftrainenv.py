from src.player.golf_train_env import GolfTrainEnv
from src.player.golf_train_env import game_status_to_multidiscrete
from src import Card

env = GolfTrainEnv()

'''
[♢0, ♤2, ♤1]
[♢2, ♡12, ♤7]
[♡4, ♢6, ♤3]
Player's cards:
[♧2, ♢11, ♡7]
[♧7, ♡12, ♢6]
[♤12, ♤9, ♢8]
last played card:  ♤12
'''

test_game_status1 = {
    'hand_card': Card(1, 1),
    'played_top_card': Card(1, 2),
    'player': [["♧2", "♢11", "♡7"],
            ["♧0", "♡12", "XX"],
            ["♤12", "♤9", "♢8"]],
    'other_players': [[["♢12", "♤2", "♤1"],
            ["♢2", "♡12", "XX"],
            ["♡4", "♢6", "♤3"]]]
}

test_game_status2 = {
    'hand_card': None,
    'played_top_card': Card(1, 2),
    'player': [["♧2", "♢11", "♡7"],
            ["♧7", "♡12", "♢6"],
            ["♤12", "♤9", "♢8"]],
    'other_players': [[["♢0", "♤2", "♤1"],
            ["♢2", "♡12", "♤7"],
            ["♡4", "♢6", "♤3"]]]
}

res1 = game_status_to_multidiscrete(test_game_status1)
print(res1)
