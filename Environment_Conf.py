import scipy as sp
def envir_configuration(width, height):
    envir = sp.zeros([height, width])

    return envir
'''
    # Building the walls in the environment
    for row in range(10, 20):
        for column in range(11, 20):
            envir[row,column] = 0.01
    for row in range(30, 40):
        for column in range(30, 40):
            envir[row,column] = 0.01
'''
def envir_reset(ag, envir):
    if(envir[ag.pos] > 0):
        envir[ag.pos] = envir[ag.pos] - 15
    if(len(ag.path) != 0):
        envir[ag.path[0]] = envir[ag.path[0]] - 5
    #if(len(ag.goal) != 0):
    #    envir[ag.goal[0]] = 0
    return envir
