import collections
import numpy as np
from Data_Stats import *

def moving(ag, agents, envir, data_stats):
    ag.path, conflict_bool = ag.conflict_handler(envir)
    data_stats = data_conflicts_and_step(data_stats, conflict_bool, ag, agents)
    ag.pos = ag.path[0]
    ag.path.pop(0)
    return ag, agents, envir, data_stats

def navigation(envir, position, goal):
    wall, gate, clear = 0.01, 0.02, 0
    width, height = envir.shape
    queue = collections.deque([[position]])
    seen = set(position)
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if (x, y) == goal:
            path.pop(0)
            return path
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1), (x-1,y-1), (x-1,y+1),(x+1,y-1), (x+1,y+1)):
        #for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < width and 0 <= y2 < height and envir[x2][y2] != wall and (envir[x2][y2] != gate or (x2, y2) == goal) and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))
