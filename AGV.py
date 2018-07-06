import numpy as np
from Navigation import navigation
import random as rd
import randomcolor as rc

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
        rand_color = rc.RandomColor()
        self.color = rand_color.generate()

    def get_X(self):
        return self.pos[0]

    def get_Y(self):
        return self.pos[1]

    def get_intent(self):
        return self.path[0]

    def get_next_goal(self):
        if(self.goal != [] and self.goal[0] != [0,0]):
            return self.goal[0]
        else:
            return []

    def update_envir(self, envir):
        envir[self.pos[::-1]] = 0.02

        if(len(self.path) > 0):
            envir[self.path[0][::-1]] = 0.03

            #if(len(self.path) > 1):
            #    envir[self.path[1][::-1]] = 0.03

        if(len(self.goal) != 0):
            envir[self.goal[0][::-1]] = 0.04
        return envir

    def conflict_handler(self, envir):
        print(self.path[0], "|", envir[self.path[0]] )
        if(envir[self.path[0]] != 0):
            print("ESGHERE")
            envir[self.path[0]] = 0.01
            if(len(self.path[1]) != 0):
                conflict_path = navigation(envir, self.pos, self.path[1])
                self.path = conflict_path[1:len(conflict_path)-1] + self.path[1:]
            else:
                self.path = [self.pos] + self.path
        return self.path
