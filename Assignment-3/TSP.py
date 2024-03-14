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
#Generate a random genome
def generate_genome():
    city_list = []
    city_list = rand.sample(range(2, 53), 51)
    city_list.insert(0, 1)
    genome = Genome(city_list, -1)
    return genome
#Initiate first population
def init_population(pop_size):
    population = []
    for _ in range(0, pop_size):
        population.append(generate_genome())
        
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

#def selection():#
#    population.sort(key=lambda x: x.fitness)
 #   fittest = population[0:(len(population)//2)]
 #   return fittest
def tournament_selection(population, t_size):
    mating_pool = []
    while len(mating_pool) < len(population)//2:
        candidates = rand.sample(population, t_size)
        fittest = min(candidates, key=lambda x: x.fitness)
        mating_pool.append(fittest)
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
    elites = []
    for i in range(elit_rate):      
        elites.append(mating_pool[0])
        mating_pool.remove(mating_pool[0])
        if rand.uniform(0, 1) <= mut_rate_elite:
            mutate_swap(elites[i])
        new_gen.append(elites[i])
            
    while len(new_gen) < pop_size:
        elite_index = rand.randint(0, elit_rate-1)
        parents = rand.sample(mating_pool, 2)
        parent1 = parents[0]
        parent2 = parents[1]
        if rand.uniform(0, 1) <= cross_rate:       
            offspring = crossover(parent1, parent2)           
        else:
            offspring = crossover(elites[elite_index], parent1)
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
genome = [] #52 size
prev_fitness = {}
population = [] 
fitness_scores = []

population = init_population(pop_size)
for genome in population:
    eval_fitness(genome)
t_size = 3
elit_rate = 1
generations = 0
cross_rate = 0.60
mut_rate = 0.33
mut_rate_elite = 0.22
mut_amount = 1
start = time.time()
while((min(population, key=lambda x: x.fitness).fitness >= 9000 or (min(population, key=lambda x: x.fitness).fitness <= 0)) and fitness_amount < 250000):
    old_fitness = (min(population, key=lambda x: x.fitness).fitness)
    mating_pool = tournament_selection(population, t_size)
    new_generation = populate_new_gen(mating_pool)
    for genome in new_generation:
        eval_fitness(genome)
    population = new_generation
    generations += 1
    if generations % 4 == 0:   
        print("Fitness:", (min(population, key=lambda x: x.fitness).fitness))
        
        
    #print("Generation:", generations)
    
end = time.time()
print("Time:", end-start)
print("Distance for last generation", (min(population, key=lambda x: x.fitness).fitness))
print("Generations:", generations)







