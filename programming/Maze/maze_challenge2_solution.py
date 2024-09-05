import socket

def send_test_message(message, server_host='127.0.0.1', server_port=9999):
    """Envía un mensaje de prueba al servidor."""
    try:
        # Crear un socket TCP/IP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Conectar al servidor
            client_socket.connect((server_host, server_port))
            print(f"Connected to server at {server_host}:{server_port}")

            # Esperar y recibir la respuesta del servidor
            response = client_socket.recv(4096)
            print(f"RECEIVED>\n{response.decode('utf-8', errors='ignore')}")
            response = client_socket.recv(4096)
            print(f"RECEIVED>\n{response.decode('utf-8', errors='ignore')}")

            print(f"SENT> {message}")
            client_socket.sendall(response)
            response = client_socket.recv(4096)
            print(f"RECEIVED>\n {response.decode('utf-8', errors='ignore')}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Ejemplos de mensajes para enviar

    solucion = """
#S#####
#+++# #
###+# #
#  +# #
###+# #
#+++  #
#E#####
"""

    send_test_message(solucion)  # Mensaje simple