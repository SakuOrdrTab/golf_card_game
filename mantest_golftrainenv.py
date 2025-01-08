from stable_baselines3 import DQN

from src.player.golf_train_env import GolfTrainEnv

env = GolfTrainEnv()

# '''
# [♢0, ♤2, ♤1]
# [♢2, ♡12, ♤7]
# [♡4, ♢6, ♤3]
# Player's cards:
# [♧2, ♢11, ♡7]
# [♧7, ♡12, ♢6]
# [♤12, ♤9, ♢8]
# last played card:  ♤12
# '''

EPISODES = 100000
model = DQN("MlpPolicy", env, verbose=1)
model.learn(EPISODES) # try 100000
model.save(f"golf_agent_{EPISODES}ep_DQN.zip")
