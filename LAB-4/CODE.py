import numpy as np
import math

def irrigation_objective(water_allocations):
    current_moisture = np.array([20.0, 35.0, 10.0])
    target_moisture = 50.0
    water_efficiency = 1.5
    evaporation_loss = 2.0
    
    predicted_moisture = current_moisture + (water_allocations * water_efficiency) - evaporation_loss
    
    total_water_cost = np.sum(water_allocations) * 0.5
    under_water_penalty = np.sum(np.maximum(0, target_moisture - predicted_moisture)**2) * 50.0
    over_water_penalty = np.sum(np.maximum(0, predicted_moisture - target_moisture)**2) * 10.0
    
    return total_water_cost + under_water_penalty + over_water_penalty

def levy_flight_step(dim, beta=1.5):
    sigma = (math.gamma(1 + beta) * math.sin(math.pi * beta / 2) / 
             (math.gamma((1 + beta) / 2) * beta * 2**((beta - 1) / 2)))**(1 / beta)
    
    u = np.random.normal(0, sigma, size=dim)
    v = np.random.normal(0, 1, size=dim)
    step = u / np.abs(v)**(1 / beta)
    return step

def cuckoo_search_irrigation(obj_func, dim, n_nests=20, pa=0.25, max_iter=200, lb=0, ub=50):
    nests = np.random.uniform(lb, ub, (n_nests, dim))
    fitness = np.apply_along_axis(obj_func, 1, nests)
    
    best_idx = np.argmin(fitness)
    best_nest = nests[best_idx].copy()
    best_fitness = fitness[best_idx]
    
    for t in range(max_iter):
        cuckoo_idx = np.random.randint(0, n_nests)
        cuckoo = nests[cuckoo_idx].copy()
        
        alpha = 0.5
        step = alpha * levy_flight_step(dim)
        cuckoo = cuckoo + step * np.random.randn(dim) 
        
        cuckoo = np.clip(cuckoo, lb, ub)
        
        cuckoo_fitness = obj_func(cuckoo)
        
        j = np.random.randint(0, n_nests)
        if cuckoo_fitness < fitness[j]:
            nests[j] = cuckoo
            fitness[j] = cuckoo_fitness
            
        sort_idx = np.argsort(fitness)
        nests = nests[sort_idx]
        fitness = fitness[sort_idx]
        num_abandon = int(pa * n_nests)
        
        for i in range(n_nests - num_abandon, n_nests):
            nest1 = nests[np.random.randint(0, n_nests)]
            nest2 = nests[np.random.randint(0, n_nests)]
            new_nest = nests[i] + np.random.uniform(0, 1, dim) * (nest1 - nest2)
            new_nest = np.clip(new_nest, lb, ub)
            
            nests[i] = new_nest
            fitness[i] = obj_func(new_nest)
            
        current_best_idx = np.argmin(fitness)
        if fitness[current_best_idx] < best_fitness:
            best_fitness = fitness[current_best_idx]
            best_nest = nests[current_best_idx].copy()
            
    return best_nest, best_fitness

if __name__ == "__main__":
    num_zones = 3
    
    best_allocation, best_score = cuckoo_search_irrigation(
        obj_func=irrigation_objective, 
        dim=num_zones, 
        n_nests=25,
        pa=0.25,
        max_iter=300,
        lb=0,
        ub=40
    )
    
    print("=== Smart Irrigation Optimization Results ===")
    print(f"Zone 1 Allocation: {best_allocation[0]:.2f} Liters")
    print(f"Zone 2 Allocation: {best_allocation[1]:.2f} Liters")
    print(f"Zone 3 Allocation: {best_allocation[2]:.2f} Liters")
    print(f"Algorithm Minimum Code cost Score: ${best_score:.4f}")


