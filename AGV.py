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
        gates = [(0,31), (0,32),(0,33), (0,37), (0,38),
                (0,39), (0,43), (0,44), (0,45)]
        goals = [(18,5),(24,6),(30,5),(36,6)
                ,(18,10),(24,11),(30,10),(36,11)
                ,(18,15),(24,16),(30,15),(36,16)
                ,(18,20),(24,21),(30,20),(36,21)
                ,(18,25),(24,26),(30,25),(36,26)
                ,(18,30),(24,31),(30,30),(36,31)
                ,(18,35),(24,36),(30,35),(36,36)
                ,(18,40),(24,41),(30,40),(36,41)]
        # Data stats: no conflict
        conflict_bool = 0
        # The following three values are used to restore the "temp walls" created
        # around the current AGV
        x = sum(sum(envir))
        envir_temp = np.copy(envir)
        if(envir_temp[self.path[0]] == 15):
            # Data stats: conflict and wait
            conflict_bool = 1
            envir_temp[self.path[0]] = 0.01
            # If the AGV path is longer than 1, you're not reaching the goal so
            # you can try to recalculate the path.
            if(len(self.path) > 1):
                # Data stats: conflict and path change
                conflict_bool = 2
                # Calculate how many times a single AGV can recalculate the conflict path
                conflict_count = 0
                #if(len(self.path) > 3):
                #    conf_calc_max =
                #else:
                conf_calc_max = len(self.path)
                # Initialize the conflict path to empty path []
                conflict_path = None
                # Calculate the conflict path until the bool is trues
                while(conflict_count < conf_calc_max and conflict_path == None):
                    conflict_path = navigation(envir_temp, self.pos, self.path[conflict_count])
                    if(conflict_path is not None):
                        if(envir_temp[conflict_path[0]] == 15 or conflict_path[0] in gates or conflict_path[0] in goals):
                            envir_temp[conflict_path[0]] = 0.01
                            conflict_count = conflict_count + 1
                        else:
                            break
                    else:
                        conflict_count = conflict_count + 1
                if(conflict_path is None):
                    self.path = [self.pos] + self.path
                    print("Stai fermo", self.path)
                else:
                    self.path = conflict_path + self.path[conflict_count:]
                    print("Cambia la tua path in", self.path)
            # It means that your next step is the goal. Just wait
            else:
                self.path = [self.pos] + self.path
        return self.path, conflict_bool
