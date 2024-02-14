import socket

def send_msg_to_LED(host, port, command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the server
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        while True:
            if command.lower() == 'exit':
                break

            # Send the command to the server
            client_socket.sendall(command.encode('utf-8'))

if __name__ == "__main__":
    HOST, PORT = '127.0.0.1', 12345  # Change host and port if needed
    send_msg_to_LED(HOST, PORT)

