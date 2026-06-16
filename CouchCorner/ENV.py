#import sys
#sys.path.insert(0, "../../Help_Scripts")
import hide_errors
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import mss
import cv2
import math
import random
import time

from window import verts, angle, rotate_polygon, move_polygon, get_surface_area, dist_to_end, polygon_center, reset_polygon, dist_to_opp_end

class Couch_Env(gym.Env):
    def __init__(self):
        super(Couch_Env, self).__init__()

        #x, y, rotation (degrees), dist_to_end, surface_area
        #(ints, discrete) dx, dy, dr (1 = 1px or 1deg)
        
        self.observation_space = spaces.Box(low=np.array([50, 0, 0, 0, 0], dtype=np.float32), high=np.array([2000, 600, 720, 2000, 30000], dtype=np.float32), dtype=np.float32)
        
        self.action_space = spaces.MultiDiscrete([3, 3, 3])

        self.timestep = 0
        self.counter = 0

        self.last_dist = 0

        self.num_time_ends = 0
        self.num_small_ends = 0
        self.num_goal_reached_ends = 0
        self.end_pos = (0,0)
        self.end_area = 0
        self.end_reward = 0

        self.movements = (0,0,0)

        
    def get_obs(self):
        (x, y) = polygon_center()
        return np.array([x/400, y/600, angle/720, dist_to_end()/2000, get_surface_area()/20000], dtype=np.float32)
        1000
    def reset(self, seed=None, options=None):
        reset_polygon()
        self.timestep = 0
        return self.get_obs(), {}

    def get_reward(self):
        if(get_surface_area() < 8500):
            return -100

        if(dist_to_end() < 50):
            #return get_surface_area()/200
            return 1000
        #return get_surface_area()/2000 + (1/dist_to_end())*5000
        #return (1/dist_to_end())*1000
        #d = self.last_dist-dist_to_opp_end()
        #self.last_dist = dist_to_opp_end()
        #print(d)
        #return (1 - dist_to_end()/2000)
        (x,y) = polygon_center()
        return x-225
    
    def step(self, action):
        nx = int(action[0])-1
        ny = int(action[1])-1
        nr = int(action[2])-1

        self.movements += action#(action/1000.0)

        self.timestep += 1
        self.counter += 1
        
        move_polygon(nx, ny)
        rotate_polygon(nr)

        reward = self.get_reward()

        if(get_surface_area() < 8500):
            self.num_small_ends += 1
            return self.get_obs(), reward, True, True, {}
        
        if(self.timestep > 1000):
            self.num_time_ends += 1
            return self.get_obs(), reward, False, True, {}

        if(dist_to_end() < 50):
            self.num_goal_reached_ends += 1
            return self.get_obs(), reward, True, False, {}

        if(self.counter % 1000 == 0):
            print(self.counter, "timesteps | Small Ends:", self.num_small_ends, "Time Ends:", self.num_time_ends, "Reached the goal:", self.num_goal_reached_ends, "\nEnd Position:", polygon_center(), "End surface area:", get_surface_area(), "End Reward:", reward, "Movements (X:",self.movements[0],"Y:",self.movements[1],"R:",self.movements[2],")")
            self.movements = (0,0,0)
        
        return self.get_obs(), reward, False, False, {}
        
        
    def render(self): # USUALLY LEFT EMPTY
        return
    
    def close(self): # USUALLY LEFT EMPTY
        return
        
