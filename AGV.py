class AGV:
    #variabili comuni alle istanze della clase
    time = 1
    state = "Free"
    path = []
    goal = []

    #costruttore
    def __init__(self, pos):
        #variabili che cambiano per ogni istanza
        self.pos = pos

    def get_X(self):
        return self.pos[0]

    def get_Y(self):
        return self.pos[1]

'''
    #metodo
    def add_path(self, step):
        self.path.append(step)


#---------------------------
#           MAIN
#---------------------------

x = AGV([0,0],[5,5])

#accedere al valore dei parametri

print x.init_state
print "-----------"
print x.pos
print "-----------"

#chiamare i metodi
x.add_path(8)
x.add_path(4)
x.add_path(12)

print x.path
'''
