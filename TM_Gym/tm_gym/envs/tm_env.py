import gym
import numpy as np
import math
import matplotlib.pyplot as plt
import subprocess, os, signal
from ReadWriteMemory import ReadWriteMemory
from time import sleep
# Kill the process using pywin32
import psutil
from tm_gym.envs.key_input import KeyInput
# TM Interface related stuff
from tminterface.interface import TMInterface
from tminterface.client import Client, run_client
import sys
import tensorflow as tf

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

        self.key_input = KeyInput()
        sleep(1)
        self.load_map()

    def load_map(self):
        print('Loading A01')
        # Need to type in 'map A01-Race.Challenge.Gbx'
        # Shift = 0x2A, not sure if capitalization will matter... probs...
        # self.key_input.KeyStroke(0x41)
        # self.key_input.KeyStroke(0x41)
        self.key_input.KeyStroke(0x29)              # Grave
        self.key_input.KeyStroke(0x29)              # Grave
        self.key_input.KeyStroke(0x32)              # M
        self.key_input.KeyStroke(0x1E)              # A
        self.key_input.KeyStroke(0x19)              # P
        self.key_input.KeyStroke(0x39)              # Space
        self.key_input.KeyStroke(0x1E, cap=True)    # A
        self.key_input.KeyStroke(0x0B)              # 0
        self.key_input.KeyStroke(0x02)              # 1
        self.key_input.KeyStroke(0x0C)              # -
        self.key_input.KeyStroke(0x13, cap=True)    # R
        self.key_input.KeyStroke(0x1E)              # A
        self.key_input.KeyStroke(0x2E)              # C
        self.key_input.KeyStroke(0x12)              # E
        self.key_input.KeyStroke(0x34)              # .
        self.key_input.KeyStroke(0x2E, cap=True)    # C
        self.key_input.KeyStroke(0x23)              # H
        self.key_input.KeyStroke(0x1E)              # A
        self.key_input.KeyStroke(0x26)              # L
        self.key_input.KeyStroke(0x26)              # L
        self.key_input.KeyStroke(0x12)              # E
        self.key_input.KeyStroke(0x31)              # N
        self.key_input.KeyStroke(0x22)              # G
        self.key_input.KeyStroke(0x12)              # E
        self.key_input.KeyStroke(0x34)              # .
        self.key_input.KeyStroke(0x22, cap=True)    # G
        self.key_input.KeyStroke(0x30)              # B
        self.key_input.KeyStroke(0x2D)              # X
        self.key_input.KeyStroke(0x1C)              # Return
        self.key_input.KeyStroke(0x29)              # Grave
        self.key_input.KeyStroke(0xCD)              # Right
        # self.key_input.KeyStroke(0xCD)              # Right
        self.key_input.KeyStroke(0x1C)              # Return
        sleep(2)
        self.key_input.KeyStroke(0x1C)              # Return
        sleep(0.1)
        self.key_input.KeyStroke(0x1C)              # Return
        sleep(0.1)
        self.key_input.KeyStroke(0x1C)              # Return

        self.server_name = f'TMInterface{sys.argv[1]}' if len(sys.argv) > 1 else 'TMInterface0'
        print(f'Connecting to {self.server_name}...')
        self.client = run_client(MainClient(), self.server_name)

        
    def step(self, actions):
        print('Step')
        self.client.update_actions(right=actions[0],
                                   left=actions[1],
                                   gas=actions[2],
                                   brake=actions[3])
        obs = self.client.get_observation()
        #What is the reward? 
        #Lets say 1 per check point. 
        if(self.client.check_ckpts()):
            reward = 1
        else:
            reward = 0

        #How do we know when we are done?
        #There is some sort of done signal
        self.done = self.client.check_done()
        return obs, reward, self.done, dict()

    def seed(self, seed=None):
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        return [seed]

    def reset(self):
        print('Reset')
        self.client.reset_run()
        obs = self.client.get_observation()
        return np.array(obs, dtype=np.float32)

    def render(self, mode='human'):
        print('Render')

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

class MainClient(Client):
    def __init__(self) -> None:
        self.state = None
        super(MainClient, self).__init__()
        self.right = False
        self.left = False
        self.gas = False
        self.brake = False
        self.obs = None
        self.reset = False
        self.checkpoint_changed = False
        self.done = False
        self.iface = None
        self.frame_skip = 30

    def update_actions(self, right, left, gas, brake):
        self.right=right
        self.left=left
        self.gas=gas
        self.brake=brake

    def get_observation(self):
        # print('obs')
        # print(obs)
        return self.obs

    def frame_step(self, frame_skip=30):
        if(self.iface != None):
            self.iface.set_speed(1)
        self.frame_skip = frame_skip

    def reset_run(self):
        self.reset=True

    def check_ckpts(self):
        ckpt_change = False
        if(self.checkpoint_changed):
            ckpt_change = True
            self.checkpoint_changed = False
        return ckpt_change

    def check_done(self):
        return self.done

    def on_registered(self, iface: TMInterface) -> None:
        print(f'Registered to {iface.server_name}')

    def on_run_step(self, iface: TMInterface, _time: int):
        if _time % self.frame_skip==0:
            iface.set_speed(0)
        if _time == 0:
            self.iface = iface
            self.state = iface.get_simulation_state()
            print(self.state)

        state = iface.get_simulation_state()
        # ckpts = iface.get_checkpoint_state()
        self.obs = tf.constant([#state.time/1000000, 
                            #state.display_speed/1000, 
                            state.position[0]/1000,
                            state.position[1]/1000,
                            state.position[2]/1000, 
                            state.velocity[0]/1000,
                            state.velocity[1]/1000, 
                            state.velocity[2]/1000,
                            state.yaw_pitch_roll[0],
                            state.yaw_pitch_roll[1],
                            state.yaw_pitch_roll[2]],
                            shape=(1,9),
                            dtype=tf.float32)

        # Update Actions
        iface.set_input_state(right=self.right, left=self.left, accelerate=self.gas, brake=self.brake)

        # if _time == 500:
        #     self.state = iface.get_simulation_state()
 
        if(self.reset):
            # iface.rewind_to_state(self.state)
            iface.respawn()
            self.reset=False
            self.done = False

    def on_checkpoint_count_changed(self, iface, current: int, target: int):
        self.checkpoint_changed = True
        if current == target:
            print(f'Finished the race at {self.race_time}')
            self.done = True
