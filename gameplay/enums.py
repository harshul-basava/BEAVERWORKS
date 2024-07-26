from enum import Enum


class State(Enum):
    ZOMBIE = "zombie"
    HEALTHY = "healthy"

class ActionState(Enum):
    SAVE = 'save'
    SQUISH = 'squish'
    SKIP = 'skip'
    SCRAM = 'scram'
    REVEAL = 'reveal'
    
class ActionCost(Enum):
    SAVE = 30
    SQUISH = 15
    SKIP = 20
    SCRAM = 50
    REVEAL = 30

class Job(Enum):
    DOCTOR = "doctor"
    ENGINEER = "engineer"
    THUG = "thug"
    NORMAL = "normal"
    FATTY = "fatty"
    PESSIMIST = "pessimist"

class JobBaseEffect(Enum):
    ENGINEER = 45
    FATTY = 60
    PESSIMIST = 0.4