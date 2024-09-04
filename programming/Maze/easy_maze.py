import socket
import signal
import sys
import numpy as np
from mazelib import Maze
from mazelib.generate.Prims import Prims
from mazelib.solve.BacktrackingSolver import BacktrackingSolver

""" 
EASY CHALLENGE - ALWAYS THE SAME MAZE TO RESOLVE
"""

MAZE_HEIGHT = 3
MAZE_WIDTH = 3

HOST = "0.0.0.0"
PORT = 9999


def generate_maze(width, height):
    """Generates a new maze using the Prims algorithmaze."""
    maze = Maze()
    maze.set_seed(123)
    maze.generator = Prims(width, height)
    maze.generate()
    maze.generate_entrances()

    maze.solver = BacktrackingSolver()
    maze.solve()

    return maze


def serve_maze(maze, host=HOST, port=PORT):

    def signal_handler(sig, frame):
        print("\nServer is shutting down.")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Listening on {host}:{port}")

        client_socket, addr = server_socket.accept()

        with client_socket:
            print(f"Connected by {addr}")

            while True:
                client_socket.sendall(maze)
                data = client_socket.recv(4096)

                if not data:
                    break
                client_socket.sendall(data)

    


if __name__ == "__main__":
    mazeString = generate_maze(MAZE_WIDTH, MAZE_HEIGHT)

    serve_maze(mazeString.tostring(True, False))

    print(mazeString.tostring(True, False))
    print(mazeString.tostring(True, True))


