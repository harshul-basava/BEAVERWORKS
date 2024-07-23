from enum import Enum


class State(Enum):
    ZOMBIE = "zombie"
    HEALTHY = "healthy"
    # INJURED = "injured"
    # CORPSE = "corpse"

class ActionState(Enum):
    SAVE = 'save'
    SQUISH = 'squish'
    SKIP = 'skip'
    SCRAM = 'scram'
    REVEAL = 'reveal'
    
class ActionCost(Enum):
    SAVE = 30
    SQUISH = 5
    SKIP = 15
    SCRAM = 120
    REVEAL = 20

class Job(Enum):
    DOCTOR = "doctor"
    ENGINEER = "engineer"
    THUG = "thug"
    NORMAL = "normal"
    FATTY = "fatty"
    PESSIMIST = "pessimist"
