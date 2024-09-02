import socket
import signal
import sys
import threading
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

def calculate_solution(maze):
    """Calculates the solution path for the given maze and converts it to an ASCII representation."""
    maze.solver = BacktrackingSolver()
    maze.solve()  # Compute the solution

def receive_full_response(client_socket):
    """Receives all data from the socket until the connection is closed or an end-of-message marker is received."""
    response = b''  # Buffer to hold the full response
    while True:
        try:
            part = client_socket.recv(4096)  # Receive up to 4096 bytes
            if not part:
                break  # Exit loop if no more data is received
            response += part  # Append received part to the response buffer

        except socket.timeout:
            print("Socket timeout reached, stopping reception")
            break

        except Exception as e:
            print(f"Error while receiving data: {e}")
            break
    
    # Decode the full response once all parts are received
    response_str = response.decode('utf-8', errors='ignore').strip()    
    return response_str

def handle_client(client_socket):
    """Handles a client connection by sending a maze and waiting for a solution response."""
    maze = generate_maze(MAZE_HEIGHT, MAZE_WIDTH)  # Generate a new maze
    calculate_solution(maze)

    print("Solved Maze:")
    print(maze.tostring(True, True))  # Print the solved maze

    # Send the maze to the client
    client_socket.sendall(maze.tostring(True, False).encode('utf-8'))
    client_socket.sendall(b"\n3,2,1 solve it!\n")

    # Set a timeout for the response
    client_socket.settimeout(10.0)  # Adjust as needed

    try:
        # Receive the solution from the client
        response = receive_full_response(client_socket)

        print("Received Response:")
        print(response)  # Print the response received from the client

        if response == maze.solutions:
            client_socket.sendall(b"CONGRATULATIONS THIS IS YOUR FLAG\n")
        else:
            client_socket.sendall(b"Incorrect solution. Try again.\n")

    except socket.timeout:
        try:
            client_socket.sendall(b"Too slow!\n")
        except BrokenPipeError:
            print("Client disconnected before receiving timeout message.")

    except BrokenPipeError:
        print("Client disconnected unexpectedly. Could not send message.")

    except Exception as e:
        print(f"Exception: {e}")
        try:
            client_socket.sendall(b"Something went wrong\n")
        except BrokenPipeError:
            print("Client disconnected before receiving error message.")

    finally:
        client_socket.close()

def serve_maze(host='0.0.0.0', port=9998):
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
                
                # Create a new thread to handle the client
                client_thread = threading.Thread(target=handle_client, args=(client_socket,))
                client_thread.start()
            except KeyboardInterrupt:
                print("\nServer interrupted by user. Shutting down.")
                break
            except Exception as e:
                print(f"Server encountered an error: {e}")

if __name__ == "__main__":
    serve_maze()
