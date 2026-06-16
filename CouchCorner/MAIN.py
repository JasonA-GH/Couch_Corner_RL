#import sys
#sys.path.insert(0, "../../Help_Scripts")
import hide_errors
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import torch as th
import torch.nn as nn
from stable_baselines3 import PPO, DQN
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.vec_env import SubprocVecEnv

import random
import math
import time
import sys
from pathlib import Path

from ENV import Couch_Env

#from c4_env import Connect4_Env import Env

timesteps = int(sys.argv[1])

env = Couch_Env()

if(not Path("C.zip").exists()):
    print("NO SAVE FOUND! Starting new")
    model = PPO("MlpPolicy", env, verbose=1, device="cpu", batch_size=128, gamma=0.99) # CREATE MODEL
else:
    model = PPO.load("C", env=env, device="cpu") # LOAD MODEL
model.verbose = 1
if(timesteps > 1):
    model.learn(total_timesteps=timesteps, log_interval=500) # TRAIN MODEL

    model.save("C") # SAVE MODEL


from window import verts, angle, rotate_polygon, move_polygon, get_surface_area, dist_to_end, training, reset_polygon, polygon_center, draw

training = False
reset_polygon()

count = 0
last_dist = 0
while count < 1000:
    count += 1
    (x, y) = polygon_center()
    obs = np.array([x/2000, y/600, angle/720, dist_to_end()/2000, get_surface_area()/20000], dtype=np.float32)
    a, _s = model.predict(obs, deterministic=True)

    nx = int(a[0])-1
    ny = int(a[1])-1
    nr = int(a[2])-1

    #d = abs(last_dist-dist_to_end())
    #last_dist = dist_to_end()
    #print(d)
    
    if(get_surface_area() < 8500):
        break
    
    if(count % 100 == 0):
        print(a, (nx, ny, nr), count)
    
    move_polygon(nx, ny)
    rotate_polygon(nr)

    draw()

print("Final surface area:", get_surface_area(), "Final Dist:", dist_to_end())
