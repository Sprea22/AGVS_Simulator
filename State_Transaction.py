def state_transaction(state, goal):
    map_transaction = {
    ("Free", goal != (-1, -1)) : "To_Goal",
    ("Free", goal == (-1, -1)) : "To_Home",
    ("To_Goal", goal) : "Loading",
    ("To_Gate", goal) : "Unloading",
    ("To_Home", goal) : "Home",
    ("To_WaitP", not(goal)) : "To_Gate",
    ("To_WaitP", goal) : "Wait",
    ("Loading", goal != (-1, -1)) : "To_Gate",
    ("Loading", goal == (-1, -1)) : "To_WaitP",
    ("Unloading", goal) : "Free",
    ("Home", goal) : "----------------",
    ("Wait", goal) : "To_Gate",
    }

    for i in map_transaction.keys():
        if(type(i[1]) != type(True)):
            if(i[0] == state):
                return map_transaction[i]
        else:
            if(i[0] == state and i[1] == True):
                return map_transaction[i]
