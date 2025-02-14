from gameplay.enums import ActionCost, ActionState, JobBaseEffect
import pandas as pd
from ui_elements.probability import Probability
import random
import os
from collections import Counter


MAP_ACTION_STR_TO_INT = {s.value:i for i,s in enumerate(ActionState)}
MAP_ACTION_INT_TO_STR = [s.value for s in ActionState]


class ScoreKeeper(object):
    def __init__(self, shift_len, capacity):
        
        self.shift_len = int(shift_len)  # minutes
        self.capacity = capacity
        self.carrying = []
        
        self.actions = 5
        self.diff = None
        
        self.logger = []
        self.all_logs = []
        
        self.serum = 0

        self.reset()
        
    def reset(self):
        """
        resets scorekeeper on new environment
        """
        self.ambulance = {
            "zombie": 0,
            # "injured": 0,
            "healthy": 0
        }
        self.scorekeeper = {
            "killed": 0,
            "saved": 0,
        }
        self.remaining_time = int(self.shift_len)  # minutes
        
        self.all_logs = []
        self.logger = []
    
    def log(self, humanoid, action):
        """
        logs current action taken against a humanoid
        
        humanoid : the humanoid presented
        action : the action taken
        """
        self.logger.append({"humanoid_class": humanoid.state,
                            "humanoid_fp": humanoid.fp,
                            "humanoid_probs": humanoid.probability,
                            "humanoid_job": humanoid.job,
                            "action": action,
                            "remaining_time": self.remaining_time,
                            "capacity": self.get_current_capacity(),
                            })
        
    def save_log(self, mode, diff=None):
        """
        Saves a single log.csv file containing the actions that were taken,and the humanoids presented at the time. 
        Note: will overwrite previous logs
        """

        if mode == 'player':
            fp = 'data_logs_players'
            current_num_files = next(os.walk(fp))[2]
            run_num = len(current_num_files)
        elif mode == 'rl':
            fp = 'data_logs_RL'
            current_num_files = next(os.walk(fp))[2]
            run_num = len(current_num_files)

        if len(self.logger) > 0:
            self.all_logs.append(self.logger)
        logs = []
        for i, log in enumerate(self.all_logs):
            log = pd.DataFrame(log)
            log['local_run_id'] = i
            logs.append(log)
        logs = pd.concat(logs, ignore_index=True)

        if mode == "player":
            log = f'{fp}/log_{run_num}_{diff}.csv'
            logs.to_csv(log)
        elif mode == "rl":
            log = f'{fp}/log_{run_num}_{diff}.csv'
            logs.to_csv(log)
        else:
            log = f'log.csv'
            logs.to_csv(log)

        with open(log, mode='a') as file:
            file.write("Killed: " + str(self.scorekeeper["killed"]) + " Saved: " + str(self.scorekeeper["saved"]))
    def save(self, humanoid):
        """
        saves the humanoid, applies serum on zombie if available
        updates scorekeeper
        """
        self.log(humanoid, 'save')
        self.carrying.append(humanoid)
        
        self.remaining_time -= ActionCost.SAVE.value
        if humanoid.is_zombie():
            if self.serum > 0:
                humanoid.set_human()
                self.ambulance["healthy"] += 1
                self.serum -= 1

            else:
                self.ambulance["zombie"] += 1
        # elif humanoid.is_injured():
        #     self.ambulance["injured"] += 1
        else:
            self.ambulance["healthy"] += 1
        

    def squish(self, humanoid):
        """
        squishes the humanoid
        updates scorekeeper
        """
        self.log(humanoid, 'squish')
        
        self.remaining_time -= ActionCost.SQUISH.value
        if humanoid.is_healthy():
            self.scorekeeper["killed"] += 1


    def skip(self, humanoid):
        """
        skips the humanoid
        updates scorekeeper
        """
        self.log(humanoid, 'skip')
        
        self.remaining_time -= ActionCost.SKIP.value
        # if humanoid.is_injured():
        #     self.scorekeeper["killed"] += 1
        

    def scram(self, humanoid = None):
        """
        scrams
        updates scorekeeper
        """
        if humanoid:
            self.log(humanoid, 'scram')
        

        self.remaining_time -= ActionCost.SCRAM.value
        if self.ambulance["zombie"] > 0:
            self.scorekeeper["killed"] += self.ambulance["healthy"]
        else:
            self.scorekeeper["saved"] += self.ambulance["healthy"]
            self.apply_all_job_buffs()


        self.ambulance["zombie"] = 0
        # self.ambulance["injured"] = 0
        self.ambulance["healthy"] = 0
       
                
        self.carrying = []

    def reveal(self, humanoid):
        
        if humanoid.revealedd() or self.diff == "easy":
            return
        
        "shows the occupation of the current human/zombie"
        self.log(humanoid, 'reveal')

        self.remaining_time -= ActionCost.REVEAL.value
        humanoid.reveals()
    
    # add to remaining time 
    def apply_engineer_buff(self, multiplier):
        self.remaining_time+=JobBaseEffect.ENGINEER.value*multiplier
        
    # subtract from remaining time
    def apply_imposter_buff(self, multiplier):
        self.remaining_time-=JobBaseEffect.IMPOSTER.value*multiplier
    
    # for each doctor in ambulance, add one serum
    def apply_doctor_buff(self, multiplier):
        if (multiplier*100) > random.randint(0, 100):
            self.serum += 1
    
    # if there is a thug present in the ambulance, each person has a 50% chance of dyind
    def apply_thug_buff(self):
        for victim in self.carrying:
            if victim.get_job()!="thug":
                if random.random() < .5:
                    self.scorekeeper["killed"]+=1
                    self.scorekeeper["saved"]-=1
            
    
    # applies all job-related buffs, which are only valid if the person is healthy
    def apply_all_job_buffs(self):
        job_counts = Counter(person.get_job() for person in self.carrying if person.is_healthy())

        pessimist_multiplier = 1
        for i in range(job_counts['pessimist']):
            pessimist_multiplier*= (1-JobBaseEffect.PESSIMIST.value)
    
        for _ in range(job_counts["doctor"]):
            self.apply_doctor_buff(pessimist_multiplier)

        for _ in range(job_counts["engineer"]):
            self.apply_engineer_buff(pessimist_multiplier)
        
        for _ in range(job_counts["imposter"]):
            self.apply_imposter_buff(pessimist_multiplier)
        
        for _ in range(job_counts["thug"]):
            self.apply_thug_buff()

        return
    
    def available_action_space(self):
        """
        returns available action space as a list of bools
        """
        action_dict = {s.value:True for s in ActionState}
        if self.remaining_time <= 0:
            action_dict['save'] = False
            action_dict['squish'] = False
            action_dict['skip'] = False
            action_dict['reveal'] = False
        if self.at_capacity():
            action_dict['save'] = False
        if len(self.logger) > 0 and self.logger[-1]['action'] == 'reveal':
            action_dict['reveal'] = False
        if self.diff == "easy":
            action_dict['reveal'] = False
        return [action_dict[s.value] for s in ActionState]
        
    # do_action or return false if not possible
    def map_do_action(self, idx, humanoid):
        """
        does an action on a humanoid. Intended for RL use.
        
        idx : the action index 
        """
        if idx == 0:
            if self.remaining_time <= 0 or self.at_capacity():
                return False
            self.save(humanoid)
        elif idx == 1:
            if self.remaining_time <= 0:
                return False
            self.squish(humanoid)
        elif idx == 2:
            if self.remaining_time <= 0:
                return False
            self.skip(humanoid)
        elif idx == 3:
            self.scram(humanoid)
        elif idx == 4:
            self.reveal(humanoid)
        else:
            raise ValueError("action index range exceeded")
        return True
        
    def get_cumulative_reward(self):
        """
        returns cumulative reward (current score)
        Note: the score can be denoted as anything, not set in stone
        """
        killed = self.scorekeeper["killed"]
        saved = self.scorekeeper["saved"] 
        if self.ambulance["zombie"] > 0:
            killed += self.ambulance["healthy"]
        else:
            saved += self.ambulance["healthy"]
        return saved - killed

    def get_current_capacity(self):
        return sum(self.ambulance.values())

    def at_capacity(self):
        return sum(self.ambulance.values()) >= self.capacity

    def get_score(self):
        self.scram()
        return self.scorekeeper
    
    @staticmethod
    def get_action_idx(class_string):
        return MAP_ACTION_STR_TO_INT[class_string]
    
    @staticmethod
    def get_action_string(class_idx):
        return MAP_ACTION_INT_TO_STR[class_idx]
    
    @staticmethod
    def get_all_actions():
        return MAP_ACTION_INT_TO_STR
