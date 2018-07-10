import scipy as sp
def envir_configuration(width, height):
    envir = sp.zeros([height, width])

    ################################
    # WALLS and GATE configuration #
    ################################
    # Set WALLS in the environment
    wall_x = list(range(8, 12))*35 + list(range(18, 22))*35 + list(range(28, 32))*35 + list(range(38, 42))*35
    wall_y = [range(10,45)] * 16
    # Set the matrix value to 0.01 if it's a WALL
    for x in wall_x:
        for y in wall_y:
            envir[y,x] = 0.01

    # Set GATES in the environment
    gate_x =  list(range(9, 14)) + list(range(23, 28)) + list(range(37, 42))
    gate_y = [0] * len(gate_x)
    # Set the matrix value to 0.02 if it's a GATE
    for x in gate_x:
        for y in gate_y:
            envir[y,x] = 0.02

    return envir, wall_x, wall_y, gate_x, gate_y

def envir_reset(ag, envir):
    if(envir[ag.pos] == 15):
        envir[ag.pos] =  0
    if(len(ag.path) != 0):
        if(envir[ag.path[0]] == 5):
            envir[ag.path[0]] = 0
    #if(len(ag.goal) != 0):
    #    envir[ag.goal[0]] = 0
    return envir

#######################################################################
###### Update Environment method ######
#######################################################################
# INPUT: self = AGV, envir = environement
# Set the environment value to 15 for the current AGV position
# If the AGV has an intent
    # Set the environment value to 5

def update_envir(self, envir):
    envir[self.pos] = 15

    if(len(self.path) > 0):
        envir[self.path[0]] = 5

    # If you decomment this code, you set the environment value
    # for each AGV goal but you have to handle the Conflict Handler method
    # otherwise the AGV will not access a goal location.

    #if(len(self.goal) != 0):
    #    envir[self.goal[0]] = 0.5
    return envir
