import random

random.seed(42)

corridor_len = 5

Q = [[0, 0] for _ in range(corridor_len)]

lr = 0.1
discount = 0.95
exploration = 0.2

def step(state, action):
    movement = -1 if action == 0 else 1
    next_state = max(0, min(corridor_len - 1, state + movement))
    finished = next_state == corridor_len - 1
    reward = 1.0 if finished else -0.01
    return next_state, reward, finished

def choose_action(state):
    if random.random() < exploration:
        return random.randrange(2)
    best = max(Q[state])
    return random.choice([a for a in range(2) if Q[state][a] == best])

for episode in range(100):
    state = 0

    for _ in range(300):
        action = choose_action(state)
        next_state, reward, finished = step(state, action)
        future = 0.0 if finished else max(Q[next_state])
        target = reward + discount * future

        # This is the learning step: update ONE table entry.
        Q[state][action] += lr * (target - Q[state][action])

        state = next_state
        if finished:
            break


print("State    Left    Right    Best action")
for state in range(4):
    left, right = Q[state]
    best = "right" if right > left else "left"
    print(f"{state:5}  {left:6.3f}  {right:7.3f}    {best}")