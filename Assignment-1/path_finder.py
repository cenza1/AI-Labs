import queue

def shortest_path_gbf(start, goal, graph, heuristic_distances):
    shortest_path = []
    path_distance = 0
    next_cities = queue.PriorityQueue()
    next_cities.put((0, start))
    while not next_cities.empty():
        current_distance, current_city = next_cities.get()
        shortest_path.append(current_city)
        path_distance += current_distance
        
        if current_city == goal:
            return path_distance, shortest_path
        #Loop through all of a city's neighbours and calculate their heuristic distance to the goal
        #Add the neighbours to the priority queue, the city with the shortest distance to the goal will get added to the front of the queue
        for neighbour, _ in graph[current_city]:
            heuristic = heuristic_distances[neighbour]
            next_cities.put((heuristic, neighbour))
                  
    return 0, []

#FIX Leave comments and fix better return values
def shortest_path_aStar(start, goal, graph, heuristic_distances):
    next_cities = queue.PriorityQueue()
    next_cities.put((0, start))
    visited_cities = {start: 0}
    #parent is used to track back and find the optimal path to print
    parent = {start: (None, 0)}
    
    while not next_cities.empty():
        current_distance, current_city = next_cities.get()       
        if current_city == goal:
            #When we have found the goal we recontruct the shortest path and its distance
            path = []
            tot_distance = 0
            while current_city is not None:
                path.insert(0, current_city)
                current_city, dist = parent[current_city]
                tot_distance += dist
            return tot_distance, path
            
        
        #Loop through all neighbours and calculate their total cost, if a neighbour has already been visited but another path grants less total cost we replace it
        #If a neighbour has already been visited but the total cost is not less we skip it
        for neighbour, distance in graph[current_city]:
            heuristic = heuristic_distances[neighbour]
            #total cost includes the heuristic distance, the current distance traveled and the distance to travel in order to get to the neighbour
            total_cost = current_distance + distance + heuristic
            
            if neighbour not in visited_cities or total_cost < visited_cities[neighbour]:
                visited_cities[neighbour] = total_cost
                parent[neighbour] = current_city, distance
                next_cities.put((total_cost, neighbour)) 
                
        
            
      
    return 0, []


with open('C:/Users/oscar/OneDrive/Skrivbord/AI-Labs/Assignment-1/input_files/spain_map.txt', 'r') as file:
    for _ in range(4):
        next(file)
    lines = file.readlines()
#Create and fill dictionaries for the city graph and the heuristic distance between cities
city_graph = {}
heuristic_distances = {}

for line in lines:
    if line.strip() == "Straight line Distances (to valladolid)":
        continue
    if len(line.strip().split()) == 3:
        city1, city2, distance = line.strip().split()
        distance = int(distance)
        city_graph.setdefault(city1, []).append((city2, distance))
        city_graph.setdefault(city2, []).append((city1, distance))
    else:
        city, distance = line.strip().split()
        distance = int(distance)
        heuristic_distances[city] = distance


start_city = "Malaga"
goal_city = "Valladolid"

#Astar
result, visited_cities = shortest_path_aStar(start_city, goal_city, city_graph, heuristic_distances)
if (result, visited_cities) == (0, []):
    print("No path to the goal was found")
print("Astar")
for city in visited_cities:
    print(city, "-->", end="",)
print("Total distance:", result)

#GBF
result, visited_cities = shortest_path_gbf(start_city, goal_city, city_graph, heuristic_distances)
if (result, visited_cities) == (0, []):
    print("No path to the goal was found")
print("GBF")
for city in visited_cities:
    print(city, "-->", end="",)
print("Total distance:", result)

    



    
    
        
        
    