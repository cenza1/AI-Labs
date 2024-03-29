import numpy as np
import random as rand
import time


fitness_amount = 0
class Genome:
    def __init__(self, path, fitness):
        self.path = path
        self.fitness = fitness



def read_items():
    cities = {}
    with open('C:/Users/oscar/OneDrive\Dokument/GitHub/AI-Labs/Assignment-3/berlin52.tsp', 'r') as file:
        for _ in range(6):
            next(file)
        lines = file.readlines()
        i = 0
        for line in lines:
            if line.strip() == "EOF":
                break
            coord = line.split()
            (x,y) = (float(coord[1]), float(coord[2]))
            cities[int(coord[0])] = (x, y)
            i += 1
    return cities
#Calculates the euclidian distance between two points
def calculate_distance(city1, city2):
    (x1, y1) = city1
    (x2, y2) = city2
    return np.sqrt((np.power(x2 - x1, 2)) + (np.power(y2 - y1, 2)))

def find_nearest_city(start_city, len):
    current_city = start_city
    path = []
    unvisited = [i for i in range(1, len+1)]
    for _ in (range(len)):
        next_city = rand.sample(unvisited, 1)    
        current_city = next_city[0]
        path.append(current_city)
        unvisited.remove(current_city)
    return path
#Generate a random genome
def generate_genome():
    city_list = []
    city_list = rand.sample(range(2, 53), 51)
    city_list.insert(0, 1)
    genome = Genome(city_list, -1)
    return genome
#Initiate first population
#def init_population(pop_size):
    population = []
    start_city = 1
    city_list = []
    for _ in range(0, pop_size):
        if not city_list:
            city_list = rand.sample(range(2, 53), 51)
        population.append(Genome(find_nearest_city(start_city, len(cities)), -1))
        start_city = city_list.pop() 
    return population


def init_population(pop_size):
    population = []
    for _ in range(0, pop_size):
        genome = generate_genome()
        population.append(genome)
    return population

#Evaluate fitness of a genome
def eval_fitness(genome):
    fitness_value = 0
    global fitness_amount
    if genome.fitness != 0 and genome.fitness != -1:
        return genome.fitness
    for i in range(len(genome.path) - 1):
        fitness_value += calculate_distance(cities[genome.path[i]], cities[genome.path[i+1]])
    fitness_value += calculate_distance(cities[genome.path[i + 1]], cities[1])
    genome.fitness = fitness_value
    fitness_amount += 1

def tournament_selection(population, t_size, selection_pressure):
    mating_pool = []
    pop = population[:]
    while len(mating_pool) < selection_pressure:
        candidates = rand.sample(pop, t_size)
        fittest = min(candidates, key=lambda x: x.fitness)
        mating_pool.append(fittest)
        pop.remove(fittest)
    mating_pool.sort(key=lambda x: x.fitness)
    return mating_pool

def crossover(parent1, parent2):
    cities_cut = len(cities)-1
    cut = round(rand.uniform(1, cities_cut))
    offspring = (Genome([], 0))
    offspring.path = parent1.path[0:cut]
    offspring.path += [city for city in parent2.path if city not in offspring.path]
    
   
    return offspring
#def crossover(parent1, parent2):
    #crossover_point1 = rand.randint(1, (len(parent1)-1))
    #crossover_point2 = rand.randint(1, (len(parent1)-1)) 
    crossover_points = rand.sample(range(1, (len(parent1)-1)), 2)
    crossover_points.sort()
    offspring = parent1[:]
    for i in range(len(crossover_points)//2):
        offspring[crossover_points[i] : crossover_points[i+1] + 1] = parent2[crossover_points[i] : crossover_points[i+1] + 1]
        missing_cities = [city for city in parent1 if city not in offspring[crossover_points[i]:crossover_points[i+1] + 1]]
        offspring[crossover_points[i+1] + 1:] = missing_cities
    offspring = repair(offspring)      
   
    return offspring

def populate_new_gen(mating_pool):
    new_gen = []
    for i in range(elit_rate):      
        if rand.uniform(0, 1) <= mut_rate_elite:
            mutate_swap(mating_pool[i])
        new_gen.append(mating_pool[i])
            
    while len(new_gen) < pop_size:
        parents = rand.sample(mating_pool, 2)
        parent1 = parents[0]
        parent2 = parents[1]
        if rand.uniform(0, 1) <= cross_rate:       
            offspring = crossover(parent1, parent2)           
        else:
            continue
        if rand.uniform(0, 1) <= mut_rate:
            mutate_swap(offspring)
        new_gen.append(offspring)
    return new_gen

def mutate_swap(genome):
    
    indexes = rand.sample(range(2, len(genome.path)), mut_amount*2)
    for i in range(len(indexes)//2):
        genome.path[indexes[i]], genome.path[indexes[i+1]] = genome.path[indexes[i+1]], genome.path[indexes[i]]
        genome.fitness = 0
    return genome
    


cities = read_items()

pop_size = 32
selection_pressure = 22
genome = [] #52 size
prev_fitness = {}
population = [] 
fitness_scores = []

population = init_population(pop_size)
for genome in population:
    eval_fitness(genome)
t_size = 3
elit_rate = 2
generations = 0
cross_rate = 0.80
mut_rate = 0.2
mut_rate_elite = 0.2
mut_amount = 1
start = time.time()
while((min(population, key=lambda x: x.fitness).fitness >= 9000) and fitness_amount < 250000):
    mating_pool = tournament_selection(population, t_size, selection_pressure)
    new_generation = populate_new_gen(mating_pool)
    for genome in new_generation:
        eval_fitness(genome)
    population = new_generation
    generations += 1
    if generations % 4 == 0:   
        print("Fitness:", (min(population, key=lambda x: x.fitness).fitness))
    
end = time.time()
print("Time:", end-start)
print("Distance for last generation", (min(population, key=lambda x: x.fitness).fitness))
print("Generations:", generations)







