import socket
import signal
import sys
import numpy as np
from mazelib import Maze
from mazelib.generate.Prims import Prims
from mazelib.solve.BacktrackingSolver import BacktrackingSolver

MAZE_HEIGHT = 10
MAZE_WIDTH = 20

def generate_maze(width, height):
    """Generates a new maze using the Prims algorithm."""
    m = Maze()
    m.generator = Prims(width, height)
    m.generate()
    m.generate_entrances()
    return m

def maze_to_ascii(m):
    """Converts the Maze object to an ASCII representation."""
    maze_str = ""
    for y, row in enumerate(m.grid):
        for x, cell in enumerate(row):
            if (y, x) == m.start:
                maze_str += 'S'  # Entrance
            elif (y, x) == m.end:
                maze_str += 'E'  # Exit
            elif cell == 1:
                maze_str += '#'  # Wall
            else:
                maze_str += ' '  # Path
        maze_str += '\n'
    return maze_str

def calculate_solution(maze):
    """Calculates the solution path for the given maze and converts it to an ASCII representation."""
    maze.solver = BacktrackingSolver()
    maze.solve()  # Compute the solution
    
    # Convert solution path to ASCII representation
    solution_str = ""
    solution_set = set(maze.solution)  # Assuming maze.solution holds the path
    for y, row in enumerate(maze.grid):
        for x, cell in enumerate(row):
            if (y, x) == maze.start:
                solution_str += 'S'
            elif (y, x) == maze.end:
                solution_str += 'E'
            elif (y, x) in solution_set:
                solution_str += '.'
            elif cell == 1:
                solution_str += '#'
            else:
                solution_str += ' '
        solution_str += '\n'
    
    return solution_str.strip()

def receive_full_response(client_socket):
    """Receives all data from the socket until the connection is closed."""
    response = b''
    while True:
        part = client_socket.recv(4096)
        if not part:
            break
        response += part
    return response.decode('utf-8').strip()

def handle_client(client_socket):
    """Handles a client connection by sending a maze and waiting for a solution response."""
    maze = generate_maze(MAZE_HEIGHT, MAZE_WIDTH)  # Generate a new maze
    print("Generated Maze:")
    print(maze_to_ascii(maze))  # Print the generated maze
    maze_ascii = maze_to_ascii(maze)  # Convert the maze to ASCII
    
    # Send the maze to the client
    client_socket.sendall(maze_ascii.encode('utf-8'))
    client_socket.sendall(b"\n3,2,1 solve it!\n")

    # Set a timeout for the response
    client_socket.settimeout(1.0)  # 2 seconds timeout
    
    try:
        # Receive the solution from the client
        response = receive_full_response(client_socket)
        print("Received Response:")
        print(response)  # Print the response received from the client
        
        solution_str = calculate_solution(maze)
        print("Calculated Solution:")
        print(solution_str)  # Print the calculated solution

        if response == solution_str:
            client_socket.sendall(b"CONGRATULATIONS THIS IS YOUR FLAG\n")
        else:
            client_socket.sendall(b"Incorrect solution. Try again.\n")
    except socket.timeout:
        client_socket.sendall(b"Too slow!\n")
    except Exception as e:
        print(f"Exception: {e}")
        client_socket.sendall(b"Something went wrong\n")

    finally:
        client_socket.close()


def serve_maze(host='0.0.0.0', port=9999):
    """Sets up a TCP server that sends a newly generated maze to each connected client."""
    def signal_handler(sig, frame):
        print("\nServer is shutting down.")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Listening on {host}:{port}")
        
        while True:
            try:
                client_socket, addr = server_socket.accept()
                print(f"Connected by {addr}")
                handle_client(client_socket)
            except KeyboardInterrupt:
                print("\nServer interrupted by user. Shutting down.")
                break

if __name__ == "__main__":
    serve_maze()
