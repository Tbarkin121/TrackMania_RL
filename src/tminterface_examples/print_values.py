from tminterface.interface import TMInterface
from tminterface.client import Client, run_client
import sys

class MainClient(Client):
    def __init__(self) -> None:
        super(MainClient, self).__init__()

    def on_registered(self, iface: TMInterface) -> None:
        print(f'Registered to {iface.server_name}')

    def on_run_step(self, iface: TMInterface, _time: int):
        if _time >= 0:
            state = iface.get_simulation_state()
            ckpts = iface.get_checkpoint_state()

            print(
                f'Time: {_time}\n' 
                f'Display Speed: {state.display_speed}\n'
                f'Position: {state.position}\n'
                f'Velocity: {state.velocity}\n'
                f'YPW: {state.yaw_pitch_roll}\n'
                f'Accel_input: {state.input_accelerate}\n'
                f'Break_input: {state.input_brake}\n'
                f'Left_input: {state.input_left}\n'
                f'Right_input: {state.input_right}\n'
                f'Steer_input: {state.input_steer}\n'
                # f'Gas_input: {state.input_gas}\n' #Doesn't Behave as a continuious var
            )
            state.velocity = [state.velocity[0], 100, state.velocity[2]]
            # state.position = [state.position[0], state.position[1] + 1, state.position[2]]
            iface.rewind_to_state(state)

            # input_kwargs = {'left':True, 'right':False, 'accelerate':True, 'brake':False}
            # iface.set_input_state(sim_clear_buffer=True, **input_kwargs)
            


def main():
    server_name = f'TMInterface{sys.argv[1]}' if len(sys.argv) > 1 else 'TMInterface0'
    print(f'Connecting to {server_name}...')
    run_client(MainClient(), server_name)


if __name__ == '__main__':
    main()
