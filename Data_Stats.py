import pandas as pd

def init_dataStats(data_stats, agents):
    data_stats = pd.DataFrame(columns=["AGV", "Conflicts", "Conflict_Wait", "Conflict_Path", "Waiting_Gate", "Articles", "Moving_Steps", "Time_Steps"])
    for i in range(0,len(agents)):
        data_stats.loc[i] = 0
        data_stats["AGV"].iloc[i] = i
    data_stats.set_index('AGV', inplace=True)
    return data_stats

def data_conflicts_and_step(data_stats, conflict_bool, ag, agents):
    if(conflict_bool != 0):
        # There has been a conflict
        data_stats["Conflicts"][agents.index(ag)] += 1
        if(conflict_bool == 1):
            # There has been a conflict and the agent stayed
            data_stats["Conflict_Wait"][agents.index(ag)] += 1
        elif(conflict_bool == 2):
            # There has been a conflict and the agent changed its path
            data_stats["Conflict_Path"][agents.index(ag)] += 1
    # If the agent didn't wait, increase the step number.
    if(conflict_bool != 1):
        data_stats["Moving_Steps"][agents.index(ag)] += 1
    return data_stats

def data_articles(data_stats, ag, agents):
    data_stats["Articles"][agents.index(ag)] += 1
    return data_stats

def data_timesteps(data_stats, time, ag, agents):
    data_stats["Time_Steps"][agents.index(ag)] = time
    return data_stats

def data_wait_gate(data_stats, ag, agents):
    data_stats["Waiting_Gate"][agents.index(ag)] += 1
    return data_stats
