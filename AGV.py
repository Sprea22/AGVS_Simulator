import numpy as np
import random as rd
from Navigation import navigation

class AGV:
    # agent default variables initialization
    state = "Free"
    client = ''
    path = []
    gate = -1
    info_order = -1
    goal = (-1, -1)
    articles_priority = []

    # constructor
    def __init__(self, pos, color, id, articles_priority):
        # agent default initialization
        self.id = id
        self.pos = pos
        self.init_pos = pos
        self.color = color
        self.articles_priority = articles_priority


    def get_pos(self):
        return self.pos[1], self.pos[0]

    def get_intent(self):
        return self.path[0]


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
        # Data stats: no conflict
        conflict_bool = 0
        # The following three values are used to restore the "temp walls" created
        # around the current AGV
        temp_reset = []
        val_temp_reset = []
        path_okay = False
        pos_temp = self.path[0]
        envir_temp = envir[pos_temp]
        if(envir[self.path[0]] == 15):
            # Data stats: conflict and wait
            conflict_bool = 1
            envir[self.path[0]] = 0.01
            if(len(self.path) > 1):
                # Data stats: conflict and path change
                conflict_bool = 2
                conflict_path = navigation(envir, self.pos, self.path[1])
                ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
                while not(path_okay):
                    if(envir[conflict_path[0]] == 15):
                        temp_reset.append(conflict_path[0])
                        val_temp_reset.append(envir[conflict_path[0]])
                        envir[conflict_path[0]] = 0.01
                        conflict_path = navigation(envir, self.pos, self.path[1])
                    else:
                        path_okay = True
                ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
                self.path = conflict_path[0:len(conflict_path)-1] + self.path[1:]
            else:
                self.path = [self.pos] + self.path

        ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
        for i in range(0, len(temp_reset)):
            envir[temp_reset[i]] = val_temp_reset[i]
        ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
        envir[pos_temp] = envir_temp
        return self.path, conflict_bool
