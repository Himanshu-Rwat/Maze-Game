
from maze_generator import generate_maze
from pathfinding import bfs_shortest_path


def compare_sizes(sizes=(10, 20, 30)):
    results = []
    for size in sizes:
        maze, generation_seconds = generate_maze(size)
        path, visited, bfs_seconds = bfs_shortest_path(
            maze, (0, 0), (size - 1, size - 1))
        results.append({
            "size": size,
            "generation_seconds": generation_seconds,
            "bfs_seconds": bfs_seconds,
            "visited": visited,
            "path_length": max(0, len(path) - 1),
        })
    return results
