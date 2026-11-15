import pygame
from collections import deque
import random

# random.seed(1)

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

class Agent:
    def __init__(self, world):
        self.world = world
        self.pos = (0,0)
        self.lr = 0.1
        self.discount = 0.95
        self.exploration = 0.2
        self.Q = [[[0,0,0,0] for _ in range(world.dim)] for _ in range(world.dim)]

    def step(self, action):
        if action == 0:
            movement = (-1, 0)
        elif action == 1:
            movement = (1, 0)
        elif action == 2:
            movement = (0, -1)
        else:
            movement = (0, 1)

        next_statex = max(0, min(self.world.dim - 1, self.pos[0] + movement[0]))
        next_statey = max(0, min(self.world.dim - 1, self.pos[1] + movement[1]))
        if self.world.grid[next_statex][next_statey] == 1:
            next_state = self.pos
        else:
            next_state = (next_statex, next_statey)
        finished = next_state == (self.world.dim - 1, self.world.dim - 1)
        reward = 10.0 if finished else -0.2
        return next_state, reward, finished

    def choose_action(self):
        if random.random() < self.exploration:
            return random.randrange(4)
        best = max(self.Q[self.pos[0]][self.pos[1]])
        return random.choice([a for a in range(4) if self.Q[self.pos[0]][self.pos[1]][a] == best])
       
pygame.init()
res = 500
screen = pygame.display.set_mode((res,res))
clock = pygame.time.Clock()
running = True
maze = Maze(17)
maze.carve_maze()
maze_width = int(0.8 * res)
maze_posx = int(0.1 * res)
maze_posy = int(0.1 * res)
cell_w = maze_width // maze.dim

agent = Agent(maze)
episode_steps = 0
max_episode_steps = maze.dim * maze.dim * 10


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif pygame.key.get_pressed()[pygame.K_q]:
            running = False
        elif pygame.key.get_pressed()[pygame.K_r]:
            maze = Maze(17)
            maze.carve_maze()
            agent = Agent(maze)
            episode_steps = 0

    screen.fill("darkolivegreen")

    pygame.draw.rect(screen, "tan", (0, maze_posy, maze_posx, cell_w))
    pygame.draw.rect(screen, "tan", (maze_posx + (maze.dim * cell_w), maze_posy + (maze.dim * cell_w) - cell_w, res - maze_posx + maze_width, cell_w))

    for i in range(maze.dim):
        for j in range(maze.dim):
            if maze.grid[i][j] == 0:
                pygame.draw.rect(screen, "tan", (maze_posx + (cell_w * i), maze_posy + (cell_w * j), cell_w, cell_w))

    agent_drawx = maze_posx + cell_w * agent.pos[0] + cell_w // 2 
    agent_drawy = maze_posy + cell_w * agent.pos[1] + cell_w // 2 

    pygame.draw.circle(screen, "red", (agent_drawx, agent_drawy), cell_w // 2)

    if not running:
        break

    action = agent.choose_action()
    next_state, reward, finished = agent.step(action)

    future = 0.0 if finished else max(agent.Q[next_state[0]][next_state[1]])
    target = reward + agent.discount * future

    values = agent.Q[agent.pos[0]][agent.pos[1]]
    values[action] += agent.lr * (target - values[action])

    agent.pos = next_state
    episode_steps += 1

    if finished or episode_steps >= max_episode_steps:
        agent.pos = (0, 0)
        episode_steps = 0

    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()