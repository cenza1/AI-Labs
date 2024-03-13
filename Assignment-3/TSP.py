import numpy as np
import random as rand
import time


fitness_amount = 0

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
def eval_fitness(genome):
    fitness_value = 0
    global fitness_amount
    for i in range(len(genome) - 1):
        fitness_value += calculate_distance(cities[genome[i]], cities[genome[i+1]])
    fitness_value += calculate_distance(cities[genome[i + 1]], cities[1])
    fitness_amount += 1
               
    return fitness_value
#Might want to add so that the fittest gnome will survive to the next gen
#def selection():
    k = 2
    parents = []
    for _ in range((len(population) // k)):
        #parent = roulette(fitness_scores)
        #parents.append(parent)
        #fitness_scores.remove(eval_fitness(parent))
        #population.remove(parent)
        tournament = rand.sample(population, k)
        fitness_scores = [eval_fitness(genome) for genome in tournament]
        for _ in range(k//2):
            winner_index = fitness_scores.index(min(fitness_scores))
            loser_index = fitness_scores.index(max(fitness_scores))
            parents.append(tournament[winner_index])
            population.remove(tournament[winner_index])
            population.remove(tournament[loser_index])
    return parents
def selection(fitness_scores):
    k = 2
    parents = []
    fitness = fitness_scores[:]
    while len(population) > 0:
        tournament = rand.sample(fitness, k)
        winner_index = tournament.index(min(tournament))
        loser_index = tournament.index(max(tournament))
        winner = population.index(population[fitness.index(tournament[winner_index])])
        loser = population.index(population[fitness.index(tournament[loser_index])])
        parents.append(population[winner])
        fitness_scores.remove(tournament[loser_index])
        remove_winner = population[winner]
        remove_loser = population[loser]
        population.remove(remove_winner)
        population.remove(remove_loser)
        fitness.remove(tournament[winner_index])
        fitness.remove(tournament[loser_index])
           
    return parents

def crossover(parent1, parent2):
    
    cities_cut = len(cities)-1
    cut = round(rand.uniform(1, cities_cut))
    offspring1 = parent1[0:cut]
    offspring1 += [city for city in parent2 if city not in offspring1]
    offspring2 = parent2[0:cut]
    offspring2 += [city for city in parent1 if city not in offspring2]
   
    return offspring1, offspring2
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

def populate_new_gen(fitness_scores):
    new_gen = []
    for _ in range(elit_rate):       
        winner_index = fitness_scores.index(min(fitness_scores))
        
        if rand.uniform(0, 1) <= mut_rate:
            mutate_swap(population[winner_index])
        elite = population[winner_index]
        new_gen.append(population[winner_index])
        fitness_scores.remove(fitness_scores[winner_index])
        
    for _ in range((len(population))-1):
        parents = rand.sample(population, 2)
        parent1 = parents[0]
        parent2 = parents[1]
        if rand.uniform(0, 1) <= cross_rate:       
            offspring1, offspring2 = crossover(parent1, parent2)
            new_gen.append(offspring1)
            new_gen.append(offspring2)
        else:
            elite_offspring1, elite_offspring2 = crossover(elite, parent1)
            new_gen.append(elite_offspring1)
            new_gen.append(elite_offspring2)
    if len(new_gen) != pop_size:
        new_gen.append(mutate_swap(offspring1))
    
    
    
    return new_gen

def mutate_swap(genome):
    
    indexes = rand.sample(range(2, len(genome)), mut_amount*2)
    for i in range(len(indexes)//2):
        genome[indexes[i]], genome[indexes[i+1]] = genome[indexes[i+1]], genome[indexes[i]]
    return genome
    


cities = read_items()

pop_size = 32
genome = [] #52 size
prev_fitness = {}
population = [] 
fitness_scores = []

population = init_population(pop_size)
fitness_scores = [eval_fitness(genome) for genome in population]

elit_rate = 1
generations = 0
cross_rate = 0.85
mut_rate = 0.20
mut_amount = 1
start = time.time()
while((min(fitness_scores) >= 8999) and fitness_amount < 250000):
    fitness_scores = [eval_fitness(genome) for genome in population]
    population = selection(fitness_scores)
    population = populate_new_gen(fitness_scores)
    generations += 1
    if generations % 4 == 0:   
        print("Fitness:", min(fitness_scores))
        
        
    #print("Generation:", generations)
    
end = time.time()
winner_index = fitness_scores.index(min(fitness_scores))
print("Time:", end-start)
print(population[winner_index])
print("Distance for last generation", eval_fitness(population[winner_index]))
print("Generations:", generations)







