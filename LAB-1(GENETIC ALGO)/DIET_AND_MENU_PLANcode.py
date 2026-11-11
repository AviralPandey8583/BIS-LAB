import random

FOODS = [
    {"name": "Chicken Breast", "cost": 4.5, "cal": 165, "prot": 31},
    {"name": "Brown Rice",     "cost": 1.2, "cal": 215, "prot": 5},
    {"name": "Black Beans",    "cost": 0.9, "cal": 114, "prot": 8},
    {"name": "Broccoli",       "cost": 1.5, "cal": 55,  "prot": 4},
    {"name": "Eggs",           "cost": 0.5, "cal": 78,  "prot": 6},
]

target_cal = float(input("Enter target calories (e.g. 2000): "))
target_prot = float(input("Enter target protein in grams (e.g. 120): "))

def fitness(chrom):
    cost = sum(q * f["cost"] for q, f in zip(chrom, FOODS))
    cal  = sum(q * f["cal"] for q, f in zip(chrom, FOODS))
    prot = sum(q * f["prot"] for q, f in zip(chrom, FOODS))
    penalty = max(0, target_cal - cal) + max(0, target_prot - prot)
    return 1.0 / (cost + 50 * penalty + 1e-6)

pop = [[random.randint(0, 5) for _ in FOODS] for _ in range(100)]

for _ in range(200):
    scores = [fitness(c) for c in pop]
    next_pop = []
    for _ in range(50):
        p1, p2 = random.choices(pop, weights=scores, k=2)
        c1 = [g1 if random.random() < 0.5 else g2 for g1, g2 in zip(p1, p2)]
        c2 = [g2 if random.random() < 0.5 else g1 for g1, g2 in zip(p1, p2)]
        for child in (c1, c2):
            next_pop.append([max(0, g + random.choice([-1, 1])) if random.random() < 0.2 else g for g in child])
    pop = next_pop

best = max(pop, key=fitness)

print("\n=== OPTIMIZED DIET PLAN ===")
for q, f in zip(best, FOODS):
    if q > 0:
        print(f"- {q}x {f['name']}")

print("\n=== TOTALS ===")
print(f"Total Cost: ${sum(q * f['cost'] for q, f in zip(best, FOODS)):.2f}")
print(f"Total Calories: {sum(q * f['cal'] for q, f in zip(best, FOODS))} kcal (Target: {target_cal:.0f})")
print(f"Total Protein: {sum(q * f['prot'] for q, f in zip(best, FOODS))} g (Target: {target_prot:.0f})")
