import numpy as np
import random as rand


class Ant:
    def __init__(self, num_cities):
        self.path = []
        self.unvisited = [i for i in range(0, num_cities)]
     
    def select_next_city(self, phermones, distances, current_city, unvisited_cities):
        selected_city = None
        total_probability = sum(((phermones[current_city][city]) ** alpha) * (((1.0 / distances[current_city][city]) ** beta) + 0.01) for city in unvisited_cities)
        probabilities = {}
        for city in unvisited_cities:    
            phermone_level = phermones[current_city][city]
            distance = distances[current_city][city]
            probability = (((phermone_level ** alpha) * ((1.0 / distance) ** beta)) / total_probability)
            probabilities[city] = probability
        selected_city = roulette_selection(probabilities)
        return selected_city
    
def roulette_selection(probabilities):
    selected_city = None
    total_probability = sum(probabilities.values())
    probability = rand.uniform(0, total_probability)
    cumu_probability = 0.0
    for p in probabilities:
        cumu_probability += probabilities[p]
        if cumu_probability >= probability:
            selected_city = p
            return selected_city
    return None


        
def calc_distance(city1, city2):
    (x1, y1) = city1
    (x2, y2) = city2
    return np.sqrt((np.power(x2 - x1, 2)) + (np.power(y2 - y1, 2)))

def calc_total_distance(path):
    total_distance = 0
    for i in range(len(path)-1):
        total_distance += calc_distance(cities[path[i]], cities[path[i+1]])
    total_distance += calc_distance(cities[path[i+1]], cities[0])
    return total_distance
def calc_normalized_distance(city1, city2, max_distance):
    (x1, y1) = city1
    (x2, y2) = city2
    distance = np.sqrt((np.power(x2 - x1, 2)) + (np.power(y2 - y1, 2)))
    return distance / max_distance

def read_items():
    cities = {}
    with open('berlin52.tsp', 'r') as file:
        for _ in range(6):
            next(file)
        lines = file.readlines()
        i = 0
        for line in lines:
            if line.strip() == "EOF":
                break
            coord = line.split()
            (x,y) = (float(coord[1]), float(coord[2]))
            cities[int(coord[0])-1] = (x, y)
            i += 1
    return cities        
            
def init_tables(cities, phermone_value, max_distance):            
    phermone_table = [[None for _ in range(len(cities))] for _ in range(len(cities))]
    distance_table = [[None for _ in range(len(cities))] for _ in range(len(cities))]
    #calculate max_distance to normalize 
    for i in cities:
        for j in cities:
            distance = calc_distance(cities[i], cities[j])
            if distance > max_distance:
                max_distance = distance
    #create phermone and distance tables
    for i in range(len(cities)):
        for j in range(len(cities)):
            if i == j:
                phermone_table[i][j] = None
            else:
                phermone_table[i][j] = phermone_value
            distance_table[i][j] = calc_normalized_distance(cities[i], cities[j], max_distance)
            distance_table[i][j] = calc_normalized_distance(cities[j], cities[i], max_distance)
    return phermone_table, distance_table

def update_pheromone_levels(p_levels, evap_rate, ants):
    for i in range(len(cities)):
        for j in range(len(cities)):
            if p_levels[i][j] == None:
                continue
            else:
                p_levels[i][j] -= evap_rate
    for ant in ants:
        for i in range(len(ant.path)-1):
            p_levels[ant.path[i]][ant.path[i+1]] += deposition_value
        p_levels[ant.path[i+1]][ant.path[0]] += deposition_value
        
        
def run_aco(phermone_table, distances, ant_amount, iterations, evaporation):
    best_path = None
    best_distance = float('inf')
    for _ in range(iterations):
        ants = [Ant(len(cities)) for _ in range(ant_amount)]
        print("")
        for ant in ants:
            current_city = 0
            while len(ant.unvisited) > 0:
                ant.path.append(current_city)
                ant.unvisited.remove(current_city)
                if not ant.unvisited:
                    print("")
                next_city = ant.select_next_city(phermone_table, distances, current_city, ant.unvisited)
                current_city = next_city
                print("Ant searching...")
        print("Ant done...")
        for ant in ants:
            path = ant.path
            total_distance = calc_total_distance(path)
            if best_distance > total_distance:
                best_path = path
                best_distance = total_distance         
        update_pheromone_levels(phermone_table, evaporation, ants)
        print("Updating pheromones...")
    return best_distance, best_path


cities = read_items()
alpha = 3
beta = 2
phermone_value = 1.0
evaporation_rate = 0.8
deposition_value = 2
ant_amount = 52
iterations = 10
phermone_table, distance_table = init_tables(cities, phermone_value, max_distance=0.0)
distance, path = run_aco(phermone_table, distance_table, ant_amount, iterations, evaporation_rate)
print("Distance:", distance)
print("Path:", path)

