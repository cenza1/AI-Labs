import sudoku_answers as solution
import time
#Reads sudoku grids, returns them in an array
def read_items():
    grid_array = []
    with open('C:/Users/oscar/OneDrive/Skrivbord/AI-Labs/Assignment-2/input_files/sudoku.txt', 'r') as file:
        for _ in range(4):
            next(file)
        lines = file.readlines()
        for line in lines:
            if line.strip()[:6] == "SUDOKU":
                row, col = (9, 9)
                grid = [[0]*col for _ in range(row)]
                for row in grid:
                    for col in range(len(row)):
                        row[col] = 0
                row_num = 0
                col_num = 0
                continue
            if line.strip() == "": 
                grid_array.append(grid)
                continue
            if line.strip() == "EOF":
                break
            rowN = list(line.strip())
            for num in rowN:
                grid[row_num][col_num] = int(num)
                col_num += 1
            row_num += 1
            col_num = 0
    return grid_array

#Searches for an empty cell and returns its coordinates
def find_empty_cell(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return row, col
    return -1, -1

#Checks if a certain number is a valid move
def is_valid_move(grid, row, col, num):
    
    #Check if the number already exists in the 3x3 sub-grid
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == num:
                return False
    #Check if the number already exists horizontally
    for i in range(0, col):
        if grid[row][i] == num:
            return False
    for i in range(8, col, -1):
        if grid[row][i] == num:
            return False
    #Check if the number already exists vertically
    for j in range(0, row):
        if grid[j][col] == num:
            return False
    for j in range(8, row, -1):
        if grid[j][col] == num:
            return False
        
    return True         
            

#Responsible for solving the sudoku, takes in the sudoku grid and its index.
#The function uses recursion to perform a dfs
def solve(grid, index):
    row, col = find_empty_cell(grid)
    if (row, col) == (-1, -1):
        return confirm_solved(grid, index)
    
    for num in range(10):
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num
            if solve(grid, index) == True:
                return True
            else:
                grid[row][col] = 0
    
    return False
        
        
#Confirm grid is the equal to the solution string in the sudoku_answers file
def confirm_solved(grid, index):
    flatten_grid = [element for row in grid for element in row]  
    solution_string = ''.join(map(str, flatten_grid))
    if solution_string == solution.solutions[index]:
        return True
    else:
        return False
     
        
grids = read_items()
sudoku_n = 0
start_time = time.time()
for grid in grids:
    is_solved = solve(grid, sudoku_n)
    if is_solved == True:
        print("Sudoku number", sudoku_n + 1, "has been solved")
    else:
        print("Sudoku number", sudoku_n, "has not been solved")
    sudoku_n += 1
end_time = time.time()
total_time = end_time - start_time
print("Time taken: ", total_time)

