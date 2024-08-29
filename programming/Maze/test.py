from mazelib import Maze 
from mazelib.generate.Prims import Prims 
from mazelib.solve.BacktrackingSolver import BacktrackingSolver 
import numpy as np 
 
# Function to generate the maze 
def generate_maze(width, height): 
    m = Maze() 
    m.generator = Prims(width, height) 
    m.generate() 
    m.generate_entrances() 
 
    print("\n\n GENERATED MAZE") 
    print(m) 
    solve_maze(m)
    return m 
 
def solve_maze(m): 
    m.solver = BacktrackingSolver()
    m.solve() 
    print("\n\nSolution") 
    print(m) 
 
 
def create_maze_from_ascii(ascii_maze): 
    grid_array, start, end = ascii_to_maze(ascii_maze) 
     
    mazeAscii = Maze()
    #mazeAscii.generate_entrances()
    mazeAscii.grid = grid_array
    mazeAscii.start = start
    mazeAscii.end = end

    print("\n\nAAAAA")
    print(mazeAscii)

    mazeAscii.solver = BacktrackingSolver()
    mazeAscii.solve() 

    print("\n\nBBBBBBB")
    print(mazeAscii)

    return mazeAscii
 
def ascii_to_maze(ascii_maze): 
    grid = [] 
    start = None 
    end = None 
 
    for y, line in enumerate(ascii_maze): 
        row = [] 
        for x, char in enumerate(line): 
            if char == '#': 
                row.append(1)  # Wall 
            elif char == ' ': 
                row.append(0)  # Path 
            elif char == 'S': 
                row.append(1)  # Path (entrance) 
                start = (y, x) 
            elif char == 'E': 
                row.append(1)  # Path (exit) 
                end = (y, x) 
        grid.append(row) 
     
    grid_array = np.array(grid, dtype=np.int8) 
     
    if start is None or end is None: 
        raise ValueError("Start or End position not found in the maze") 
     
    return grid_array, start, end 
 
if __name__ == "__main__": 
    # Generate and print the maze 
    maze = generate_maze(3, 3) 
 
    ascii_maze = [ 
        "#E#####", 
        "#     #", 
        "# ### #", 
        "#   # #", 
        "##### #", 
        "#     #", 
        "###S###" 
    ] 
     
    # Create Maze object from ASCII 
    create_maze_from_ascii(ascii_maze)