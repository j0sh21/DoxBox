import socket

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

if __name__ == '__main__':
    while True:
        user_input = input("Enter a number to send to the server (0-100) or type 'exit', 'stop', or 'shutdown' to quit: ").strip().lower()

        # Check for exit keywords
        if user_input in ["exit", "stop", "shutdown","leave","back", "b"]:
            print("Exiting the program.")
            break

        try:
            # Ensuring the input is a number and within the specified range
            number = int(user_input)
            if 0 <= number <= 100:
                send_number_to_server(number)
            else:
                print("Please enter a number between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a numeric value or an exit keyword.")
