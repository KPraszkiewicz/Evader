import gymnasium as gym
from EvaderGym.evader.envs.evader_env_v1 import EvaderEnv_v1
import matplotlib.pyplot as plt
import numpy as np
import cv2
# create an instance of our custom environment
# env = EvaderEnv_v1(render_mode="rgb_array")
env = EvaderEnv_v1(render_mode="human")

env.reset()
#plt.imshow(env.render())


for i in range(1000):
    obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
    #env.step(0)
    env.render()
    # cv2.imshow('render', env.render())
    # cv2.waitKey(200)
    # plt.imshow(obs)
    # plt.show()
    if terminated or truncated:
        break
    
    

env.render()

# use the Gymnasium 'check_env' function to check the environment
# - returns nothing if the environment is verified as ok
#from gymnasium.utils.env_checker import check_env
#check_env(env)

print(f'Action Space: {env.action_space}')
print(f'Action Space Sample: {env.action_space.sample()}')