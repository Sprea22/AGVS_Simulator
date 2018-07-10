import collections
import numpy as np

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
            if 0 <= x2 < width and 0 <= y2 < height and envir[x2][y2] != wall and (envir[x2][y2] != gate or (x2, y2) == goal) and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))
