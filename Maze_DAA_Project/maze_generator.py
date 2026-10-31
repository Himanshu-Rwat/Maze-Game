import random
import time


def generate_maze(size):
    
    started = time.perf_counter()
    wall_size = 2 * size + 1
    maze = [[1 for _ in range(wall_size)] for _ in range(wall_size)]
    visited = [[False for _ in range(size)] for _ in range(size)]

    start = (0, 0)
    stack = [start]
    visited[0][0] = True
    maze[1][1] = 0

    while stack:
        row, col = stack[-1]
        neighbors = []
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = row + dr, col + dc
            if 0 <= nr < size and 0 <= nc < size and not visited[nr][nc]:
                neighbors.append((nr, nc, dr, dc))

        if neighbors:
            nr, nc, dr, dc = random.choice(neighbors)
            visited[nr][nc] = True
            maze[2 * row + 1 + dr][2 * col + 1 + dc] = 0
            maze[2 * nr + 1][2 * nc + 1] = 0
            stack.append((nr, nc))
        else:
            stack.pop()  

    maze[0][1] = 0
    maze[wall_size - 1][wall_size - 2] = 0
    return maze, time.perf_counter() - started
