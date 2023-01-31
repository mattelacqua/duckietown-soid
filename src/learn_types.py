from ctypes import *
from enum import IntEnum
import random
from re import A 

STATES = 1024
#FEATURES = 20
ACTIONS = 2

class QTable(Structure):
    _fields_ = [('qt', (c_float * ACTIONS) * STATES)]

    def __init__(self, model=None):
        if model:
            for i in range (0, STATES):
                for j in range (0, ACTIONS):
                    self.qt[i][j] = model[i][j]
        
        else:
            for i in range (0, STATES):
                for j in range (0, ACTIONS):
                    #self.qt[i][j] = random.random() # Init to random 0-1 value.
                    self.qt[i][j] = 0 # Init to 0


