import os
import math
import random
import tkinter as tk
from PIL import Image
import torch
import numpy as np
from torchvision import transforms

from gameplay.enums import ActionCost, State
from gameplay.scorekeeper import ScoreKeeper
from gameplay.humanoid import Humanoid

from models.PPO import ActorCritic, PPO
from endpoints.heuristic_interface import Predictor

from gym import Env, spaces
from endpoints.data_parser import DataParser

import warnings

class RLPredictor(object):
    def __init__(self,
                 actions = 4, 
                 model_file=os.path.join('', 'model_training/RL-logs/PPO_RL-logs_0_1.pth'),
                 img_data_root='./data'):
        self.actions = actions
        self.net = None
        self.device = torch.device('cuda:0') if torch.cuda.is_available() else torch.device('cpu')
        self.transforms = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        self.is_model_loaded: bool = self._load_model(model_file)
        if not self.is_model_loaded:
            warnings.warn("Model not loaded, resorting to random prediction")
    def _load_model(self, weights_path, num_classes=4):
        try:
            K_epochs = 80               # update policy for K epochs in one PPO update

            eps_clip = 0.2          # clip parameter for PPO
            gamma = 0.99            # discount factor

            lr_actor = 0.0003       # learning rate for actor network
            lr_critic = 0.001       # learning rate for critic network
            self.net = PPO(lr_actor,lr_critic,gamma,K_epochs,eps_clip,False,0.6)
            self.net.load(weights_path)
            return True
        except Exception as e:  # file not found, maybe others?
            print(e)
            return False
    def get_action(self, observation_space):
        if self.is_model_loaded:
            action = self.net.select_action(observation_space)
        else:
            action = np.random.randint(0, self.actions)
        return action

class InferInterface(Env):
    def __init__(self, root, w, h, data_parser, scorekeeper, classifier_model_file=os.path.join('models', 'baseline.pth'), rl_model_file=os.path.join('models', 'model_training/RL-logs/PPO_RL-logs_0_0.pth'), img_data_root='data', display=False, ):
        """
        initializes RL training interface
        
        dataparser : stores humanoid information needed to retreive humanoid images and rewards
        scorekeeper : keeps track of actions being done on humanoids, score, and is needed for reward calculations
        classifier_model_file : backbone model weights used in RL observation state
        """
        self.img_data_root = img_data_root
        self.data_parser = data_parser
        self.scorekeeper = scorekeeper
        self.display = display

        self.environment_params = {
            "car_capacity": self.scorekeeper.capacity,
            "num_classes": len(Humanoid.get_all_states()),
            "num_jobs": len(Humanoid.get_all_jobs()),
            "num_actions": self.scorekeeper.actions,
        }
        self.observation_space = {"variables": np.zeros(4),
                                  "vehicle_storage_class_probs": np.zeros((self.environment_params['car_capacity'], self.environment_params['num_classes'])),
                                  "vehicle_storage_job_probs": np.zeros((self.environment_params['car_capacity'],self.environment_params['num_jobs'])),
                                  "humanoid_class_probs": np.zeros(self.environment_params['num_classes']),
                                  "job_probs": np.zeros(self.environment_params['num_jobs']),
                                  "doable_actions": np.ones(self.environment_params['num_actions'], np.int64),
                                    }

        self.action_space = spaces.Discrete(self.environment_params['num_actions'],)

        self.action_predictor = RLPredictor(rl_model_file)
        
        #helper variables
        self.reset()

        # if self.display:
        #     self.canvas = tk.Canvas(root, width=math.floor(0.2 * w), height=math.floor(0.1 * h))
        #     self.canvas.place(x=math.floor(0.75 * w), y=math.floor(0.75 * h))
        #     self.label = tk.Label(self.canvas, text="Simon says...", font=("Arial", 20))
        #     self.label.pack(side=tk.TOP)
        #
        #     self.suggestion = tk.Label(self.canvas, text=self.text, font=("Arial", 20))
        #     self.suggestion.pack(side=tk.TOP)
            
    def reset(self):
        """
        resets game for a new episode to run.
        returns observation space
        """
        self.observation_space = {"variables": np.zeros(4),
                                  "vehicle_storage_class_probs" : np.zeros((self.environment_params['car_capacity'],self.environment_params['num_classes'])),
                                  "vehicle_storage_job_probs" : np.zeros((self.environment_params['car_capacity'],self.environment_params['num_jobs'])),
                                  "humanoid_class_probs":np.zeros(self.environment_params['num_classes']),
                                  "job_probs": np.zeros(self.environment_params['num_jobs']),
                                  "doable_actions":np.ones(self.environment_params['num_actions'],np.int64),
                                    }
        self.previous_cum_reward = 0
        self.data_parser.reset()
        self.scorekeeper.reset()
        return self.observation_space


    def get_observation_space(self):
        """
        updates the observation space
        """
        self.observation_space['variables'] = np.array([self.scorekeeper.remaining_time, 
                                                        self.previous_cum_reward,
                                                        sum(self.scorekeeper.ambulance.values()),
                                                        self.scorekeeper.serum
                                                        ])
        self.observation_space["doable_actions"] = self.scorekeeper.available_action_space()
        self.observation_space["humanoid_class_probs"] = self.humanoid_probs
        self.observation_space["job_probs"] = self.job_probs
        return self.observation_space
    
    def act(self, humanoid):
        """
        Acts on the environment according the humanoid given and its observation state
        
        humanoid : the humanoid being presented
        """
        img_ = Image.open(os.path.join(self.img_data_root, humanoid.fp))

        # getting the exact class + job probs of the humanoid in the probs
        self.job_probs = humanoid.raw_probs
        self.humanoid_probs = oracle(humanoid)
        
        action_idx = self.action_predictor.get_action(self.get_observation_space())
        action = ScoreKeeper.get_action_string(action_idx)

        self.scorekeeper.map_do_action(action_idx, humanoid)
        if action == "save":
            self.observation_space["vehicle_storage_class_probs"][self.scorekeeper.get_current_capacity()-1] = self.humanoid_probs
            self.observation_space["vehicle_storage_job_probs"][self.scorekeeper.get_current_capacity()-1] = self.job_probs
        elif action == "scram":
            self.observation_space["vehicle_storage_class_probs"] = np.zeros((self.environment_params['car_capacity'],self.environment_params['num_classes']))
            self.observation_space["vehicle_storage_job_probs"] = np.zeros((self.environment_params['car_capacity'], self.environment_params['num_jobs']))
    
    def suggest(self, humanoid, pred=True):
        """
        Suggests an action on the environment according the the humanoid given and its observation state
        
        humanoid : the humanoid being presented
        """
        img_ = Image.open(os.path.join(self.img_data_root, humanoid.fp))
        if pred:
            self.humanoid_probs = self.prob_predictor.get_probs(img_)
        else:
            self.humanoid_probs = oracle(humanoid)

        self.observation_space["job_probs"] = humanoid.raw_probs
        self.observation_space["humanoid_class_probs"] = self.humanoid_probs
        
        action_idx = self.action_predictor.get_action(self.get_observation_space())
        action = ScoreKeeper.get_action_string(action_idx)
        return action


# Takes a humanoid as input and returns its class in the form of a list of probabilities
def oracle(humanoid):
    if humanoid.is_zombie():
        return [1.0, 0.0]
    elif humanoid.is_healthy():
        return [0.0, 1.0]
    else:
        return [0.5, 0.5]

