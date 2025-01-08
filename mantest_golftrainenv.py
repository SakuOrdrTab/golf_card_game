import time
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import BaseCallback

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

class CustomCallback(BaseCallback):
    # set info custom to 10000 episodes
    def __init__(self, check_freq: int, verbose: int = 1):
        super().__init__(verbose)
        self.check_freq = check_freq

    def _on_step(self) -> bool:
        if self.num_timesteps % self.check_freq == 0:
            print(f"Timestep {self.num_timesteps}: model is training...")
        return True
    

# model_path = "golf_agent_100000ep_DQN.zip"
# # Load a saved model
# model = DQN.load(model_path, env=env, device="cuda") 

start = time.time()

# 500 000 episodes took 13 minutes with cuda
EPISODES = 500000
CHECK_FREQ = 10000

policy_kwargs = dict(net_arch=[128, 128])  # Two hidden layers with 128 neurons each
# To use CUDA you have to have a capable GPU and pytorch installment
model = DQN("MlpPolicy", env, verbose=0, device="cuda", policy_kwargs=policy_kwargs)

model.learn(EPISODES, callback=CustomCallback(check_freq=CHECK_FREQ)) 

model.save(f"golf_agent_{EPISODES}ep_DQN.zip")
print(f"Complete in {(time.time()-start)/60:.2f} minutes.")
