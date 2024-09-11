import socket
import numpy as np
from mazelib import Maze
from mazelib.solve.BacktrackingSolver import BacktrackingSolver

def send_test_message(server_host='4.175.193.106', server_port=9999):
    """Envía un mensaje de prueba al servidor."""
    try:
        # Crear un socket TCP/IP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Conectar al servidor
            client_socket.connect((server_host, server_port))
            print(f"Connected to server at {server_host}:{server_port}")

            # Esperar y recibir la respuesta del servidor
            maze_data = client_socket.recv(4096)
            print(f"RECEIVED>\n{maze_data.decode('utf-8', errors='ignore')}")

            # Decode the maze data
            maze_lines = maze_data.decode('utf-8').strip().splitlines()
            maze_lines = [line for line in maze_lines if line.strip() and not line.startswith('Maze sent')]

            solution = solve_maze(maze_lines)

            print(f"SENT>\n{solution.tostring(True, True)}")
            client_socket.sendall(solution.tostring(True, True).encode("utf-8"))
            response = client_socket.recv(4096)
            print(f"RECEIVED>\n {response.decode('utf-8', errors='ignore')}")

    except Exception as e:
        print(f"Error: {e}")


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


if __name__ == "__main__":

    send_test_message()  # Mensaje simple