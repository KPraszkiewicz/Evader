import gymnasium as gym
from EvaderGym.evader.envs.evader_env_v1 import EvaderEnv_v1
import matplotlib.pyplot as plt
import numpy as np
import cv2
import math
# create an instance of our custom environment
# env = EvaderEnv_v1(render_mode="rgb_array")
env = EvaderEnv_v1(render_mode="human")

env.reset()
#plt.imshow(env.render())

def vector_to_action(v):

    angle = math.atan2(v[1], v[0])
    if(angle < 0):
        angle = math.pi*2 +  angle

    angle = angle / (math.pi*2 )
    return (round(angle *8) % 8)

def calc_distance(v1, v2):
    vector = [v1[0] - v2[0], v1[0] - v2[1]]
    return math.sqrt(vector[0]**2 + vector[1]**2)

action = 8

print(vector_to_action([1,0])) #0
print(vector_to_action([1,1])) # 1
print(vector_to_action([0,1])) # 2
print(vector_to_action([-1,1]))  # 3
print(vector_to_action([-1,0])) # 4
print(vector_to_action([-1,-1])) # 5
print(vector_to_action([0,-1])) # 6 
print(vector_to_action([1,-1])) # 7
print(vector_to_action([1,0]))

print(vector_to_action([0,10]))
print(vector_to_action([-10,0]))
print(vector_to_action([-10,-1]))
print(vector_to_action([0,-10]))
print(vector_to_action([10,-1]))

for i in range(1000):
    # obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
    obs, reward, terminated, truncated, info = env.step(action)

    # algorytm
    agent = info['agent']
    bullets = info['bullets']
    vectors = []
    distanses = []

    for b in bullets:
        v1 = b.velocity[0]
        v2 = b.velocity[1]
        print("BV: ", b.velocity)
        if v1 == 0:
            y = 0
            x = 1
        elif v2 == 0:
            y = 1
            x = 0
        else:
            x = 1
            y = -v1/v2
        
        va = [agent.x + x, agent.y + y]
        vb = [agent.x - x, agent.y - y]

        d1 = b.calc_distance_to(va)
        d2 = b.calc_distance_to(vb)
        if(d1 < d2):
            vectors.append([-x,-y])
            distanses.append(d1**2)
        else:
            vectors.append([x,y])
            distanses.append(d2**2)

        
    if(len(vectors) > 0):    
        mx = 0
        my = 0
        max_d = np.max(distanses)
        for i in range(len(vectors)):
            d = distanses[i] / max_d
            mx += vectors[i][0] * d
            my += vectors[i][1] * d
        
        print(mx,my)
        action = vector_to_action([mx, my])
        


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