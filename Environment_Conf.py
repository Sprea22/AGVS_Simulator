import scipy as sp
import numpy as np

#####################################
# WALLS, OFFICE, GATE configuration #
#####################################

def envir_configuration(width, height):
    envir = np.zeros([height, width])

    goals = goals_location()
    office_locs = office_location()
    wall_locs = wall_location(goals)
    gates_locs = gates_location()
    charging_locs = charging_location()

    for x in range(0, width):
        for y in range(0, height):
            loc = (y,x)
            if(loc in gates_locs):
                envir[y][x] = 0.02
            elif(loc in goals):
                envir[y][x]  = 0
            elif(loc in wall_locs):
                envir[y][x]  = 0.01
            elif(loc in office_locs):
                envir[y][x] = 0.01
    return envir, gates_locs, wall_locs, office_locs, charging_locs

def envir_reset(ag, envir):
    if(envir[ag.pos] != 0.5):
        envir[ag.pos] =  0
    return envir

def update_envir(self, envir):
    envir[self.pos] = 15
    if(len(self.path) > 0):
        if(envir[self.path[0]] != 15):
            envir[self.path[0]] = 5
    return envir

##############################################################################################################################
### Map locations definition ###
##############################################################################################################################

def goals_location():
    goals = [(18,5),(24,6),(30,5),(36,6)
            ,(18,10),(24,11),(30,10),(36,11)
            ,(18,15),(24,16),(30,15),(36,16)
            ,(18,20),(24,21),(30,20),(36,21)
            ,(18,25),(24,26),(30,25),(36,26)
            ,(18,30),(24,31),(30,30),(36,31)
            ,(18,35),(24,36),(30,35),(36,36)
            ,(18,40),(24,41),(30,40),(36,41)]
    return goals

def gates_location():
    gates = [(0,31), (0,32),(0,33), (0,37), (0,38),
            (0,39), (0,43), (0,44), (0,45)]
    return gates

def charging_location():
    charging_x = range(0,48)
    charging_y = [42]*48
    charging_locs = [charging_loc for charging_loc in zip(charging_y, charging_x)]
    return charging_locs

def wall_location(goals):
    wall_x = np.array(list(range(5, 7))* 27 + list(range(10, 12)) * 27 + list(range(15, 17))* 27 + list(range(20, 22)) * 27 +  list(range(25, 27))* 27 + list(range(30, 32)) * 27 + list(range(35, 37))* 27 + list(range(40, 42)) * 27)
    wall_y = np.array([range(13,40)] * 16).flatten('K')

    # Delete the goals location from the walls location
    for i in range(0, len(wall_x) - len(goals)):  #400 = 432 - 32 goals
        if((wall_y[i], wall_x[i]) in goals):
            wall_x = np.delete(wall_x, i)
            wall_y = np.delete(wall_y, i)
    wall_locs = [wall_loc for wall_loc in zip(wall_y, wall_x)]
    return wall_locs

def office_location():
    office_x =  list(range(0,24)) + list(range(5, 11)) + list(range(12, 20)) + list(range(21,24)) + list(range(5, 11)) + list(range(12, 20)) + list(range(21,24)) + [5] * 8 + [16] * 8 + [24] * 10
    office_y = [9]*24 + [3]*17 + [5]*17 + list(range(0,4)) + list(range(6,10)) + list(range(0,4)) + list(range(6,10)) + list(range(0,10))
    office_locs = [office_loc for office_loc in zip(office_y, office_x)]
    return office_locs

def order_location(ind):
    map_locations = {   "PILE S" : (18,5),  "PILE ALTA VISIBILITA'" : (24,6),  "PILE L" : (30,5),  "PILE ARANCIO" : (36,6)
                    , "GIUBBETTO" : (18,10), "ELMETTO" : (24,11), "FELPA" : (30,10), "TUTA" : (36,11)
                    , "PANTALONE LAVORO S" : (18,15), "PANTALONE LAVORO M" : (24,16), "PANTALONE LAVORO L" : (30,15), "PANTALONE ARANCIO" : (36,16)
                    , "PANTALONE JEANS S" : (18,20), "PANTALONE JEANS M" : (24,21), "PANTALONE JEANS L" : (30,20), "PANTALONE" : (36,21)
                    , "SCARPA BASSA" : (18,25), "SCARPA BASSA STRONG" : (24,26), "MAGLIETTA" : (30,25), "CAMICIA" : (36,26)
                    , "SCARPA ALTA  HARD" : (18,30), "SCARPA ASFALTISTA" : (24,31), "SCARPA ALTA ASFALTISTA" : (30,30), "SCARPA ALTA SCOTLAND" :(36,31)
                    , "SCARPA ALTA INVERNALE S" : (18,35), "SCARPA ALTA INVERNALE M" : (24,36), "SCARPA ALTA INVERNALE L" : (30,35), "SCARPA ALTA INVERNALE XL" :(36,36)
                    , "SCARPA ALTA STONE S" : (18,40), "SCARPA ALTA STONE M" : (24,41), "SCARPA ALTA STONE L" : (30,40), "STIVALE" :(36,41)}

    for i in map_locations.keys():
        if(i == ind):
            return map_locations[i]
