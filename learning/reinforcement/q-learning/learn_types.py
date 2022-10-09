from ctypes import *
from enum import IntEnum
import random
from re import A 

STATES = 1024
#FEATURES = 20
ACTIONS = 2

class RewardCtx(Structure):
    _fields_ = [('done', c_int),
                ('exit', c_int),
                ('moved', c_int),
                ('risky', c_int),
                ('moves', c_double),
                ('delay', c_int),
                ('crash', c_int),
                ('in', c_int)
                ]


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


class Learn(Structure):
    _fields_ = [('learn', c_int),   # Are learning
                ('start', c_int),   # Is the start
                ('test', c_int),    # Are we testing 

                ('gamma', c_double), 
                ('epsilon', c_double),
                ('alpha', c_double),
                
                ('smodel', POINTER(QTable)), # Model 
                ('mrow', c_int),             # Model Row
                ('pmrow', c_int),            # Previous model row

                ('segment', c_int),
                ('episode', c_int),
                ('episodes', c_int),

                ('epi_reward', c_double),
                ('avg_reward', c_double),
                ('seg_avg_reward', c_double),

                ('profile', c_int),
                ('rctx', RewardCtx),

                ('prev_reward', c_double),
                ('prev_action', c_int)
                ]



