from gameplay.enums import State
import random

MAP_CLASS_STR_TO_INT = {s.value:i for i,s in enumerate(State)}
MAP_CLASS_INT_TO_STR = [s.value for s in State]

class Humanoid(object):
    """
    Are they a human or a zombie??? What probability?
    """
    
    def __init__(self, fp, state, job_probs):
        self.fp = fp
        self.probability = job_probs  # probability is a dictionary of floats (0-1) representing probabilities of each job class
        self.state = state  # human or zombie
        self.job = self.assign_class(job_probs)

    # returns a job class based on assigned probabilities
    def assign_class(self, job_probs):
        rand_num = random.random()
        total = 0.0
        for job, prob in job_probs.items():
            total+=prob
            if rand_num <= total:
                return job
        return None

    def is_zombie(self):
        return self.state == State.ZOMBIE.value

    def is_injured(self):
        return self.state == State.INJURED.value

    def is_healthy(self):
        return self.state == State.HEALTHY.value

    def is_corpse(self):
        return self.state == State.CORPSE.value
    
    @staticmethod
    def get_state_idx(class_string):
        return MAP_CLASS_STR_TO_INT[class_string]
    
    @staticmethod
    def get_state_string(class_idx):
        return MAP_CLASS_INT_TO_STR[class_idx]
    
    @staticmethod
    def get_all_states():
        return MAP_CLASS_INT_TO_STR

