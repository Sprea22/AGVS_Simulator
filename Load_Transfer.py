
def load(state):
    if(state == "Ongoing"):
        return "Loading"
    if(state == "Loading"):
        return "Returning"

def unload(state):
    if(state == "Returning"):
        return "Unloading"
    if(state == "Unloading"):
        return "Free"
