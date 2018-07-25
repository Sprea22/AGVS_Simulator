import scipy as sp
import numpy as np
def envir_configuration(width, height):
    envir = sp.zeros([height, width])

    ################################
    # WALLS, OFFICE, GATE configuration #
    ################################

    # Set WALLS
    wall_x = np.array(list(range(5, 7))* 27 + list(range(10, 12)) * 27 + list(range(15, 17))* 27 + list(range(20, 22)) * 27 +  list(range(25, 27))* 27 + list(range(30, 32)) * 27 + list(range(35, 37))* 27 + list(range(40, 42)) * 27)
    wall_y = np.array([range(13,40)] * 16).flatten('K')

    # Set OFFICES
    office_x = list(range(0,24)) + [24] * 10
    office_y = [9]*24 + list(range(0,10))

    # Set GOAL
    goals = [(18,5),(24,6),(30,5),(36,6)
            ,(18,10),(24,11),(30,10),(36,11)
            ,(18,15),(24,16),(30,15),(36,16)
            ,(18,20),(24,21),(30,20),(36,21)
            ,(18,25),(24,26),(30,25),(36,26)
            ,(18,30),(24,31),(30,30),(36,31)
            ,(18,35),(24,36),(30,35),(36,36)
            ,(18,40),(24,41),(30,40),(36,41)]

    # Set the matrix value to 0.01 if it's a WALL or OFFICE
    for x in wall_x:
        for y in wall_y:
            envir[y,x] = 0.01

    for x in office_x:
        for y in office_y:
            envir[y,x] = 0.01

    for i in range(0, 400):  #400 = 432 - 32 goals
        if((wall_y[i], wall_x[i]) in goals):
            wall_x = np.delete(wall_x, i)
            wall_y = np.delete(wall_y, i)

    for p in goals:
        envir[p] = 0

    # Set GATES in the environment
    gate_x =  list(range(31, 34)) + list(range(37, 40)) + list(range(43,46))
    gate_y = [0] * len(gate_x)
    # Set the matrix value to 0.02 if it's a GATE
    for x in gate_x:
        for y in gate_y:
            envir[y,x] = 0.02

    return envir, wall_x, wall_y, gate_x, gate_y, office_x, office_y

def envir_reset(ag, envir):
    #if(envir[ag.pos] == 15):
    envir[ag.pos] =  0
    #if(len(ag.path) != 0):
    #    if(envir[ag.path[0]] == 5):
    #        envir[ag.path[0]] = 0
    return envir


def update_envir(self, envir):
    envir[self.pos] = 15

    if(len(self.path) > 0):
        if(envir[self.path[0]] != 15):
            envir[self.path[0]] = 5
    return envir
