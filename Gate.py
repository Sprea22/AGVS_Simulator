
class Gate:
    # constructor
    def __init__(self, id, loc_lp1, loc_lp2, loc_lp3, queue_loc):
        self.id = id
        self.loc_lp1 = loc_lp1
        self.loc_lp2 = loc_lp2
        self.loc_lp3 = loc_lp3
        self.queue_loc = queue_loc
        self.AGV_queue = []
        self.lps_locations = [loc_lp1, loc_lp2, loc_lp3]
        self.lps = [-1, -1, -1]
        self.lps_counters = [0, 0, 0]

    def lp_hold(self, ag):
        for idx, val in enumerate(self.lps):
            if(self.lps_counters[idx] < 5 and ag.info_order == val):
                self.lps_counters[idx] = self.lps_counters[idx] + 1
                return self.lps_locations[idx], self.lps_counters
        for idx, val in enumerate(self.lps):
            if(val == -1):
                self.lps[idx] = ag.info_order
                self.lps_counters[idx] = 1
                return self.lps_locations[idx], self.lps_counters
        return (-1, -1), self.lps_counters

    def lp_free(self, ag):
        # In this method the AGV's order is done. (status == 2)
        for idx, loc in enumerate(self.lps_locations):
            # If the AGV's is the last one in that gate, let it be free
            if(self.lps_counters[idx] == 0 and ag.info_order == self.lps[idx]):
                self.lps[idx] = -1
        return self

    # Ritornare anche la posizione del LP corretto
    def lp_available(self, ag):
        if(self.lps[0] == -1 or (ag.info_order == self.lps[0] and self.lps_counters[0] < 5)):
            return True
        elif(self.lps[1] == -1  or (ag.info_order == self.lps[1] and self.lps_counters[1] < 5)):
            return True
        elif(self.lps[2] == -1  or (ag.info_order == self.lps[2] and self.lps_counters[2] < 5)):
            return True
        else:
            return False
