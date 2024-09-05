import socket
import signal
import sys
import numpy as np
from mazelib import Maze
from mazelib.generate.Prims import Prims
from mazelib.solve.BacktrackingSolver import BacktrackingSolver

""" 
CHALLENGE 2 - I send you the solution and you send me it back
"""

MAZE_HEIGHT = 3
MAZE_WIDTH = 3

HOST = "0.0.0.0"
PORT = 9999

FLAG = "HACK4U{3zy_p1zy_m4z3}"


def generate_maze(width, height):
    """Generates a new maze using the Prims algorithm."""
    maze = Maze()
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

        while True:
            try:
                client_socket, addr = server_socket.accept()
                with client_socket:
                    print(f"Connected by {addr}")

                    while True:
                        try:
                            print(f"SENDING>\n{maze.tostring(True, False)}")
                            client_socket.sendall(maze.tostring(True, False).encode("utf-8"))
                            print(f"SENDING>\n{maze.tostring(True, True)}")
                            client_socket.sendall(maze.tostring(True, True).encode("utf-8"))

                            solution_received = client_socket.recv(4096).decode('utf-8', errors='ignore')
                            print(f"RECEIVED>\n {solution_received}")

                            if solution_received.replace("\n", "") == maze.tostring(True, True).replace("\n", ""):
                                client_socket.sendall(FLAG.encode('utf-8'))
                                break  # Exit the loop after successful response

                            else: 
                                client_socket.sendall("WRONG! TRY AGAIN :)".encode('utf-8'))
                        
                        except Exception as e:
                            print(f"Error during communication: {e}")
                            break  # Exit the inner loop if there's an error

            except Exception as e:
                print(f"Error accepting connections: {e}")


if __name__ == "__main__":

    maze = generate_maze(MAZE_WIDTH, MAZE_HEIGHT)
    serve_maze(maze)
