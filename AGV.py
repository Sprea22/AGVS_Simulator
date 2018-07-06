import numpy as np

class AGV:
    #variabili comuni alle istanze della clase
    state = "Free"
    path = []
    goal = []
    gate = []

    #costruttore
    def __init__(self, pos):
        #variabili che cambiano per ogni istanza
        self.pos = pos

    def get_X(self):
        return self.pos[0]

    def get_Y(self):
        return self.pos[1]

    def get_next_goal(self):
        if(self.goal != [] and self.goal[0] != [0,0]):
            return self.goal[0]
        else:
            return []

    def update_envir(self, envir):
        print("POSITION |", self.pos)
        print("PATH |", self.path)
        print("GOAL |", self.goal)

        envir[self.pos[::-1]] = 0.02

        if(len(self.path) > 0):
            envir[self.path[0][::-1]] = 0.03
            if(len(self.path) > 1):
                envir[self.path[1][::-1]] = 0.03

        if(len(self.goal) != 0):
            envir[self.goal[0][::-1]] = 0.04
        return envir
