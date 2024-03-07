import numpy as np
import random as rand
import time
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
    genome = []
    genome = rand.sample(range(2, 53), 51)
    genome.insert(0, 1)
    return genome
#Initiate first population
def init_population(pop_size):
    population = []
    for _ in range(0, pop_size):
        population.append(generate_genome())
    return population
#Evaluate fitness of a genome
def eval_fitness(genome, cities):
    fitness_value = 0 
    for i in range(len(genome) - 1):
        fitness_value += calculate_distance(cities[genome[i]], cities[genome[i+1]])
    fitness_value += calculate_distance(cities[genome[i + 1]], cities[1])
               
    return fitness_value
#Might want to add so that the fittest gnome will survive to the next gen
def selection(population, cities):
    k = 2
    parents = []
    for _ in range((len(population) // k)):
        tournament = rand.sample(population, k)
        fitness_scores = [eval_fitness(genome, cities) for genome in tournament]
        for _ in range(k//2):
            winner_index = fitness_scores.index(min(fitness_scores))
            loser_index = fitness_scores.index(max(fitness_scores))
            parents.append(tournament[winner_index])
            population.remove(tournament[winner_index])
            population.remove(tournament[loser_index])
    return parents

def repair(genome): 
    repaired_genome = []
    visited_cities = set()
    for city in genome:
        if city not in visited_cities:
            repaired_genome.append(city)
            visited_cities.add(city)
    return repaired_genome


def crossover(parent1, parent2):
    #crossover_point1 = rand.randint(1, (len(parent1)-1))
    #crossover_point2 = rand.randint(1, (len(parent1)-1))
    crossover_point1, crossover_point2 = rand.sample(range(1, (len(parent1)-1)), 2)
    while (crossover_point2 - crossover_point1) > 25 or (crossover_point2 - crossover_point1) < 5:
        crossover_point1, crossover_point2 = rand.sample(range(1, (len(parent1)-1)), 2)
    offspring = parent1[:]
    offspring[crossover_point1 : crossover_point2 + 1] = parent2[crossover_point1 : crossover_point2 + 1]
    missing_cities = [city for city in parent1 if city not in offspring[crossover_point1:crossover_point2 + 1]]
    offspring[crossover_point2 + 1:] = missing_cities
    offspring = repair(offspring)
    if rand.randint(1, 8) == 1:           
        mutate_swap(offspring)
        
   
    return offspring

def populate_new_gen(population, cities):
    new_gen = []
    fitness_scores = [eval_fitness(genome, cities) for genome in population]
    for _ in range(2):       
        winner_index = fitness_scores.index(min(fitness_scores))
        new_gen.append(population[winner_index])
        fitness_scores.remove(fitness_scores[winner_index])
    
    for _ in range((len(population))-1):
        parents = rand.sample(population, 2)
        parent1 = parents[0]
        parent2 = parents[1]
        offspring1 = crossover(parent1, parent2)
        offspring2 = crossover(parent2, parent1)
        new_gen.append(offspring1)
        new_gen.append(offspring2)
    
    
    return new_gen

def mutate_inv(genome):
    mutated_genome = genome[::-1]
    return mutated_genome
def mutate_swap(genome):
    index1, index2 = rand.sample(range(2, len(genome)), 2)
    genome[index1], genome[index2] = genome[index2], genome[index1]
    return genome
    



    
    
generations = 1000
pop_size = 104
cities = read_items()
genome = [] #52 size
population = [] #520-1040 size
fitness_scores = []
population = init_population(pop_size)
start = time.time()
for _ in range(0, generations):
    population = selection(population, cities)
    population = populate_new_gen(population, cities)
    print("New generation")
fitness_scores = [eval_fitness(genome, cities) for genome in population]
winner_index = fitness_scores.index(min(fitness_scores))
end = time.time()
print("Time:", end-start)
print(population[winner_index])
print(eval_fitness(population[winner_index], cities))







