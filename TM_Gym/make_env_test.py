import gym
import tm_gym
import torch
from time import sleep
import numpy as np
env = gym.make('TrackMania-v0')
env.connect_to_server(0)

obs = env.reset()
print('obs = {}'.format(obs))
for i in range(100):
    # act = torch.tensor([False, False, True, False])
    # print('act = {}'.format(act))
    obs, reward, done, _ = env.step([np.random.uniform()<0.5, 
                                     np.random.uniform()<0.5, 
                                     np.random.uniform()<0.5, 
                                     np.random.uniform()<0.5])
    print('obs = {}'.format(obs))
    print(i)
    if(done or np.random.uniform()<0.05):
        env.reset()
   

env.close()