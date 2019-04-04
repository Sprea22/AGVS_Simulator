import numpy as np
import random as rd
from Navigation import navigation
from Environment_Conf import goals_location
from Environment_Conf import gates_location

class AGV:
    # agent default variables initialization
    state = "Free"
    client = ''
    path = []
    gate = -1
    goal = (-1, -1)
    info_order = -1
    # Just if it's BT2, otherwise []
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

    def get_neighborhood(self, envir):
        results = []
        curr_position = self.get_pos()[::-1]
        for x_t in [-1, 0, +1]:
            for y_t in [-1, 0, +1]:
                #
                # ERRORE QUANDO IL CONFLICT è SUL BORDO DELLA MATRICE
                # QUINDI BISOGNA CONTROLLARE CHE LA POSIZIONE (SOMMATA) ESISTA
                #
                try:
                    position = envir[curr_position[0] + x_t, curr_position[1] + y_t]
                    if(position == 15 or position == 5):
                        results.append((curr_position[0] + x_t, curr_position[1] + y_t))
                except IndexError:
                    pass
        return results

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
        gates = gates_location()
        goals = goals_location()
        # Data stats: no conflict
        conflict_bool = 0
        # The following three values are used to restore the "temp walls" created
        # around the current AGV
        x = sum(sum(envir))
        envir_temp = np.copy(envir)

        if(envir_temp[self.path[0]] == 15):
            # Data stats: conflict and wait
            conflict_bool = 1

            neighborhood = self.get_neighborhood(envir_temp)
            for pos in neighborhood:
                envir_temp[pos] = 0.01

            # If the AGV path is longer than 1, you're not reaching the goal so
            # you can try to recalculate the path.
            if(len(self.path) > 1):
                conflict_bool = 2
                # Calculate how many times a single AGV can recalculate the conflict path
                conflict_count = 0
                conflict_count_b = 0
                #if(len(self.path) > 3):
                #    conf_calc_max =
                #else:
                conf_calc_max = len(self.path)
                # Initialize the conflict path to empty path []
                conflict_path = None
                conflict_path_b = None
                # Calculate the conflict path until the bool is trues
                while(conflict_count < conf_calc_max and conflict_path == None):
                    conflict_path = navigation(envir_temp, self.pos, self.path[conflict_count])

                    if(conflict_path is not None):
                        if(envir_temp[conflict_path[0]] == 15):
                            envir_temp[conflict_path[0]] = 0.01
                            conflict_path = None
                            conflict_count = conflict_count + 1
                        else:
                            if(conflict_path[0] in gates or conflict_path[0] in goals):
                                conflict_path_b = conflict_path
                                conflict_count_b = conflict_count
                                envir_temp[conflict_path[0]] = 0.01
                                conflict_path = None
                                conflict_count = conflict_count + 1
                            else:
                                break
                    else:
                        conflict_count = conflict_count + 1

                if(conflict_path is None):
                    if(conflict_path_b is None):
                        conflict_bool = 1
                        self.path = [self.pos] + self.path
                    else:
                        self.path = conflict_path_b + self.path[conflict_count_b:]
                else:
                    self.path = conflict_path + self.path[conflict_count:]
            # It means that your next step is the goal. Just wait
            else:
                self.path = [self.pos] + self.path
        return self.path, conflict_bool
