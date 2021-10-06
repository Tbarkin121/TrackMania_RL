from tminterface.interface import TMInterface
from tminterface.client import Client, run_client
import sys
import os
import pandas as pd
from datetime import datetime
# datetime object containing current date and time
now = datetime.now()
folder_name =  os.path.join('recorded_data', now.strftime("%d.%m.%Y_%H-%M-%S\\"))
try:
    os.makedirs(folder_name)
except OSError as error:    
    pass
print("Saving to folder", folder_name)

class MainClient(Client):
    def __init__(self) -> None:
        super(MainClient, self).__init__()
        self.actions = []
        self.states = []
        self.playback_idx = 0
        self.record_data = True
        self.dataframe_idx = 0

    def on_registered(self, iface: TMInterface) -> None:
        print(f'Registered to {iface.server_name}')

    def on_run_step(self, iface: TMInterface, _time: int):
        if _time == 0:
            if(self.record_data == True):
                self.actions = []
                self.states = []
            self.playback_idx = 0

        if _time >= 0:
            state = iface.get_simulation_state()
            ckpts = iface.get_checkpoint_state()

            if(self.record_data):
                self.actions.append( (state.input_accelerate, 
                                      state.input_brake, 
                                      state.input_left, 
                                      state.input_right) )
                self.states.append( (#state.time/1000000, 
                                     #state.display_speed/1000, 
                                     state.position[0]/1000,
                                     state.position[1]/1000,
                                     state.position[2]/1000, 
                                     state.velocity[0]/1000,
                                     state.velocity[1]/1000, 
                                     state.velocity[2]/1000,
                                     state.yaw_pitch_roll[0],
                                     state.yaw_pitch_roll[1],
                                     state.yaw_pitch_roll[2]) )
            else:
                self.playback_idx += 1
                if (self.playback_idx >= len(self.actions)):
                    input_kwargs = {'left':0, 
                                    'right':0, 
                                    'accelerate':0, 
                                    'brake':0}
                else:
                    input_kwargs = {'left':self.actions[self.playback_idx][2], 
                                    'right':self.actions[self.playback_idx][3], 
                                    'accelerate':self.actions[self.playback_idx][0], 
                                    'brake':self.actions[self.playback_idx][1]}
                                
                print(input_kwargs)
                iface.set_input_state(sim_clear_buffer=True, **input_kwargs)
            print(self.states[-1])
            # print(
            #     f'Time: {_time}\n' 
            #     f'Display Speed: {state.display_speed}\n'
            #     f'Position: {state.position}\n'
            #     f'Velocity: {state.velocity}\n'
            #     f'YPW: {state.yaw_pitch_roll}\n'
            #     f'Accel_input: {state.input_accelerate}\n'
            #     f'Break_input: {state.input_brake}\n'
            #     f'Left_input: {state.input_left}\n'
            #     f'Right_input: {state.input_right}\n'
            #     f'Steer_input: {state.input_steer}\n'
            #     # f'Gas_input: {state.input_gas}\n' #Doesn't Behave as a continuious var
            # )
            # state.velocity = [state.velocity[0], 100, state.velocity[2]]
            # state.position = [state.position[0], state.position[1] + 1, state.position[2]]
            # iface.rewind_to_state(state)

            # input_kwargs = {'left':True, 'right':False, 'accelerate':True, 'brake':False}
            # iface.set_input_state(sim_clear_buffer=True, **input_kwargs)
            
    def on_checkpoint_count_changed(self, iface, current: int, target: int):
        print('checkpoint')

    def on_laps_count_changed(self, iface, current: int):
        print('lap')
        # self.record_data = False
        self.playback_idx = 0
        actions_df = pd.DataFrame(self.actions)
        states_df = pd.DataFrame(self.states)
        actions_save_path = os.path.join(folder_name, "actions_df_{}.pkl".format(self.dataframe_idx))
        states_save_path = os.path.join(folder_name, "states_df_{}.pkl".format(self.dataframe_idx))
        print('Saving ' + actions_save_path)
        actions_df.to_pickle(actions_save_path)
        print('Saving ' + states_save_path)
        states_df.to_pickle(states_save_path)
        self.dataframe_idx += 1

        #     input_kwargs = {'left':0, 
        #                     'right':0, 
        #                     'accelerate':0, 
        #                     'brake':0}
        #     iface.set_input_state(sim_clear_buffer=True, **input_kwargs)



def main():
    server_name = f'TMInterface{sys.argv[1]}' if len(sys.argv) > 1 else 'TMInterface0'
    print(f'Connecting to {server_name}...')
    run_client(MainClient(), server_name)


if __name__ == '__main__':
    main()
