import socket
import numpy as np
from mazelib import Maze
from mazelib.solve.BacktrackingSolver import BacktrackingSolver

def receive_maze_and_send_solution(host='localhost', port=9998):
    """Connects to the server, receives the maze, solves it, and sends the solution back."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            # Connect to the server
            client_socket.connect((host, port))

            # Receive the maze from the server
            maze_data = b''
            while True:
                part = client_socket.recv(4096)
                print(part)
                if not part:
                    break
                maze_data += part

            # Decode the maze data
            maze_lines = maze_data.decode('utf-8').strip().splitlines()

            # Filter out non-maze lines
            maze_lines = [line for line in maze_lines if line.strip() and not line.startswith('Maze sent')]

            # Solve the maze
            solution = solve_maze(maze_lines)

            # Convert the solution to string and add \r\n at the end of each line
            solution_str = solution.tostring(True, True)  # Use maze.tostring() format
            solution_with_crlf = '\r\n'.join(solution_str.splitlines()) + '\r\n'
            print("SENDING> ")
            print(solution_with_crlf)
    
            client_socket.sendall(solution_with_crlf.encode('utf-8'))
            response = client_socket.recv(4096)

            for line in solution_with_crlf: 
                print(line)
                client_socket.sendall(line.encode('utf-8'))

            # Receive and print the response from the server
            response = b''
            while True:
                part = client_socket.recv(4096)
                if not part:
                    break
                response += part
            print("Server Response:", response.decode('utf-8'))

        except ConnectionError as e:
            print(f"Error connecting to the server: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def is_valid_maze_line(line):
    """Determines if a line is a valid part of the maze (contains only maze characters)."""
    return all(char in ' #SE' for char in line)

def ascii_to_maze(ascii_maze):
    """Converts ASCII maze representation to a Maze object."""
    grid = []
    start = None
    end = None

    # Filter valid maze lines
    filtered_lines = [line for line in ascii_maze if is_valid_maze_line(line)]

    if not filtered_lines:
        raise ValueError("No valid maze lines found")

    max_width = max(len(line) for line in filtered_lines)  # Find the maximum width
    
    for y, line in enumerate(filtered_lines):
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
    """Solves the maze using BacktrackingSolver and returns the solution as a Maze object."""
    grid_array, start, end = ascii_to_maze(maze_ascii)

    maze = Maze()
    maze.grid = grid_array
    maze.start = start
    maze.end = end

    print("MAZE RECEIVED....")
    print(maze)

    # Solve the maze
    maze.solver = BacktrackingSolver()
    maze.solve()

    print("\n\nMAZE SOLUTION....")
    print(maze)

    return maze  # Return the maze object containing the solution as a string

if __name__ == "__main__":
    receive_maze_and_send_solution('localhost', 9998)
