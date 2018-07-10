import scipy as sp
def envir_configuration(width, height):
    envir = sp.zeros([height, width])
    #Wall
    #wall_x = [5] * 30
    #wall_y = [range(0,30)]

    wall_x = list(range(8, 12))*35 + list(range(18, 22))*35 + list(range(28, 32))*35 + list(range(38, 42))*35
    wall_y = [range(10,45)] * 16
    for x in wall_x:
        for y in wall_y:
            envir[y,x] = 0.01
    #Gate
    envir[0, 9:13] = 0.02
    envir[0, 23:27] = 0.02
    envir[0, 37:41] = 0.02

    return envir

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
