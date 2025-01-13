from src.player.golf_train_env import GolfTrainEnv

env = GolfTrainEnv()
obs, info = env.reset()
done = False
while not done:
    action = env.action_space.sample()  # random
    obs, reward, done, truncated, info = env.step(action)
    print("obs:", obs, "reward:", reward, "done:", done)
