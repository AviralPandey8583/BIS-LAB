import random

N = 6
ROADS = 4
ITERATIONS = 5

traffic = [40, 80, 60, 20]

def create_cell():
    a = random.randint(20, 40)
    b = random.randint(20, 40)
    c = random.randint(20, 40)
    d = 120 - a - b - c

    return [a, b, c, d]

def fitness(cell):
    return sum(traffic[i] / cell[i] for i in range(ROADS))

# Initialize cells
cells = [create_cell() for _ in range(N)]

print("INITIAL POPULATION")
for i, cell in enumerate(cells):
    print("Cell", i+1, ":", cell,
          "Fitness:", round(fitness(cell), 2))

# PCA iterations
for t in range(ITERATIONS):

    new_cells = [cell[:] for cell in cells]

    print("\nITERATION", t+1)

    for i in range(N):

        left = (i-1) % N
        right = (i+1) % N

        best = min([cells[i], cells[left], cells[right]],
                   key=fitness)

        # Crossover
        candidate = [
            best[k] if random.random() < 0.5
            else cells[i][k] for k in range(ROADS)
        ]

        # Mutation
        k = random.randint(0, ROADS-1)
        candidate[k] += random.choice([-2, 2])

        # Repair total green time
        diff = 120 - sum(candidate)
        candidate[(k+1) % ROADS] += diff

        # Replacement
        if fitness(candidate) < fitness(cells[i]):
            new_cells[i] = candidate

    cells = new_cells

    best = min(cells, key=fitness)

    print("Best Timings:", best)
    print("Best Fitness:", round(fitness(best), 3))

# Final result
best = min(cells, key=fitness)

print("\nFINAL TRAFFIC SIGNAL SCHEDULE")
for i in range(ROADS):
    print("Road", i+1, ":", best[i], "seconds")

print("Total Green Time:", sum(best), "seconds")
print("Final Fitness:", round(fitness(best), 3))
