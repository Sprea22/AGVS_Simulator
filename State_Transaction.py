
def state_transaction(state, goal):
    if(state == "Free" and len(goal) != 0):
        return "To_Goal"

    elif(state == "Free" and len(goal) == 0):
        return "To_Home"

    elif(state == "To_Goal"):
        return "Loading"

    elif(state == "To_Gate"):
        return "Unloading"

    elif(state == "To_Home"):
        return "Home"

    elif(state == "To_WaitingPoint" and not(goal)):
        return "To_Gate"

    elif(state == "To_WaitingPoint" and goal):
        return "Wait"

    elif(state == "Loading" and goal != (-1, -1)):
        return "To_Gate"

    elif(state == "Loading" and goal == (-1, -1)):
        return "To_WaitingPoint"

    elif(state == "Unloading" and len(goal) == 0):
        return "Free"

    elif(state == "Unloading" and len(goal) != 0):
        return "To_Goal"

    elif(state == "Home"):
        return "--------------------------------"

    elif(state == "Wait"):
        return "To_Gate"
