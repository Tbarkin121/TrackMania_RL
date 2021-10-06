import gym
import numpy as np
import math
import matplotlib.pyplot as plt


class TrackManiaEnv(gym.Env):
    def __init__(self):
        # Reaction Wheel Throttles : Vec3 (There are three unique wheel inputs)
        self.action_space = gym.spaces.box.Box(low=-1,
                                               high=1, 
                                               shape=(3,),
                                               dtype=np.float32) 

        # Base Orientation : Vec4
        # Base Velocity : Vec3
        # Flywheel Speeds : Vec3
        # Goal : None (Reward will be based on Base Orientation to start)
        self.observation_space = gym.spaces.box.Box(low=-1,
                                                    high=1, 
                                                    shape=(10,),
                                                    dtype=np.float32) 

        
    def step(self, action):
        # Feed action to the robot and get observation of robot's state
        # action = self.get_user_action()
        self.robot.apply_action(action)
        p.stepSimulation()
        robot_ob = self.robot.get_observation()

        # The reward is based on the corner Z-height
        # This structure should incentivise getting the corner as high as possible
        # I expect the bot to learn how to ballance on an edge, and maybe later a corner. 
        
        reward = self.robot.get_corner_height()
        # print(reward)
        ob = np.array(robot_ob, dtype=np.float32)

        if(self.current_step_count > self.max_step_count):
            reward = 0
            self.done = True
        self.current_step_count += 1
        
        return ob, reward, self.done, dict()

    def seed(self, seed=None):
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        return [seed]

    def reset(self):
        p.resetSimulation(self.client)
        p.setGravity(0, 0, -10)
        # Reload the Plane
        Plane(self.client)
        # Reload the Robot
        self.robot = CubeBot3D(self.client)

        # Set the goal to a random target
        self.reset_goal()
        self.done = False

        # # Visual element of the goal
        # self.goalObj = Goal(self.client, self.goal)

        # Get observation to return
        robot_ob = self.robot.get_observation()

        self.current_step_count = 0
        # print(robot_ob)
        return np.array(robot_ob, dtype=np.float32)

    # def reset_goal(self):
        # The goal is a body angle, starting with 45 deg (upright)
        # self.goal = (0.785398,) #45 deg in rad

        # print("p.getNumBodies : {}".format(p.getNumBodies()))
        # for i in range(p.getNumBodies()):
        #     print("p.getBodyInfo(i) : {}".format(p.getBodyInfo(i)))


    def render(self, mode='human'):
        pass

    def get_user_action(self):
        self.user_angle = p.readUserDebugParameter(self.angle)
        self.user_throttle = p.readUserDebugParameter(self.throttle)
        return ([self.user_throttle , self.user_angle])

    def close(self):
        p.disconnect(self.client)