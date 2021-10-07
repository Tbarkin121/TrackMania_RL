# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 20:50:43 2021

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
# for i in range (1):
#     env.append(TrackManiaEnv())
env = TrackManiaEnv()
# env.reset()
# env.step(0)
# env.render()`
# env.close()

#%%
env.key_input.KeyStroke(0x41)
#%%
# env.render()
# for e in env:
#     e.close()
env.close()

#%%
print(env.process_id)
print(env.exe_subprocess.pid)