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

def print_pic():
    print("Start printer mock")
    time.sleep(45)
    print("printing simulation finished!")
    send_number_to_server(5)

if __name__ == '__main__':
    print_pic()