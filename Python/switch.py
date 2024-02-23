import config
import requests
import time
import threading
import socket

def send_message_to_app(message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((config.HOST, config.PORT))
            client_socket.sendall(message.encode())
    except socket.error as e:
        print(f"Error in sending message to app: {e}")

def main_loop():
    try:
        response = requests.get(config.API_URL, headers={'X-API-Key': config.API_KEY})
        prevHash = response.json()[0]['payment_hash']
    except requests.exceptions.RequestException as e:
        print(f"Initial request failed, maybe there is no payment_hash (e.g. brand new ln wallet): {e}")
        send_message_to_app("143")  #initialization failure, maybe there is no payment_hash (e.g. brand new ln wallet)
        return  # Exit if initial request fails

    while True:
        print("Polling LNbits API for new payments")
        try:
            wait = config.CHECK_INTERVAL
            response = requests.get(config.API_URL, headers={'X-API-Key': config.API_KEY})
            if (response.status_code == 200):
                rsJson = response.json()

                currHash = rsJson[0]['payment_hash']

                if (currHash != prevHash):
                    prevHash = currHash

                    amount = rsJson[0]['amount'] / 1000  # Amount in SATS

                    if (amount == config.AMOUNT_THRESHOLD):
                        print("Sats received! Sending message '1' to app.py and start DoxBox!")
                        send_message_to_app("1")
                        time.sleep(config.POST_PAYMENT_DELAY)
                    else:
                        print(f"{str(amount)} Sats received, but one photo costs {config.AMOUNT_THRESHOLD}.\n Since no refund is implemented yet, pleas try again...")
                        time.sleep(config.CHECK_INTERVAL)
                        send_message_to_app("144")
                else:
                    print(f"No payment received! Fetching LNbits API again in {wait} seconds...")
                    time.sleep(wait)
            else:
                print("Response status code is not 200")
                send_message_to_app("141")
                exit(response.status_code)
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error: {e}")
            wait = config.CHECK_INTERVAL * 2
            print(f"Sleep for {wait} seconds")
            send_message_to_app("142")
            time.sleep(wait)  # Wait a bit before retrying in case of connection error
        except Exception as e:
            print(f"Unexpected error: {e}")
            send_message_to_app("140")
            wait = config.CHECK_INTERVAL * 4
            print(f"Sleep for {wait} seconds")
            time.sleep(wait)  # Wait before retrying after an unexpected error


if __name__ == '__main__':
    print("switch.py is now running.")
    main_thread = threading.Thread(target=main_loop)
    main_thread.start()
