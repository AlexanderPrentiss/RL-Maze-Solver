import pygame
from collections import deque
import random

# random.seed(1)

pygame.init()
screen = pygame.display.set_mode((1000, 1000))

clock = pygame.time.Clock()
running = True

class Maze:
    def __init__(self, dim):
        self.dim = dim
        self.grid = [[0 if _ % 2 == 0 else 1 for _ in range(dim)] if _ % 2 == 0 else [1 for _ in range(dim)] for _ in range(dim)]

    def get_neighbors(self, pos):
        posx, posy = pos
        out = []
        if posx > self.dim // 2 + 1 or posy > self.dim // 2 + 1:
            return 
        if posx - 1 >= 0:
            out.append((posx - 1, posy))
        if posx + 1 < self.dim // 2 + 1:
            out.append((posx + 1, posy))
        if posy - 1 >= 0:
            out.append((posx, posy - 1))
        if posy + 1 < self.dim // 2 + 1:
            out.append((posx, posy + 1))

        for i in range(len(out)-1, -1, -1):
            if out[i] == -1:
                out.pop(i)

        random.shuffle(out)

        return out

    def carve_maze(self):
        visited = set()
        to_visit = deque()
        maze_graph = {}
        pos = (0, 0)
        neighbors = self.get_neighbors(pos)
        print(neighbors)
        print('\n\n')
        for i in range(len(neighbors)-1,-1,-1):
            if neighbors[i] in visited:
                neighbors.pop(i)
            else:
                maze_graph[neighbors[i]] = pos
                to_visit.appendleft(neighbors[i])
        visited.add(pos)
        while len(to_visit) > 0:
            pos = to_visit.popleft()
            prev = maze_graph[pos]

            print('\n\n')
            print(pos, prev)
            print(prev[0] * 2 + (pos[0] - prev[0]), prev[1] * 2 + (pos[1] - prev[1]))
            print('\n\n')
            self.grid[prev[0] * 2 + (pos[0] - prev[0])][prev[1] * 2 + (pos[1] - prev[1])] = 0
            neighbors = self.get_neighbors(pos)
            for i in range(len(neighbors)-1,-1,-1):
                if neighbors[i] in visited:
                    neighbors.pop(i)
                else:
                    maze_graph[neighbors[i]] = pos
                    to_visit.appendleft(neighbors[i])
            print(neighbors)
            print('\n\n')
            visited.add(pos)
       

maze = Maze(17)
maze.carve_maze()
maze_width = 800
maze_posx = 100
maze_posy = 100
border_w = 10
border_w = border_w // 2
cell_w = maze_width // maze.dim

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif pygame.key.get_pressed()[pygame.K_q]:
            running = False
        elif pygame.key.get_pressed()[pygame.K_r]:
            maze = Maze(17)
            maze.carve_maze()

    screen.fill("darkolivegreen")
    # pygame.draw.rect(screen, "Black", (maze_posx - border_w, maze_posy - border_w, maze_width + border_w, maze_width + border_w), 10)

    # RENDER YOUR GAME HERE

    pygame.draw.rect(screen, "tan", (0, maze_posy, maze_posx, cell_w))
    pygame.draw.rect(screen, "tan", (maze_posx + maze_width - 1, maze_posy + maze_width - cell_w, 1000 - maze_posx + maze_width, cell_w))

    for i in range(maze.dim):
        for j in range(maze.dim):
            if maze.grid[i][j] == 0:
                pygame.draw.rect(screen, "tan", (maze_posx + (cell_w * i), maze_posy + (cell_w * j), cell_w, cell_w))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()