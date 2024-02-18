import socket

def run_client(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the server
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        while True:
            # Prompt the user for a command
            command = input("Enter command (or 'exit' to quit): ")
            if command.lower() == 'exit':
                break

            # Send the command to the server
            client_socket.sendall(command.encode('utf-8'))

if __name__ == "__main__":
    HOST, PORT = '127.0.0.1', 12345  # Change host and port if needed
    run_client(HOST, PORT)
