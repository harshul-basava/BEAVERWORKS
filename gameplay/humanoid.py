from gameplay.enums import State, Job
import random

MAP_CLASS_STR_TO_INT = {s.value:i for i,s in enumerate(State)}
MAP_CLASS_INT_TO_STR = [s.value for s in State]

MAP_JOB_STR_TO_INT = {j.value: i for i, j in enumerate(Job)}
MAP_JOB_INT_TO_STR = [j.value for j in Job]

class Humanoid(object):
    """
    Are they a human or a zombie??? What job??
    """
    
    def __init__(self, fp, state, job_probs=None):
        self.fp = fp
        self.probability = self.create_job_probs()  # probability is a dictionary of floats (0-1) representing probabilities of each job class
        self.state = state  # human or zombie
        self.job = self.assign_class(self.probability)
    
    # creates probabilities for jobs
    def create_job_probs(self):
        probs = {}
        doctorProb = random.randint(0, 100)
        engineerProb = random.randint(0, 100-doctorProb)
        normalProb = random.randint(0,100-doctorProb-engineerProb)
        thugProb = random.randint(0,100-doctorProb-engineerProb-normalProb)
        fattyProb = 100-doctorProb-engineerProb-normalProb-thugProb
        probs['doctor'] = doctorProb
        probs['engineer'] = engineerProb
        probs['normal'] = normalProb
        probs['thug'] = thugProb
        probs['fatty'] = fattyProb
        return probs

    # returns a job class based on assigned probabilities
    def assign_class(self, job_probs):
        if job_probs is not None:
            rand_num = random.randint(0, 100)
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
    
    def get_job(self):
        return self.job.value
    
    @staticmethod
    def get_state_idx(class_string):
        return MAP_CLASS_STR_TO_INT[class_string]
    
    @staticmethod
    def get_state_string(class_idx):
        return MAP_CLASS_INT_TO_STR[class_idx]
    
    @staticmethod
    def get_job_idx(job_string):
        return MAP_JOB_STR_TO_INT[job_string]
    
    @staticmethod
    def get_job_string(job_idx):
        return MAP_JOB_INT_TO_STR[job_idx]
    
    @staticmethod
    def get_all_states():
        return MAP_CLASS_INT_TO_STR
    
    @staticmethod
    def get_all_jobs():
        return MAP_JOB_INT_TO_STR


