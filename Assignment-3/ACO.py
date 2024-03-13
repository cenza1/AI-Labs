import numpy as np

class Node:
    
    def __init__(self, xCoord, yCoord, pheromone):
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.pheromone = pheromone
        
    def distance_to(self, other_node):
        (x1, y1) = (self.xCoord, self.yCoord)
        (x2, y2) = (other_node.xCoord, other_node.yCoord)
        return np.sqrt((np.power(x2 - x1, 2)) + (np.power(y2 - y1, 2)))

    def calc_normalized_distance(self, other_node):
        (x1, y1) = (self.xCoord, self.yCoord)
        (x2, y2) = (other_node.xCoord, other_node.yCoord)
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
            cities[int(coord[0])] = Node(x, y, 10)
            i += 1
    return cities


cities = read_items()
max_distance = 0.0
for i in cities:
    for j in cities:
        distance = cities[i].distance_to(cities[j])
        if distance > max_distance:
            max_distance = distance



