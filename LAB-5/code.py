import random

# Job processing times
jobs = [4, 2, 7, 5, 3, 6]

# Number of machines and wolves
num_machines = 3
num_wolves = 10
max_iterations = 100

num_jobs = len(jobs)

# Convert continuous wolf position into machine assignments
def decode(position):
    return [
        min(num_machines - 1, max(0, round(x)))
        for x in position
    ]

# Calculate fitness (makespan)
def fitness(position):
    assignment = decode(position)
    machine_loads = [0] * num_machines

    for i in range(num_jobs):
        machine = assignment[i]
        machine_loads[machine] += jobs[i]

    return max(machine_loads)

# Initialize wolves randomly
wolves = [
    [random.uniform(0, num_machines - 1)
     for _ in range(num_jobs)]
    for _ in range(num_wolves)
]

# GWO algorithm
for t in range(1, max_iterations + 1):

    # Evaluate fitness of all wolves
    ranked = sorted(wolves, key=fitness)

    alpha = ranked[0][:]
    beta = ranked[1][:]
    delta = ranked[2][:]

    # Calculate a
    a = 2 - (2 * t / max_iterations)

    new_wolves = []

    for wolf in wolves:
        new_position = []

        for j in range(num_jobs):

            # Random values
            r1, r2 = random.random(), random.random()
            A1 = 2 * a * r1 - a
            C1 = 2 * r2

            r1, r2 = random.random(), random.random()
            A2 = 2 * a * r1 - a
            C2 = 2 * r2

            r1, r2 = random.random(), random.random()
            A3 = 2 * a * r1 - a
            C3 = 2 * r2

            # Distance from Alpha, Beta and Delta
            D_alpha = abs(C1 * alpha[j] - wolf[j])
            D_beta = abs(C2 * beta[j] - wolf[j])
            D_delta = abs(C3 * delta[j] - wolf[j])

            # New positions
            X1 = alpha[j] - A1 * D_alpha
            X2 = beta[j] - A2 * D_beta
            X3 = delta[j] - A3 * D_delta

            new_x = (X1 + X2 + X3) / 3

            # Boundary handling
            new_x = max(0, min(num_machines - 1, new_x))

            new_position.append(new_x)

        new_wolves.append(new_position)

    wolves = new_wolves

# Find final best solution
best_wolf = min(wolves, key=fitness)
best_assignment = decode(best_wolf)
best_fitness = fitness(best_wolf)

# Display results
print("JOB SCHEDULING USING GREY WOLF OPTIMIZATION")
print("--------------------------------------------")

machine_loads = [0] * num_machines

for i in range(num_jobs):
    machine = best_assignment[i]
    machine_loads[machine] += jobs[i]

for m in range(num_machines):
    print(f"\nMachine {m + 1}:")
    for i in range(num_jobs):
        if best_assignment[i] == m:
            print(f"  Job {i + 1} - Processing Time: {jobs[i]}")

    print("Total Processing Time:", machine_loads[m])

print("\nMinimum Makespan:", best_fitness)
