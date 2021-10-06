from tminterface.interface import TMInterface
from tminterface.client import Client, run_client
import sys


class MainClient(Client):
    def __init__(self) -> None:
        self.state = None
        self.finished = False
        self.race_time = 0
        super(MainClient, self).__init__()

    def on_registered(self, iface: TMInterface) -> None:
        print(f'Registered to {iface.server_name}')

    def on_simulation_begin(self, iface: TMInterface):
        iface.remove_state_validation()
        self.finished = False

    def on_simulation_step(self, iface: TMInterface, _time: int):
        self.race_time = _time
        if self.race_time == 0:
            self.state = iface.get_simulation_state()
            
        if self.race_time > 0:
            input_kwargs = {'left':False, 'right':False, 'accelerate':True, 'brake':False}
            iface.set_input_state(sim_clear_buffer=True, **input_kwargs)

        if self.finished:
            iface.rewind_to_state(self.state)
            self.finished = False

    def on_checkpoint_count_changed(self, iface: TMInterface, current: int, target: int):
        print(f'Reached checkpoint {current}/{target}')
        if current == target:
            print(f'Finished the race at {self.race_time}')
            self.finished = True
            iface.prevent_simulation_finish()

    def on_simulation_end(self, iface, result: int):
        print('Simulation finished')


def main():
    server_name = f'TMInterface{sys.argv[1]}' if len(sys.argv) > 1 else 'TMInterface0'
    print(f'Connecting to {server_name}...')
    run_client(MainClient(), server_name)


if __name__ == '__main__':
    main()
