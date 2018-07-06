
def load(state):
    if(state == "Ongoing"):
        return "Loading"
    if(state == "Loading"):
        return "Returning"

def unload(state, goal):
    if(state == "Returning"):
        return "Unloading"
    if(state == "Unloading" and len(goal)==0):
        return "Free"
    else:
        return "Next_Goal"
