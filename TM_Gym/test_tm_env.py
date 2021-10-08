# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 20:50:43 2021
12
@author: tylerbarkin
"""

import gym
import numpy as np
import math
from tm_gym.envs.tm_env import TrackManiaEnv
import matplotlib.pyplot as plt
from time import sleep

#%%
# env = []
# for i in range (5):
    # env.append(TrackManiaEnv())
env = TrackManiaEnv()
# env.reset()
# env.step(0)
# env.render()
# env.close()

#%%
# env.render()
# for e in env:
#     e.close()
for i in range(15):
    env.client.frame_step(500)
    obs = env.client.get_observation()
    print('obs')
    print(obs)
    # if(i%2==0):
    #     env.client.update_actions(right=False, 
    #                               left=False, 
    #                               gas=True, 
    #                               brake=False)
    # if(i%4==1):
    #     env.client.update_actions(right=False, 
    #                               left=True, 
    #                               gas=True, 
    #                               brake=False)
    # if(i%4==3):
    #     env.client.update_actions(right=True, 
    #                               left=False, 
    #                               gas=True, 
    #                               brake=False)
    # if(i%10==9):
    #     env.client.reset_run()
    if(i==5):
        env.client.update_actions(right=False, 
                                    left=False, 
                                    gas=True, 
                                    brake=False)
    if(i==10):
        env.client.reset_run()
        
    print(i)
    sleep(1)
env.close()

#%%
print(env.process_id)
print(env.exe_subprocess.pid)

