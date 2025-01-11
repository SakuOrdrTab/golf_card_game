import time
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import BaseCallback, EvalCallback
import matplotlib.pyplot as plt

from src.player.golf_train_env import GolfTrainEnv

env = GolfTrainEnv()

class RewardLoggerCallback(BaseCallback):
    def __init__(self, check_freq: int = 1000, verbose: int = 1):
        super().__init__(verbose)
        self.check_freq = check_freq
        self.rewards = []
        self.timesteps = []
        self.episode_rewards = 0  # To track cumulative reward for each episode

    def _on_step(self) -> bool:
        # Update episode reward with current reward
        reward = self.locals["rewards"]  # Current reward from the environment
        self.episode_rewards += reward

        # Check if the episode is done
        if self.locals["dones"]:
            self.rewards.append(self.episode_rewards)
            self.timesteps.append(self.num_timesteps)
            if self.verbose > 0:
                print(f"Timestep {self.num_timesteps}: Episode reward = {self.episode_rewards}")
            self.episode_rewards = 0  # Reset for the next episode

        # Log at the specified frequency
        if self.num_timesteps % self.check_freq == 0:
            print(f"Timestep {self.num_timesteps}: Logging in progress...")

        return True

model_path = "golf_agent_1000000ep_DQN"
# # Load a saved model
model = DQN.load(model_path, env=env, device="cuda") 

start = time.time()

# 500 000 episodes took 13 minutes with cuda
# 2000 000 episodes took 53 minutes with cuda
EPISODES = 10000
CHECK_FREQ = 100000

reward_logger = RewardLoggerCallback(check_freq=CHECK_FREQ)

policy_kwargs = dict(net_arch=[256, 128])  
# To use CUDA you have to have a capable GPU and pytorch installment
# model = DQN("MlpPolicy", env, verbose=0, device="cuda", policy_kwargs=policy_kwargs)
# model = DQN("MlpPolicy", 
#             env, 
#             verbose=0, 
#             device="cuda", 
#             learning_rate=0.005,
#             exploration_fraction=0.3,
#             exploration_final_eps=0.03,
#             policy_kwargs=policy_kwargs
#         )

model.learn(EPISODES, callback=reward_logger)

model.save(f"golf_agent_{EPISODES}ep_DQN.zip")
print(f"Complete in {(time.time()-start)/60:.2f} minutes.")

plt.plot(reward_logger.timesteps, reward_logger.rewards)
plt.xlabel("Timesteps")
plt.ylabel("Mean Reward")
plt.title("Learning Progress")
plt.show()
