import socket
import sys
import threading
import numpy as np
from mazelib import Maze
from mazelib.generate.Prims import Prims
from mazelib.solve.BacktrackingSolver import BacktrackingSolver

""" 
CHALLENGE 2 - I send you the solution and you send me it back
"""

MAZE_HEIGHT = 5
MAZE_WIDTH = 10

HOST = "0.0.0.0"
PORT = 9998

FLAG = "HACK4U{y34h_y0u_g0t_1t!}"
TIMEOUT = 10  # 10 seconds timeout


def generate_maze(width, height):
    """Generates a new maze using the Prims algorithm."""
    maze = Maze()
    maze.generator = Prims(height, width)
    maze.generate()
    maze.generate_entrances()

    maze.solver = BacktrackingSolver()
    maze.solve()

    return maze


def handle_client(client_socket, addr):
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
                maze = generate_maze(MAZE_WIDTH, MAZE_HEIGHT)

                # Send the unsolved maze
                print(f"SENDING>\n{maze.tostring(True, False)}")
                client_socket.sendall(maze.tostring(True, False).encode("utf-8"))

                # Send the solution
                print(f"SENDING>\n{maze.tostring(True, True)}")
                client_socket.sendall(maze.tostring(True, True).encode("utf-8"))

                # Receive the solution from the client
                solution_received = client_socket.recv(4096).decode('utf-8', errors='ignore')
                print(f"RECEIVED>\n{solution_received}")

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


def serve_maze(host=HOST, port=PORT):

    # Start the server and listen for connections
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Listening on {host}:{port}")

        while True:
            try:
                client_socket, addr = server_socket.accept()
                client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
                client_thread.start()

            except Exception as e:
                print(f"Error accepting connections: {e}")


if __name__ == "__main__":
    serve_maze()
