import os
from numpy.core.numeric import NaN 

import torch
import gym
import tm_gym
import numpy as np

import time
from time import sleep
import math

import torch as th
from stable_baselines3 import SAC, PPO
from stable_baselines3.common.vec_env import SubprocVecEnv, VecNormalize, DummyVecEnv
from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.monitor import Monitor
from typing import Callable
from stable_baselines3.common.callbacks import CallbackList, CheckpointCallback, EvalCallback

def main():
    tb_name = 'TrackMania_FirstTest'
    env_stats_path = 'model_save/stats_' + tb_name + '.pkl'
    best_model_path = 'model_save/best/' + tb_name
    checkpoint_path = 'model_save/ckpt/' + tb_name
    start_fresh = True
    do_training = True
    do_render = True
    num_cpu = 1
    learn_step_num = 100000
    eval_freq = 100000/num_cpu #The num_cpu seemed to factor in. 1000 = 16000 for 16 cpu
    

    # nn = torch.nn.Sequential(torch.nn.Linear(8, 64), torch.nn.Tanh(),
    #                          torch.nn.Linear(64, 2))
    # agent = TRPOAgent(policy=nn)
    # agent.load_model("agent.pth")
    # agent.train("SimpleDriving-v0", seed=0, batch_size=5000, iterations=100,
    #             max_episode_length=250, verbose=True)
    # agent.save_model("agent.pth")

    policy_kwargs = dict(activation_fn=th.nn.LeakyReLU, net_arch=[dict(pi=[128, 128], vf=[128, 128])])

    # env = gym.make('TrackMania-v0')
    env = DummyVecEnv([make_env('TrackMania-v0', i, log_dir='log/') for i in range(num_cpu)])
    # env = SubprocVecEnv([make_env('TrackMania-v0', i, log_dir='log/') for i in range(num_cpu)])
    # eval_env = SubprocVecEnv([make_env('TrackMania-v0', i, log_dir='log/') for i in range(1)])
    print('Action Space :')
    print(env.action_space)
    print('Observation Space')
    print(env.observation_space)

    if(start_fresh):
        # env = VecNormalize(env, norm_obs=True, norm_reward=True, clip_obs=10.)
        obs = env.reset()
        model = PPO('MlpPolicy',
                    env, 
                    policy_kwargs = policy_kwargs, 
                    verbose=1, 
                    tensorboard_log='log/')
    else:
        # env = VecNormalize.load(env_stats_path, env)
        obs = env.reset()
        model = PPO.load(best_model_path+'/best_model.zip')
        model.set_env(env)       
    
    if(do_training):
        checkpoint_callback = CheckpointCallback(save_freq=eval_freq, 
                                                 save_path=checkpoint_path)
        # Use deterministic actions for evaluation
        # eval_callback = EvalCallback(eval_env, 
        #                             best_model_save_path=best_model_path,
        #                             log_path='log/', 
        #                             eval_freq=eval_freq,
        #                             deterministic=True, 
        #                             render=False)
        callbacks = CallbackList([checkpoint_callback])#, eval_callback])
        model.learn(total_timesteps=learn_step_num,
                    reset_num_timesteps=False, #Getting some issues with this line... not sure why
                    tb_log_name=tb_name,
                    callback=callbacks)
        model.save('model_save/' + tb_name)
        # env.save(env_stats_path)
    
    if(do_render):
        obs = env.reset()[0]
        print('obs = {}'.format(obs))
        for _ in range(2000):
            # act = torch.tensor([False, False, True, False])
            # print('act = {}'.format(act))
            act = model.predict(obs)
            print('act = {}'.format(act))
            obs, reward, done, _ = env.step(act)
            obs = obs[0]
            print('obs = {}'.format(obs))    
            if(done):
                env.reset()
            sleep(0.01)
        env.close()
        # render_env = DummyVecEnv([make_env('Cube3DStand-v0', i, log_dir='log/') for i in range(1)])
        # # eval_env = VecNormalize.load(env_stats_path, eval_env)
        # # eval_env = gym.make('SimpleDriving-v0')
        # obs = render_env.reset()
        # for _ in range(2000):
        #     action = model.predict(obs)[0]
        #     obs, reward, done, _ = render_env.step(action)
        #     render_env.render()
        #     print('action = {}'.format(action))
        #     print('observ = {}'.format(obs))
        #     print('reward = {}'.format(reward))
        #     if done:
        #         ob = render_env.reset()
        #         time.sleep(1/30)


def make_env(env_id: str, rank: int, seed: int = 4, log_dir=None) -> Callable:
    '''
    Utility function for multiprocessed env.
    
    :param env_id: (str) the environment ID
    :param num_env: (int) the number of environment you wish to have in subprocesses
    :param seed: (int) the inital seed for RNG
    :param rank: (int) index of the subprocess
    :return: (Callable)
    '''
    def _init() -> gym.Env:
        env = gym.make(env_id)
        env.connect_to_server(rank)
        # Create folder if needed
        if log_dir is not None:
            os.makedirs(log_dir, exist_ok=True)
        
        env = Monitor(env, log_dir)
        env.seed(seed + rank)
        return env
    set_random_seed(seed)
    return _init

if __name__ == '__main__':
    main()