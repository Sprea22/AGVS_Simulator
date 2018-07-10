import numpy as np
from Navigation import navigation
import random as rd
import randomcolor as rc

class AGV:
    #variabili comuni alle istanze della clase
    state = "Free"
    path = []
    goal = []
    gate = []



    #costruttore
    def __init__(self, pos, color):
        #variabili che cambiano per ogni istanza
        self.pos = pos
        #rand_color = rc.RandomColor()
        #self.color = rand_color.generate()
        self.color = color

    def get_X(self):
        return self.pos[1]

    def get_Y(self):
        return self.pos[0]

    def get_intent(self):
        return self.path[0]

    def get_next_goal(self):
        if(self.goal != [] and self.goal[0] != [0,0]):
            return self.goal[0]
        else:
            return []



#######################################################################
###### Conflict Handler method ######
#######################################################################
# INPUT: self = AGV, envir = environement
# pos_temp variable allows to save the environment location that is going to be initialized as a temporary wall
# If the next step is not free (is not 0)
    # Set the next step as a wall (0.01)
    # If your next step is NOT the goal, recalculate the path considering the next step as a wall
        # OUTPUT: the path to avoid the wall ahead + the old path
    # If your next step is the goal, just wait
        # OUTPUT: the new path with the current position ahead
# reset the pos_temp environment location to free
    def conflict_handler(self, envir):
        pos_temp = self.path[0]

        if(envir[self.path[0]] != 0):
            envir[self.path[0]] = 0.01
            if(len(self.path) > 1):
                conflict_path = navigation(envir, self.pos, self.path[1])
                self.path = conflict_path[0:len(conflict_path)-1] + self.path[1:]
            else:
                self.path = [self.pos] + self.path

        envir[pos_temp] = envir[self.path[0]]
        return self.path
