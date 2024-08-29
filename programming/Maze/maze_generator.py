import socket
import signal
import sys
import numpy as np
from mazelib import Maze
from mazelib.generate.Prims import Prims
from mazelib.solve.BacktrackingSolver import BacktrackingSolver

MAZE_HEIGHT = 5
MAZE_WIDTH = 10

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
                with client_socket:
                    print(f"Connected by {addr}")
                    
                    # Generate a new maze for each client connection
                    maze = generate_maze(MAZE_HEIGHT, MAZE_WIDTH)  # You can adjust the maze size here
                    maze_ascii = maze_to_ascii(maze)
                    
                    # Send the maze to the client
                    client_socket.sendall(maze_ascii.encode('utf-8'))
                    client_socket.sendall(b"\nMaze sent. Connection will be closed.\n")
            except KeyboardInterrupt:
                print("\nServer interrupted by user. Shutting down.")
                break

if __name__ == "__main__":
    serve_maze()
