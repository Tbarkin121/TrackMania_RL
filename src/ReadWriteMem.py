# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 18:09:17 2021

@author: tylerbarkin
"""

from ReadWriteMemory import ReadWriteMemory
import struct
import time
import subprocess
import sys
import os
from time import sleep
# Key Input
import ctypes

SendInput = ctypes.windll.user32.SendInput
W = 0x11
A = 0x1E
S = 0x1F
D = 0x20
RETURN = 0x1C 
RIGHT = 0xCD
DOWN = 0xD0

PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def test1():
    print('running main')
    base_address = 0x00400000       # "TrackMania Base Address"
    static_address_offset = 0x009560CC
    pointer_static_address = base_address + static_address_offset
    # pointer_static_address = 0x20A3344C
    offsets = [0x4, 0x2EC, 0x120]
    
    rwm = ReadWriteMemory()
    # procList()
    process = rwm.get_process_by_name('TmForever.exe')
    process.open()
    my_pointer = process.get_pointer(pointer_static_address, offsets=offsets)
    
    for _ in range(1000):
        pointer_value = process.read(my_pointer)
        data = pointer_value.to_bytes(4, 'big')
        value = struct.unpack('>f', data) #big endian
        print(value)  
        time.sleep(0.1)

def test2():
    print('running main')
    base_address = 0x5FA70000      # "TmInterface.dll Base Address"
    static_address_offset = 0x00128E5C
    pointer_static_address = base_address + static_address_offset
    # pointer_static_address = 0x20A3344C
    offsets = [0x144, 0x00, 0x58, 0x140]
    
    rwm = ReadWriteMemory()
    process = rwm.get_process_by_name('TmForever.exe')
    # process.get_process_by_id(44232)
    process.open()
    my_pointer = process.get_pointer(pointer_static_address, offsets=offsets)
    
    loop_idx = 0
    start_time = time.time()
    for _ in range(1000):
        pointer_value = process.read(my_pointer)
        data = pointer_value.to_bytes(4, 'big')
        value = struct.unpack('>f', data) #big endian
        print(value)  
        time.sleep(0.05)
        if( (loop_idx % 10) == 0):
            elapsed_time = time.time() - start_time
            print(elapsed_time)
            start_time = time.time()
        loop_idx += 1

def test3():
    rwm = ReadWriteMemory()
    out =  rwm.enumerate_processes()
    print(out)
    process = rwm.get_process_by_name('TmForever.exe')
    print(process.__dict__)
    help(process)

def test4():
    rwm = ReadWriteMemory()
    procces_ids_old =  rwm.enumerate_processes()
    # Start a new TmForever instance
    exe_str = '"E:/Program Files (x86)/TmNationsForever/TmForever.exe"'
    parent = subprocess.Popen(exe_str, stderr=subprocess.PIPE, close_fds=True)
    procces_ids_new =  rwm.enumerate_processes()
    process_ids_diff = list(set(procces_ids_new) - set(procces_ids_old))
    print(process_ids_diff)
    print(parent)
    process = rwm.get_process_by_id(process_ids_diff[0])
    print(process.__dict__)
    time.sleep(3)
    PressKey(RETURN)
    time.sleep(0.01)
    ReleaseKey(RETURN)
    time.sleep(0.25)
    PressKey(RIGHT)
    time.sleep(0.01)
    ReleaseKey(RIGHT)
    time.sleep(0.25)
    PressKey(RETURN)
    time.sleep(0.01)
    ReleaseKey(RETURN)
    time.sleep(0.25)
    PressKey(DOWN)
    time.sleep(0.01)
    ReleaseKey(DOWN)
    time.sleep(0.25)
    PressKey(RETURN)
    time.sleep(0.01)
    ReleaseKey(RETURN)
    time.sleep(0.25)
    PressKey(DOWN)
    time.sleep(0.01)
    ReleaseKey(DOWN)
    time.sleep(0.25)
    PressKey(RETURN)
    time.sleep(0.01)
    ReleaseKey(RETURN)
    time.sleep(0.25)
    PressKey(RIGHT)
    time.sleep(0.01)
    ReleaseKey(RIGHT)
    time.sleep(0.25)
    PressKey(RIGHT)
    time.sleep(0.01)
    ReleaseKey(RIGHT)
    time.sleep(0.25)
    PressKey(RETURN)
    time.sleep(0.01)
    ReleaseKey(RETURN)
    time.sleep(0.25)
    PressKey(RETURN)
    time.sleep(0.01)
    ReleaseKey(RETURN)
    time.sleep(5)
    time.sleep(0.25)
    PressKey(RETURN)
    time.sleep(0.01)
    ReleaseKey(RETURN)
    time.sleep(0.25)
    PressKey(RETURN)
    time.sleep(0.01)
    ReleaseKey(RETURN)
    time.sleep(0.25)
    PressKey(RETURN)
    time.sleep(0.01)
    ReleaseKey(RETURN)
    time.sleep(30)
    parent.terminate()
        
def main():
    test4()
    
    
if __name__ == '__main__':
    main()

