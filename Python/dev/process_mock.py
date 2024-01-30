import socket
import time


def send_number_to_server(number):
    try:
        # Establishing connection with the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 9999))

        # Sending the chosen number to the server
        client_socket.sendall(str(number).encode())

        # Closing the connection
        client_socket.close()
        print(f"Number {number} sent to server successfully.")

    except Exception as e:
        print(f"Error in sending number to server: {e}")

def test_process():
    time.sleep(2)
    print("HI")
    send_number_to_server(1)
    time.sleep(5)
    send_number_to_server(2)
    time.sleep(10)
    send_number_to_server(3)
    time.sleep(2)
    send_number_to_server(4)
    time.sleep(45)
    send_number_to_server(4)

if __name__ == '__main__':
    test_process()
