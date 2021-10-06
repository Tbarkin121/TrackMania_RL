# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 20:50:43 2021

@author: tylerbarkin
"""

# import gym
# import numpy as np
# import math
# from tm_gym.envs.tm_env import TrackManiaEnv
# import matplotlib.pyplot as plt
# from time import sleep

#%%
# env = TrackManiaEnv()
# env.reset()
# env.step(0)
# env.render()
# env.close()

#%%
import subprocess
from ReadWriteMemory import ReadWriteMemory
from time import sleep

# print('Init Track Mania')
# rwm = ReadWriteMemory()
# procces_ids_old =  rwm.enumerate_processes()
exe_str = '"C:/Program Files (x86)/TmNationsForever/TmForever.exe"'
# # exe_str = '"C:/Program Files (x86)/TmNationsForever/TMInterface.exe"'
# exe_str = '"C:/Program Files/Mozilla Firefox/firefox.exe"'
# parent = subprocess.Popen(exe_str, stderr=subprocess.PIPE, close_fds=True)
# procces_ids_new =  rwm.enumerate_processes()
# process_ids_diff = list(set(procces_ids_new) - set(procces_ids_old))
# print(process_ids_diff)
# print(parent)
# process = rwm.get_process_by_id(process_ids_diff[0])
# print(process.__dict__)
# sleep(3)
# parent.terminate()

# https://stackoverflow.com/questions/1230669/subprocess-deleting-child-processes-in-windows
# import psutil, os

# def kill_proc_tree(pid, including_parent=True):    
#     parent = psutil.Process(pid)
#     children = parent.children(recursive=True)
#     for child in children:
#         child.kill()
#     gone, still_alive = psutil.wait_procs(children, timeout=5)
#     if including_parent:
#         parent.kill()
#         parent.wait(5)

# me = os.getpid()
# kill_proc_tree(me)

#%%
exe_str = r"C:\Program Files (x86)\TmNationsForever2\TmForever.exe"
# parent = subprocess.Popen(exe_str, stderr=subprocess.PIPE, close_fds=True)
parent = subprocess.Popen(exe_str)
#%%
print(parent.pid)
parent.terminate()

#%%
import os
os.startfile(exe_str)
