

import time
import pygame
from maze_generator import generate_maze
from pathfinding import bfs_shortest_path
from performance import compare_sizes

WIDTH, HEIGHT = 1000, 760
PANEL_X = 700
SIZES = {pygame.K_1: 10, pygame.K_2: 20, pygame.K_3: 30}
WHITE = (245, 246, 250)
DARK = (35, 42, 58)
WALL = (38, 48, 68)
FLOOR = (230, 235, 242)
GREEN = (62, 170, 110)
RED = (225, 85, 85)
BLUE = (65, 125, 220)
YELLOW = (255, 205, 70)


class MazeGame:

    def __init__(self, screen, font, small_font):
        self.screen = screen
        self.font = font
        self.small_font = small_font
        self.size = 20
        self.new_maze()

    def new_maze(self):

        self.maze, self.generation_time = generate_maze(self.size)
        self.start = (0, 0)
        self.goal = (self.size - 1, self.size - 1)
        self.player = self.start
        self.moves = 0
        self.started_at = None
        self.game_started = False
        self.finished_at = None
        self.won = False
        self.solution = []
        self.bfs_visited = 0
        self.bfs_time = 0.0
        self.path_length = 0
        self.performance_rows = []

    def reset(self):

        self.player = self.start
        self.moves = 0
        self.started_at = None
        self.game_started = False
        self.finished_at = None
        self.won = False

    def start_game(self):

        if not self.game_started and not self.won:
            self.game_started = True
            self.started_at = time.perf_counter()

    def move(self, dr, dc):

        if self.won or not self.game_started:
            return
        row, col = self.player
        nr, nc = row + dr, col + dc
        if 0 <= nr < self.size and 0 <= nc < self.size:
            if self.maze[2 * row + 1 + dr][2 * col + 1 + dc] == 0:
                self.player = (nr, nc)
                self.moves += 1
                if self.player == self.goal:
                    self.won = True
                    self.finished_at = time.perf_counter()

    def solve(self):
        
        self.solution, self.bfs_visited, self.bfs_time = bfs_shortest_path(
            self.maze, self.start, self.goal)
        self.path_length = max(0, len(self.solution) - 1)

    def draw_text(self, text, x, y, color=DARK, font=None):
        self.screen.blit((font or self.small_font).render(text, True, color), (x, y))

    def draw(self):
        self.screen.fill(WHITE)
        self.draw_text("MAZE GAME | DFS GENERATION + BFS", 24, 18, DARK, self.font)
        self.draw_text("Move with arrows or WASD. Reach the green goal.", 24, 52)

    
        usable = min(640, HEIGHT - 105)
        tile = max(5, usable // len(self.maze))
        board_x, board_y = 24, 96
        for row in range(len(self.maze)):
            for col in range(len(self.maze)):
                color = FLOOR if self.maze[row][col] == 0 else WALL
                pygame.draw.rect(self.screen, color,
                                 (board_x + col * tile, board_y + row * tile,
                                  tile, tile))

        def center(cell):
            row, col = cell
            return (board_x + (2 * col + 1) * tile + tile // 2,
                    board_y + (2 * row + 1) * tile + tile // 2)

        if self.solution:
            points = [center(cell) for cell in self.solution]
            if len(points) > 1:
                pygame.draw.lines(self.screen, BLUE, False, points, max(2, tile // 3))
            for point in points:
                pygame.draw.circle(self.screen, BLUE, point, max(2, tile // 3))
        for cell, color in ((self.start, GREEN), (self.goal, RED), (self.player, YELLOW)):
            pygame.draw.circle(self.screen, color, center(cell), max(3, tile // 2))

        x = PANEL_X
        self.draw_text("CONTROLS", x, 105, DARK, self.font)
        controls = ["Enter: start game and timer", "Arrow keys / WASD: move", "N: new random maze", "R: reset player",
                    "F: show BFS shortest path", "P: compare all sizes", "1 / 2 / 3: choose size"]
        for index, line in enumerate(controls):
            self.draw_text(line, x, 145 + index * 27)
        self.draw_text("GAME STATUS", x, 325, DARK, self.font)
        if self.started_at is None:
            elapsed = 0.0
        elif self.won and self.finished_at is not None:
            elapsed = self.finished_at - self.started_at
        else:
            elapsed = time.perf_counter() - self.started_at
        values = ["Maze size: {} x {}".format(self.size, self.size),
                  "Moves: {}".format(self.moves), "Time: {:.1f} s".format(elapsed),
                  "Generation: {:.5f} s".format(self.generation_time),
                  "BFS visited: {}".format(self.bfs_visited),
                  "BFS time: {:.6f} s".format(self.bfs_time),
                  "Path length: {} moves".format(self.path_length)]
        for index, line in enumerate(values):
            self.draw_text(line, x, 365 + index * 27)
        if self.won:
            self.draw_text("YOU REACHED THE GOAL!", x, 565, GREEN, self.font)
        elif not self.game_started:
            self.draw_text("Press ENTER to start", x, 565, BLUE, self.font)
        if self.performance_rows:
            self.draw_text("SIZE  GEN(s)   BFS(s)  VISITED  PATH", x, 602)
            for index, row in enumerate(self.performance_rows):
                line = "{size:>2}x{size:<2} {generation_seconds:.4f}  {bfs_seconds:.5f}  {visited:>5}   {path_length:>4}".format(**row)
                self.draw_text(line, x, 626 + index * 22)
        self.draw_text("Green: Start  Red: Goal  Yellow: Player  Blue: BFS route", 24, HEIGHT - 29)
        pygame.display.flip()


def main():
    pygame.init()
    pygame.display.set_caption("DAA Maze Game")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game = MazeGame(screen, pygame.font.SysFont("arial", 23, bold=True),
                    pygame.font.SysFont("arial", 17))
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key in SIZES:
                    game.size = SIZES[event.key]
                    game.new_maze()
                elif event.key == pygame.K_n:
                    game.new_maze()
                elif event.key == pygame.K_r:
                    game.reset()
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    game.start_game()
                elif event.key == pygame.K_f:
                    game.solve()
                elif event.key == pygame.K_p:
                    game.performance_rows = compare_sizes()
                elif event.key in (pygame.K_UP, pygame.K_w):
                    game.move(-1, 0)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    game.move(1, 0)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    game.move(0, -1)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    game.move(0, 1)
        game.draw()
        clock.tick(60)


if __name__ == "__main__":
    main()
