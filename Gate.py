
class Gate:
    lp_one = 0
    lp_two = 0
    lp_three = 0
    AGV_queue = []

    # constructor
    def __init__(self, id, loc_lp1, loc_lp2, loc_lp3, queue_loc):
        self.id = id
        self.loc_lp1 = loc_lp1
        self.loc_lp2 = loc_lp2
        self.loc_lp3 = loc_lp3
        self.queue_loc = queue_loc

    # Ritornare anche la posizione del LP corretto
    def lp_hold(self):
        if(self.lp_one == 0):
            self.lp_one = 1
            return self.loc_lp1
        elif(self.lp_two == 0):
            self.lp_two = 1
            return self.loc_lp2
        elif(self.lp_three == 0):
            self.lp_three = 1
            return self.loc_lp3
        else:
            return (-1,-1)

    # Ritornare anche la posizione del LP corretto
    def lp_available(self):
        if(self.lp_one == 0):
            return True
        elif(self.lp_two == 0):
            return True
        elif(self.lp_three == 0):
            return True
        else:
            return False

    def lp_free(self, pos):
        if(self.loc_lp1 == pos):
            self.lp_one = 0
        elif(self.loc_lp2 == pos):
            self.lp_two = 0
        elif(self.loc_lp3 == pos):
            self.lp_three = 0
        else:
            print("Error - The gates are free")
            return "Error - The gates are free"
        return self
