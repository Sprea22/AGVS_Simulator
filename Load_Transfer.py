
def load(state):
    if(state == "Ongoing"):
        return "Loading"
    if(state == "Loading"):
        return "Returning"
    if(state == "Loading_FullGate"):
        return "Returning_Wait"
    if(state == "Returning_Wait" or state == "Wait"):
        return "Returning"

def unload(state, goal):
    if(state == "Returning"):
        return "Unloading"
    if(state == "Unloading" and len(goal)==0):
        return "Free"
    if(state == "Returning_Wait"):
        return "Wait"
    else:
        return "Next_Goal"
