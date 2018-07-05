import collections

def navigation(envir, position, goal):
    width, height = envir.shape
    wall, clear = 1, 0
    queue = collections.deque([[position]])
    seen = set(position)
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if [x, y] == goal:
            return path, 1
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1), (x-1,y-1), (x-1,y+1),(x+1,y-1), (x+1,y+1)):
            if 0 <= x2 < width and 0 <= y2 < height and envir[y2][x2] != wall and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))
