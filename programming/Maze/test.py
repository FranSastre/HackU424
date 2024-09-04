import socket

def send_test_message(message, server_host='127.0.0.1', server_port=9998):
    """Envía un mensaje de prueba al servidor."""
    try:
        # Crear un socket TCP/IP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Conectar al servidor
            client_socket.connect((server_host, server_port))
            print(f"Connected to server at {server_host}:{server_port}")

            # Enviar el mensaje codificado
            client_socket.sendall(message.encode('utf-8'))
            print(f"SENT> {message}")

            # Esperar y recibir la respuesta del servidor
            response = client_socket.recv(4096)
            print(f"RECEIVED> {response.decode('utf-8', errors='ignore')}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Ejemplos de mensajes para enviar
    send_test_message("Hello, Server!")  # Mensaje simple
    send_test_message("This is a second test message!")  # Mensaje más largo
    send_test_message("1234567890" * 10)  # Mensaje más largo aún
    send_test_message("Special characters AAAAAAAAAAAAAh")  # Mensaje con caracteres especiales
