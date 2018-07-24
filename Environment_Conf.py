import scipy as sp
def envir_configuration(width, height):
    envir = sp.zeros([height, width])

    ################################
    # WALLS, OFFICE, GATE configuration #
    ################################

    # Set WALLS in the environment
    wall_x = list(range(5, 7))* 27 + list(range(10, 12)) * 27 + list(range(15, 17))* 27 + list(range(20, 22)) * 27 +  list(range(25, 27))* 27 + list(range(30, 32)) * 27 + list(range(35, 37))* 27 + list(range(40, 42)) * 27

    wall_y = [range(13,40)] * 16

    #wall_x =
    #wall_y = [range(12,40)] * BO

    # Set OFFICES in the environment
    office_x = list(range(0,24)) + [24] * 9
    office_y = [8]*24 + list(range(0,9))

    # Set the matrix value to 0.01 if it's a WALL or OFFICE
    for x in wall_x:
        for y in wall_y:
            envir[y,x] = 0.01

    for x in office_x:
        for y in office_y:
            envir[y,x] = 0.01


    # Set GATES in the environment
    gate_x =  list(range(31, 34)) + list(range(37, 40)) + list(range(43,46))
    gate_y = [0] * len(gate_x)
    # Set the matrix value to 0.02 if it's a GATE
    for x in gate_x:
        for y in gate_y:
            envir[y,x] = 0.02

    return envir, wall_x, wall_y, gate_x, gate_y, office_x, office_y
# Initilizing the gate objects
    gates.append(Gate(0, (0,31), (0,32), (0,33), (3, 30)))
    gates.append(Gate(1, (0,37), (0,38), (0,39), (3, 39)))
    gates.append(Gate(2, (0,43), (0,44), (0,45), (3, 46)))
