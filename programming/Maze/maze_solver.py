import socket
import numpy as np
from mazelib import Maze
from mazelib.solve.BacktrackingSolver import BacktrackingSolver

def receive_maze(host='localhost', port=9999):
    """Connects to the server, receives the maze, and returns it as ASCII lines."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host, port))
            data = b''
            while True:
                part = client_socket.recv(4096)
                if not part:
                    break
                data += part
            maze_lines = data.decode('utf-8').strip().splitlines()
            
            # Filter out non-maze lines (like 'Maze sent. Connection will be closed.')
            maze_lines = [line for line in maze_lines if line.strip() and not line.startswith('Maze sent')]
            
            return maze_lines
        except ConnectionError as e:
            print(f"Error connecting to the server: {e}")
            return None

def ascii_to_maze(ascii_maze):
    """Converts ASCII maze representation to a Maze object."""
    grid = []
    start = None
    end = None

    max_width = max(len(line) for line in ascii_maze)  # Find the maximum width

    for y, line in enumerate(ascii_maze):
        if len(line) != max_width:
            raise ValueError("Inconsistent row lengths in the maze")
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

def solve_maze(maze_ascii):
    """Solves the maze using BacktrackingSolver and prints both the original and solved maze."""
    grid_array, start, end = ascii_to_maze(maze_ascii)

    maze = Maze()
    maze.grid = grid_array
    maze.start = start
    maze.end = end

    # Print the original maze
    print("Original Maze:")
    for line in maze_ascii:
        print(line)

    # Solve the maze
    maze.solver = BacktrackingSolver()
    maze.solve()

    # Print the solved maze
    print("\nSolved Maze:")
    print(maze)
    
if __name__ == "__main__":
    ascii_maze = receive_maze('localhost', 9999)
    if ascii_maze:
        solve_maze(ascii_maze)
