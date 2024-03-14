import numpy as np

ALPHA = 0.9
BETA = 1.5 
class Ant:
    def __init__(self, num_cities):
        self.path = []
        self.visited = [False]*num_cities
     
    def select_next_city(self, phermones, distances):
        next_city = 0
        if not self.path:
            current_city = 0
        else:    
            current_city = self.path.pop()
        total_probability = sum(phermones[current_city][city] * (1.0 / distances[current_city][city]) for city in cities if city != current_city)
        probabilities = {}
        for city in cities:
            if city != current_city:
                phermone_level = phermones[current_city][city]
                distance = distances[current_city][city]
                probability = (phermone_level * (1.0 / distance)) / total_probability
                probabilities[city] = probability
        for city, probability in probabilities.items():
            print(city, probability)
                
            
        print("AAAAAAAAAAAAAAAAAA")
        return next_city
        
def calc_distance(city1, city2):
    (x1, y1) = city1
    (x2, y2) = city2
    return np.sqrt((np.power(x2 - x1, 2)) + (np.power(y2 - y1, 2)))

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
                phermone_table[i][j] = -1
            else:
                phermone_table[i][j] = phermone_value
            distance_table[i][j] = calc_normalized_distance(cities[i], cities[j], max_distance)
            distance_table[i][j] = calc_normalized_distance(cities[j], cities[i], max_distance)
    return phermone_table, distance_table


def run_aco(phermone_table, distances, ant_amount, iterations, evaporation):
    best_path = []
    best_distance = 0
    for iteration in range(iterations):
        ants = [Ant(len(cities)) for _ in range(ant_amount)]
        for ant in ants:
            current_path = []
            current_distance = 0
            while not all(ant.visited):
                next_city = ant.select_next_city(phermone_table, distances)
            
        
        if current_distance < best_path:
            best_path = current_path
    return best_path

cities = read_items()
phermone_value = 10
evaporation_rate = 0.01
ant_amount = len(cities)
iterations = 10
phermone_table, distance_table = init_tables(cities, phermone_value, max_distance=0.0)
run_aco(phermone_table, distance_table, ant_amount, iterations, evaporation_rate)

