from queue import Queue
import time

class Item:
    def __init__(self, level, weight, value, included_items):
        self.level = level
        self.weight = weight
        self.value = value
        self.included_items = included_items
     
def knapsackDFS(total_weight, items, size):
    max_profit = 0
    curr_weight = 0
    selected_items = []
    #we use a stack here since this allows us to traverse in a depth first manner by adding the left most child node first
    stack = [Item(-1, 0, 0, [])]
    while stack:
        #get the current node
        current_item = stack.pop()
        #if the node is a leaf we check if max_profit has been improved
        if current_item.level == size - 1:
            if current_item.value > max_profit and current_item.weight <= total_weight:
                max_profit = current_item.value
                curr_weight = current_item.weight  
                selected_items = current_item.included_items        
            continue
        next_item = items[current_item.level + 1]
        #we add the child node where we grab the item
        if current_item.weight + next_item.weight <= total_weight:
            included_items = current_item.included_items.copy()
            included_items.append(current_item.level + 2)
            stack.append(Item(current_item.level + 1, current_item.weight + next_item.weight, current_item.value + next_item.value, included_items))
        #we add the child node where we do not grab the item
        stack.append(Item(current_item.level + 1, current_item.weight, current_item.value, current_item.included_items))
    
    return max_profit, curr_weight, selected_items

def knapsackBFS(total_weight, items, size):
    max_profit = 0
    curr_weight = 0
    selected_items = []
    #we use a FIFO queue here since this allows us to traverse in a breadth first manner
    queue = Queue()
    queue.put(Item(-1, 0, 0, []))
    while not queue.empty():
        current_item = queue.get()
        #if we reach the bottom level or the current weight has equalled the total weight we break
        if current_item.level == size - 1:
            if current_item.value >= max_profit and current_item.weight <= total_weight:
                max_profit = current_item.value
                curr_weight = current_item.weight
                selected_items = current_item.included_items
            continue
        
        #we add the child node where we grab the item
        next_item_weight = current_item.weight + items[current_item.level + 1].weight
        next_item_value = current_item.value + items[current_item.level + 1].value
        if next_item_weight < total_weight:
            included_items = current_item.included_items.copy()
            included_items.append(current_item.level + 2)
            queue.put(Item(current_item.level + 1, next_item_weight, next_item_value, included_items))
            
        #we add the child node where we do not grab the item
        next_item_exclude = Item(current_item.level + 1, current_item.weight, current_item.value, current_item.included_items)  
        queue.put(next_item_exclude)
            
    return max_profit, curr_weight, selected_items

def read_items():    
    with open('C:/Users/oscar/OneDrive/Skrivbord/AI-Labs/Assignment-1/input_files/knapsack.txt', 'r') as file:
        for _ in range(6):
            next(file)
        lines = file.readlines()
        items = []
        for line in lines:
            if line.strip() == "EOF":
                break
            level, value, weight = map(int, line.split())
            items.append(Item((level - 1), weight, value, []))
    return items
      
weight = 420
items = read_items()


#BFS
start_time = time.time()
profit, knapsack_weight, selected_items = knapsackBFS(weight, items, len(items))
end_time = time.time()
time_taken = end_time - start_time
print("Calculated max profit for BFS:", profit, "Time taken:", time_taken, "Weight:", knapsack_weight)
print("Items selected:", selected_items)

#DFS
start_timeDFS = time.time()
profitDFS, knapsack_weightDFS, selected_items = knapsackDFS(weight, items, len(items))
end_timeDFS = time.time()
time_takenDFS = end_timeDFS - start_timeDFS
print("Calculated max profit for DFS:", profitDFS, "Time taken:", time_takenDFS, "Weight:", knapsack_weightDFS)
print("Items selected:", selected_items)






