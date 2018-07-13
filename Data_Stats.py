import pandas as pd

def init_dataStats(params, data_stats, agents):
    data_stats = pd.DataFrame(columns=["AGV", "Conflicts", "Waits", "Path_Change", "Runs", "Steps", "Time_Steps"])
    for i in range(0,len(agents)):
        data_stats.loc[i] = 0
        data_stats["AGV"].iloc[i] = i
    data_stats.set_index('AGV', inplace=True)
    return data_stats

def data_conflicts_and_step(data_stats, conflict_bool, ag, agents):
    if(conflict_bool != [0,0]):
        # There has been a conflict
        data_stats["Conflicts"][agents.index(ag)] += 1
        if(conflict_bool == [1,0]):
            # There has been a conflict and the agent stayed
            data_stats["Waits"][agents.index(ag)] += 1
        elif(conflict_bool == [2,0]):
            # There has been a conflict and the agent changed its path
            data_stats["Path_Change"][agents.index(ag)] += 1
    # If the agent didn't wait, increase the step number.
    if(conflict_bool != [1,0]):
        data_stats["Steps"][agents.index(ag)] += 1
    return data_stats

def data_runs(data_stats, ag, agents):
    data_stats["Runs"][agents.index(ag)] += 1
    return data_stats

def data_timesteps(data_stats, time, ag, agents):
    data_stats["Time_Steps"][agents.index(ag)] = time
    return data_stats
