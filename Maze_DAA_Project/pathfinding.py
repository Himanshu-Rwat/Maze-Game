from collections import deque
import time


def _neighbors(maze, cell):
    row, col = cell
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = row + dr, col + dc
        if (0 <= 2 * nr + 1 < len(maze) - 1 and
                0 <= 2 * nc + 1 < len(maze) - 1 and
                maze[2 * row + 1 + dr][2 * col + 1 + dc] == 0):
            yield nr, nc


def bfs_shortest_path(maze, start, goal):
    started = time.perf_counter()
    queue = deque([start])
    parent = {start: None}
    while queue:
        current = queue.popleft()
        if current == goal:
            break
        for neighbor in _neighbors(maze, current):
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)
    path = []
    if goal in parent:
        current = goal
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
    return path, len(parent), time.perf_counter() - started


def dfs_path(maze, start, goal):
    started = time.perf_counter()
    stack = [start]
    parent = {start: None}
    while stack:
        current = stack.pop()
        if current == goal:
            break
        for neighbor in _neighbors(maze, current):
            if neighbor not in parent:
                parent[neighbor] = current
                stack.append(neighbor)
    path = []
    if goal in parent:
        current = goal
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
    return path, len(parent), time.perf_counter() - started
