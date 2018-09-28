
class Waiting_Point:
    # constructor
    def __init__(self, id, wait_poing_init):
        self.id = id
        self.waiting_locations = []
        x, y = wait_poing_init
        for j in [y, y+1, y+2]:
            for i in [x, x+1]:
                self.waiting_locations.append((i, j))
        self.waiting_availability = [0] * len(self.waiting_locations)
        self.waiting_agv = [-1] * len(self.waiting_locations)
        self.waiting_order = [-1] * len(self.waiting_locations)

    def free_spots(self):
        if(sum(self.waiting_availability) != len(self.waiting_availability)):
            number_free_spots = len(self.waiting_availability) - sum(self.waiting_availability)
            return number_free_spots
        else:
            return 0

    def hold_waiting_location(self, ag):
        if(sum(self.waiting_availability) != len(self.waiting_availability)):
            for idx, val in enumerate(self.waiting_availability):
                if(val == 0):
                    self.waiting_availability[idx] = 1
                    self.waiting_agv[idx] = ag.id
                    self.waiting_order[idx] = ag.info_order
                    return self, self.waiting_locations[idx], True

    def free_waiting_location(self, ag):
        #index_min_order_waiting = np.argmin(waiting_order[waiting_order != -1])
        for idx, val in enumerate(self.waiting_agv):
            if(self.waiting_agv[idx] == ag.id):
                self.waiting_agv[idx] = -1
                self.waiting_availability[idx] = 0
                self.waiting_order[idx] = -1
                return self, True
        print("Error: impossible to find position of the waiting location ", self.id)
        return self, False
