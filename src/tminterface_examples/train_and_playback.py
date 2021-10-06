# from re import L

from tensorflow.python.ops.numpy_ops.np_math_ops import true_divide
from tminterface.interface import TMInterface
from tminterface.client import Client, run_client
import sys, os, glob
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import tqdm
from datetime import datetime
# datetime object containing current date and time
now = datetime.now()
model_loc =  os.path.join('model', now.strftime("%d.%m.%Y_%H-%M-%S"))
print("Model Location", model_loc)
data_location = 'recorded_data\\all_data\\'
tb_name = 'MeanDriver_MoreData_Dropout_128'
load_path = 'model\\05.10.2021_19-10-29'

load_model = True
do_training = False
max_episodes = 5000
batch_size = 2048
n = 256
noise_scale = 1.0

class MainClient(Client):
    def __init__(self) -> None:
        super(MainClient, self).__init__()
        # self.actions = pd.read_pickle("actions_df.pkl").values.tolist()
        # self.states = pd.read_pickle("states_df.pkl").values.tolist()
        frames = []
        for file in glob.glob(data_location + "actions*"):
            print(file)
            frames.append(pd.read_pickle(file))
        self.actions_df = pd.concat(frames)
        
        frames = []
        for file in glob.glob(data_location + "states*"):
            print(file)
            frames.append(pd.read_pickle(file))
        self.states_df = pd.concat(frames)
        del frames


        self.actions_tensor = tf.convert_to_tensor(self.actions_df, dtype=tf.float32)
        self.states_tensor = tf.convert_to_tensor(self.states_df, dtype=tf.float32)

        # Prepare the training dataset.
        
        self.train_dataset = tf.data.Dataset.from_tensor_slices((self.states_tensor, self.actions_tensor))
        self.train_dataset = self.train_dataset.shuffle(buffer_size=30000).batch(batch_size)
        # print(self.actions_tensor)
        # print(self.states_tensor)
        
        actor_input = tf.keras.Input(shape=(9))
        x = tf.keras.layers.Dense(n)(actor_input)
        x = tf.keras.layers.LeakyReLU()(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Dropout(0.5)(x)

        y1 = tf.keras.layers.Dense(n)(x)
        y1 = tf.keras.layers.LeakyReLU()(y1)
        y1 = tf.keras.layers.BatchNormalization()(y1)
        y1 = tf.keras.layers.Dropout(0.5)(y1)
        y1 = tf.keras.layers.Dense(4)(y1)
        y1 = tf.keras.activations.sigmoid(y1)

        y2 = tf.keras.layers.Dense(n)(x)
        y2 = tf.keras.layers.LeakyReLU()(y2)
        y2 = tf.keras.layers.BatchNormalization()(y2)
        y2 = tf.keras.layers.Dropout(0.5)(y2)
        y2 = tf.keras.layers.Dense(4,activation = 'softplus')(y2)
        self.ActorModel = tf.keras.Model(actor_input, [y1, y2])
        # self.ActorModel = tf.keras.Model(actor_input, y1)

        self.ActorOptimizer = tf.keras.optimizers.Adam(learning_rate=0.0005)
        self.ActorModel.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
            loss=tf.keras.losses.BinaryCrossentropy(),
            metrics=[tf.keras.metrics.BinaryCrossentropy()],
        )
        self.loss_fun =  tf.keras.losses.BinaryCrossentropy()
        # print(self.states_tensor)
        # print(self.actions_tensor)

        summary_writer = tf.summary.create_file_writer('log\\'+tb_name)
        if(load_model):
            self.ActorModel = tf.keras.models.load_model(load_path)
        if(do_training):
            if(0):
                history = self.ActorModel.fit(
                    self.states_tensor,
                    self.actions_tensor,
                    batch_size=1024,
                    epochs=max_episodes,
                    # We pass some validation for
                    # monitoring validation loss and metrics
                    # at the end of each epoch
                    validation_data=(self.states_tensor, self.actions_tensor),
                )
                try:
                    os.makedirs(model_loc)
                except OSError as error:    
                    pass
                self.ActorModel.save(model_loc)
            else:
                with tqdm.trange(max_episodes) as t:
                    with summary_writer.as_default():
                        for i in t:
                            for step, (x_batch_train, y_batch_train) in enumerate(self.train_dataset):
                                # print(step)
                                # print(x_batch_train)
                                # print(y_batch_train)
                                # print('!!!!!!!!!!!!!!!!')
                                with tf.GradientTape() as tape:
                                    y_mean, y_std = self.ActorModel(x_batch_train)
                                    # y_mean = self.ActorModel(x_batch_train)
                                    R2 = (y_batch_train-y_mean)**2
                                    # mean_loss = tf.reduce_mean(R2)
                                    var_loss = tf.reduce_mean((R2-y_std**2)**2)
                                    # loss = mean_loss + var_loss
                                    # loss = mean_loss
                                    
                                    loss = self.loss_fun(y_batch_train, y_mean) + var_loss
                                grads = tape.gradient(loss, self.ActorModel.trainable_variables)
                                self.ActorOptimizer.apply_gradients(zip(grads, self.ActorModel.trainable_variables))

                            tf.summary.scalar('loss', loss.numpy(), step=i)
                            t.set_description(f'Episode {i}')
                            t.set_postfix(loss=loss.numpy())
                    try:
                        os.makedirs(model_loc)
                    except OSError as error:    
                        pass
                    self.ActorModel.save(model_loc)
        


    def on_registered(self, iface: TMInterface) -> None:
        print(f'Registered to {iface.server_name}')

    def on_run_step(self, iface: TMInterface, _time: int):

        if _time >= 0:
            state = iface.get_simulation_state()
            ckpts = iface.get_checkpoint_state()

            obs = tf.constant([#state.time/1000000, 
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

            # print('obs')
            # print(obs)
            random_vect = np.array([np.random.random_sample(), 
                           np.random.random_sample(), 
                           np.random.random_sample(), 
                           np.random.random_sample()])

            actions, var = self.ActorModel(obs)
            actions_np = actions.numpy() + var.numpy()*random_vect*noise_scale
            # print('actions')
            # print(actions_np)
            input_kwargs = {'left': np.round(actions_np[0][2]), 
                            'right': np.round(actions_np[0][3]), 
                            'accelerate': np.round(actions_np[0][0]), 
                            'brake': np.round(actions_np[0][1])}
                                
            print(input_kwargs)
            iface.set_input_state(sim_clear_buffer=True, **input_kwargs)


            
    def on_checkpoint_count_changed(self, iface, current: int, target: int):
        print('checkpoint')

    def on_laps_count_changed(self, iface, current: int):
        print('lap')

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
