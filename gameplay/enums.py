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
    SWAP = 'swap'
    
class ActionCost(Enum):
    SAVE = 15
    SQUISH = 5
    SKIP = 10
    SCRAM = 45
    REVEAL = 15
    SWAP = 30

class Job(Enum):
    DOCTOR = "doctor"
    ENGINEER = "engineer"
    THUG = "thug"
    NORMAL = "normal"
    FATTY = "fatty"
    PESSIMIST = "pessimist"
