import socket
import sys
import threading
import numpy as np
from mazelib import Maze
from mazelib.generate.Prims import Prims
from mazelib.solve.BacktrackingSolver import BacktrackingSolver

"""
CHALLENGE 1 - ALWAYS THE SAME MAZE TO RESOLVE
"""

MAZE_HEIGHT = 3
MAZE_WIDTH = 3

HOST = "0.0.0.0"
PORT = 9997
FLAG = "HACK4U{3zy_p1zy_m4z3}"
TIMEOUT = 60  # 1-minute timeout


def generate_maze(width, height):
    """Generates a new maze using the Prims algorithm."""
    maze = Maze()
    maze.set_seed(123)
    maze.generator = Prims(width, height)
    maze.generate()
    maze.generate_entrances()

    maze.solver = BacktrackingSolver()
    maze.solve()

    return maze


def handle_client(client_socket, addr, maze):
    """Handles communication with a client."""
    
    # Function to disconnect the client due to timeout
    def disconnect_client():
        print(f"Connection with {addr} timed out.")
        client_socket.sendall("Connection timed out!".encode('utf-8'))
        client_socket.close()

    # Start the timeout timer
    timer = threading.Timer(TIMEOUT, disconnect_client)
    timer.start()

    try:
        print(f"Connected by {addr}")
        while True:
            try:
                # Send the maze
                print(f"SENDING>\n{maze.tostring(True, False)}")
                client_socket.sendall(maze.tostring(True, False).encode("utf-8"))

                # Receive the solution from the client
                solution_received = client_socket.recv(4096).decode('utf-8', errors='ignore')
                print(f"RECEIVED>\n {solution_received}")

                # Reset the timeout timer after receiving data from the client
                timer.cancel()  # Cancel the current timer
                timer = threading.Timer(TIMEOUT, disconnect_client)  # Restart the timer
                timer.start()

                # Check if the solution is correct
                if solution_received.replace("\n", "") == maze.tostring(True, True).replace("\n", ""):
                    client_socket.sendall(FLAG.encode('utf-8'))
                    break  # Exit the loop after a successful response
                else:
                    client_socket.sendall("WRONG! TRY AGAIN :)".encode('utf-8'))

            except Exception as e:
                print(f"Error during communication: {e}")
                break  # Exit the loop in case of an error

    finally:
        # Stop the timer and close the socket
        timer.cancel()
        client_socket.close()


def serve_maze(maze, host=HOST, port=PORT):

    def signal_handler(sig, frame):
        print("\nServer is shutting down.")
        sys.exit(0)

    # Start the server and listen for connections
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Listening on {host}:{port}")

        while True:
            try:
                client_socket, addr = server_socket.accept()
                client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, maze))
                client_thread.start()

            except Exception as e:
                print(f"Error accepting connections: {e}")


if __name__ == "__main__":
    maze = generate_maze(MAZE_WIDTH, MAZE_HEIGHT)
    serve_maze(maze)
