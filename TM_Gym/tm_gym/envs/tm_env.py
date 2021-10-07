import gym
import numpy as np
import math
import matplotlib.pyplot as plt
import subprocess, os, signal
from ReadWriteMemory import ReadWriteMemory
from time import sleep
# Kill the process using pywin32
import psutil
import key_input

class TrackManiaEnv(gym.Env):
    def __init__(self):
        print('Init Track Mania')
        self.rwm = ReadWriteMemory()
        procces_ids_old =  self.rwm.enumerate_processes()
        sleep(0.1)
        # exe_name = 'TmForever.exe'
        exe_name = 'TMInterface'
        exe_path = 'C:/Program Files (x86)/TmNationsForever/'
        wd = os.getcwd()
        os.chdir(exe_path)
        self.exe_subprocess = subprocess.Popen(exe_name, 
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE, 
                                               shell=True,
                                               close_fds=True)
        os.chdir(wd)
        sleep(0.1)
        procces_ids_new =  self.rwm.enumerate_processes()
        process_ids_diff = list(set(procces_ids_new) - set(procces_ids_old))
        print(process_ids_diff)
        print(self.exe_subprocess)
        for id in process_ids_diff:
            self.process = self.rwm.get_process_by_id(id)
            print(self.process.__dict__)
            if(self.process.name == 'TmForever.exe'):
                self.process_id = id

        self.key_input = key_input.KeyInput()
        self.load_map()

    def load_map(self):
        print('Loading A01')
        self.key_input.KeyStroke(0x41)
        self.key_input.KeyStroke(0x41)
        self.key_input.KeyStroke(0x1)
        self.key_input.KeyStroke(0x2)
        self.key_input.KeyStroke(0x3)

        
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
        if(psutil.pid_exists(self.exe_subprocess.pid)):
            print('found pid')
        else:
            print('didnt find pid')
        # for proc in psutil.process_iter():
        #     print(proc.name())


    def close(self):
        print('Close')

        if(psutil.pid_exists(self.process_id)):
            print('found pid')
            proc = psutil.Process(self.process_id)
            proc.kill()
        else:
            print('didnt find pid')
        
        # os.kill(self.exe_subprocess.pid, signal.SIGSTOP)
        # self.exe_subprocess.kill()