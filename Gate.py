
class Gate:
    lp_one = -1
    lp_two = -1
    lp_three = -1
    AGV_queue = []

    # constructor
    def __init__(self, id, loc_lp1, loc_lp2, loc_lp3, queue_loc):
        self.id = id
        self.loc_lp1 = loc_lp1
        self.loc_lp2 = loc_lp2
        self.loc_lp3 = loc_lp3
        self.queue_loc = queue_loc

    # Ritornare anche la posizione del LP corretto
    def lp_hold(self, ag):
        if(ag.info_order == self.lp_one):
            self.lp_one = ag.info_order
            return self.loc_lp1

        if(ag.info_order == self.lp_two):
            self.lp_two = ag.info_order
            return self.loc_lp2

        if(ag.info_order == self.lp_three):
            self.lp_three = ag.info_order
            return self.loc_lp3

        if(self.lp_one == -1):
            self.lp_one = ag.info_order
            return self.loc_lp1

        elif(self.lp_two == -1):
            self.lp_two = ag.info_order
            return self.loc_lp2

        elif(self.lp_three == -1):
            self.lp_three = ag.info_order
            return self.loc_lp3

        else:
            return (-1,-1)

    # Ritornare anche la posizione del LP corretto
    def lp_available(self, ag):
        if(self.lp_one == -1 or ag.info_order == self.lp_one):
            return True
        elif(self.lp_two == -1  or ag.info_order == self.lp_two):
            return True
        elif(self.lp_three == -1  or ag.info_order == self.lp_three):
            return True
        else:
            return False

    def lp_free(self, pos):
        if(self.loc_lp1 == pos):
            self.lp_one = -1
        elif(self.loc_lp2 == pos):
            self.lp_two = -1
        elif(self.loc_lp3 == pos):
            self.lp_three = -1
        else:
            print("Error - The gates are free")
            return "Error - The gates are free"
        return self
