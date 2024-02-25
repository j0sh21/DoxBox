import socket

def run():
    print(f"Server listening on {host}:{port}")
    while True:
        client_socket, address = server_socket.accept()
        handle_client(client_socket)

def handle_client(client_socket):
    with client_socket:
        while True:
            msg = client_socket.recv(1024).decode('utf-8')
            if not msg:
                break
            print(f"{msg}")


if __name__ == '__main__':
    host='localhost'
    port=6548

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()
    run()