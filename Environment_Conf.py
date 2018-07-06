import scipy as sp
def envir_configuration(width, height):
    envir = sp.zeros([height, width])
    return envir

'''
    # Building the walls in the environment
    for row in range(10, 20):
        for column in range(10, 20):
            envir[row,column] = 0.01
    for row in range(30, 40):
        for column in range(30, 40):
            envir[row,column] = 0.01
'''
