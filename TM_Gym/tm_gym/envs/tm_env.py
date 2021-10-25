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

class TrackManiaEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        print('Init Track Mania')
        self.action_space = gym.spaces.MultiBinary(4) # Right, Left, Gas, Brake
        self.observation_space = gym.spaces.box.Box(low=-1,
                                                    high=1, 
                                                    shape=(10,),
                                                    dtype=np.float32) 

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
        # print('Loading A01')
        # # Need to type in 'map A01-Race.Challenge.Gbx'
        # # Shift = 0x2A, not sure if capitalization will matter... probs...
        # # self.key_input.KeyStroke(0x41)
        # # self.key_input.KeyStroke(0x41)
        # self.key_input.KeyStroke(0x29)              # Grave
        # self.key_input.KeyStroke(0x29)              # Grave
        # self.key_input.KeyStroke(0x32)              # M
        # self.key_input.KeyStroke(0x1E)              # A
        # self.key_input.KeyStroke(0x19)              # P
        # self.key_input.KeyStroke(0x39)              # Space
        # self.key_input.KeyStroke(0x1E, cap=True)    # A
        # self.key_input.KeyStroke(0x0B)              # 0
        # self.key_input.KeyStroke(0x02)              # 1
        # self.key_input.KeyStroke(0x0C)              # -
        # self.key_input.KeyStroke(0x13, cap=True)    # R
        # self.key_input.KeyStroke(0x1E)              # A
        # self.key_input.KeyStroke(0x2E)              # C
        # self.key_input.KeyStroke(0x12)              # E
        # self.key_input.KeyStroke(0x34)              # .
        # self.key_input.KeyStroke(0x2E, cap=True)    # C
        # self.key_input.KeyStroke(0x23)              # H
        # self.key_input.KeyStroke(0x1E)              # A
        # self.key_input.KeyStroke(0x26)              # L
        # self.key_input.KeyStroke(0x26)              # L
        # self.key_input.KeyStroke(0x12)              # E
        # self.key_input.KeyStroke(0x31)              # N
        # self.key_input.KeyStroke(0x22)              # G
        # self.key_input.KeyStroke(0x12)              # E
        # self.key_input.KeyStroke(0x34)              # .
        # self.key_input.KeyStroke(0x22, cap=True)    # G
        # self.key_input.KeyStroke(0x30)              # B
        # self.key_input.KeyStroke(0x2D)              # X
        print('Loading TM1')
        self.key_input.KeyStroke(0x29)              # Grave
        self.key_input.KeyStroke(0x29)              # Grave
        self.key_input.KeyStroke(0x32)              # M
        self.key_input.KeyStroke(0x1E)              # A
        self.key_input.KeyStroke(0x19)              # P
        self.key_input.KeyStroke(0x39)              # Space
        self.key_input.KeyStroke(0x14)              # T
        self.key_input.KeyStroke(0x32)              # M
        self.key_input.KeyStroke(0x02)              # 1
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
        sleep(0.5)

    def connect_to_server(self, server_num=0):
        self.server_name = f'TMInterface{server_num}'
        print(f'Connecting to {self.server_name}...')
        self.client = run_client(MainClient(), self.server_name)
        sleep(2)
        
    def step(self, actions):
        # print('Step')
        # sleep(0.01)
        # Set Next Actions
        # print(actions)
        self.client.update_actions(right=actions[0],
                                   left=actions[1],
                                   gas=actions[2],
                                   brake=actions[3])
        # Execute Next Actions
        self.client.frame_step(frame_skip=10, speed=10)

        # Get New Observation
        obs = self.client.get_observation()
        
        reward = obs[0]/100
        # If we get a checkpoint, +1 !!! 
        if(self.client.check_ckpts()):
            reward = 1

        # If we finish the race, we are done. 
        self.done = self.client.check_done()
        sleep(0.05)
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
        self.start_state = None
        self.state = None
        super(MainClient, self).__init__()
        self.right = False
        self.left = False
        self.gas = False
        self.brake = False
        self.obs = None
        self.checkpoint_changed = False
        self.done = False
        self.iface = None
        self.frame_skip = 30
        self.frame_count  = 0
        self.running = False
        self.reset = False
        self.race_time = 0
        
    def update_actions(self, right, left, gas, brake):
        # print('update actions')
        self.right=right>0.5
        self.left=left>0.5
        self.gas=gas>0.5
        self.brake=brake>0.5

    def get_observation(self):
        # print('get_observation')
        # print('obs')
        # print(obs)
        return self.obs

    def frame_step(self, frame_skip=30, speed=1):
        # print('frame_step enter')
        if(self.iface != None):
            self.running = True
            # sleep(0.05)
            self.frame_skip = frame_skip
            self.frame_count = 0
            self.iface.set_speed(speed)
            # print('frame_step Wait Loop')
            while(self.running):
                pass
        # print('frame_step exit')

    def reset_run(self):
        # print('reset_run')
        self.reset=True
        self.done = False
        self.frame_count = 0
        # self.iface.set_speed(1)
        self.frame_step(frame_skip=1, speed=1)
        

    def check_ckpts(self):
        # print('check_ckpts')
        ckpt_change = False
        if(self.checkpoint_changed):
            ckpt_change = True
            self.checkpoint_changed = False
        return ckpt_change

    def check_done(self):
        # print('check_done')
        return self.done

    def on_registered(self, iface: TMInterface) -> None:
        print(f'Registered to {iface.server_name}')
        self.iface = iface
        self.iface.set_timeout(10000)

    def on_run_step(self, iface: TMInterface, _time: int):
        self.race_time = _time
        if(self.reset):
            # self.iface.set_speed(0)
            self.save_observation()
            if(self.start_state != None):
                self.iface.rewind_to_state(self.start_state)
            else:
                self.iface.respawn()
            self.reset=False
            return

        if _time == 0:
            self.start_state = iface.get_simulation_state()
            # print(self.start_state)
        
        if(self.frame_count == 0):
            # Update Actions
            iface.set_input_state(right=self.right, left=self.left, accelerate=self.gas, brake=self.brake)

        if(self.frame_count == self.frame_skip):
            iface.set_speed(0)
            self.save_observation()
            self.running = False
        
        # if(self.state != None):
        #     if _time>60000 or self.state.position[1]<20:
        #         self.done = True
        if(self.state != None):
            if _time>60000:
                self.done = True
        self.frame_count += 1

    def save_observation(self):
        if(self.iface != None):
            self.state = self.iface.get_simulation_state()
            # ckpts = iface.get_checkpoint_state()
            self.obs = np.array([#self.state.time/1000000, 
                                    self.state.display_speed/1000, 
                                    self.state.position[0]/1000,
                                    self.state.position[1]/1000,
                                    self.state.position[2]/1000, 
                                    self.state.velocity[0]/1000,
                                    self.state.velocity[1]/1000, 
                                    self.state.velocity[2]/1000,
                                    self.state.yaw_pitch_roll[0],
                                    self.state.yaw_pitch_roll[1],
                                    self.state.yaw_pitch_roll[2]],
                                    dtype=np.float32)    

    def on_checkpoint_count_changed(self, iface, current: int, target: int):
        self.checkpoint_changed = True
        if current == target:
            print(f'Finished the race at {self.race_time}')
            self.done = True
