import gym
import numpy as np
import math
import matplotlib.pyplot as plt
import subprocess
from ReadWriteMemory import ReadWriteMemory
from time import sleep

class TrackManiaEnv(gym.Env):
    def __init__(self):
        print('Init Track Mania')
        rwm = ReadWriteMemory()
        procces_ids_old =  rwm.enumerate_processes()
        exe_str = '"C:/Program Files (x86)/TmNationsForever/TmForever.exe"'
        parent = subprocess.Popen(exe_str, stderr=subprocess.PIPE, close_fds=True)
        procces_ids_new =  rwm.enumerate_processes()
        process_ids_diff = list(set(procces_ids_new) - set(procces_ids_old))
        print(process_ids_diff)
        print(parent)
        process = rwm.get_process_by_id(process_ids_diff[0])
        print(process.__dict__)
        sleep(5)
    def step(self, action):
        print('Step')
        ob = 0
        reward = 0
        self.done = 0
        return ob, reward, self.done, dict()

    def seed(self, seed=None):
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        return [seed]

    def reset(self):
        print('Reset')
        ob = 0
        return np.array(ob, dtype=np.float32)

    def render(self, mode='human'):
        print('Render')

    def close(self):
        print('Close')