# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 16:24:05 2021

@author: tylerbarkin
"""
from ReadWriteMemory import ReadWriteMemory
import numpy as np
import struct
import time
import subprocess
import sys
import os

class TrackMania_State():
    def __init__(self, TM_address, TMI_address):
        self.rwm = ReadWriteMemory()
        self.process = self.rwm.get_process_by_name('TmForever.exe')
        self.process.open()
        
        
        self.TM_address = TM_address
        self.TMI_address = TMI_address
        self.TMI_state_static_offset = 0x00128E5C
        self.TMI_state_static_addr =  self.TMI_address + self.TMI_state_static_offset
        
        self.pitch_addr_offsets = [0x144, 0x00, 0x58, 0x12C]
        self.roll_addr_offsets = [0x144, 0x00, 0x58, 0x130]
        self.yaw_addr_offsets = [0x144, 0x00, 0x58, 0x134]
        self.px_addr_offsets = [0x144, 0x00, 0x58, 0x140]
        self.py_addr_offsets = [0x144, 0x00, 0x58, 0x144]
        self.pz_addr_offsets = [0x144, 0x00, 0x58, 0x148]
        self.vx_addr_offsets = [0x144, 0x00, 0x58, 0x14C]
        self.vy_addr_offsets = [0x144, 0x00, 0x58, 0x150]
        self.vz_addr_offsets = [0x144, 0x00, 0x58, 0x154]
        
        self.pitch_ptr = self.process.get_pointer(self.TMI_state_static_addr, offsets=self.pitch_addr_offsets)
        self.roll_ptr = self.process.get_pointer(self.TMI_state_static_addr, offsets=self.roll_addr_offsets)
        self.yaw_ptr = self.process.get_pointer(self.TMI_state_static_addr, offsets=self.yaw_addr_offsets)
        self.px_ptr = self.process.get_pointer(self.TMI_state_static_addr, offsets=self.px_addr_offsets)
        self.py_ptr = self.process.get_pointer(self.TMI_state_static_addr, offsets=self.py_addr_offsets)
        self.pz_ptr = self.process.get_pointer(self.TMI_state_static_addr, offsets=self.pz_addr_offsets)
        self.vx_ptr = self.process.get_pointer(self.TMI_state_static_addr, offsets=self.vx_addr_offsets)
        self.vy_ptr = self.process.get_pointer(self.TMI_state_static_addr, offsets=self.vy_addr_offsets)
        self.vz_ptr = self.process.get_pointer(self.TMI_state_static_addr, offsets=self.vz_addr_offsets)
        
        self.ptr_list = [self.pitch_ptr, self.roll_ptr, self.yaw_ptr, self.px_ptr, self.py_ptr, self.pz_ptr, self.vx_ptr, self.vy_ptr, self.vz_ptr]
        
        self.pitch=0
        self.roll=0
        self.yaw=0
        self.px=0
        self.py=0
        self.pz=0
        self.vx=0
        self.vy=0
        self.vz=0
        
        self.state = np.zeros(9)
    
    def UpdateState(self):
        start_time = time.time()
        idx = 0
        for ptr in self.ptr_list:
            pointer_value = self.process.read(ptr)
            data = pointer_value.to_bytes(4, 'big')
            print('uh4')
            value = struct.unpack('>f', data) #big endian
            self.state[idx] = value[0]
            idx += 1
        return self.state

        

        

test = TrackMania_State(0x00400000, 0x5FA70000)
for _ in range(1000):
    state = test.UpdateState()
    print('state (p_x,p_y,p_z) = ({:.2f},{:.2f},{:.2f})'.format(test.state[3], test.state[4], test.state[5]))
    print('state (v_x,v_y,v_z) = ({:.2f},{:.2f},{:.2f})'.format(test.state[6], test.state[7], test.state[8]))
    time.sleep(0.05)