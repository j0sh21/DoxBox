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
    prevHash = ''
    currHash = ''
    rsJson = ''
    try:
        response = requests.get(config.API_URL, headers={'X-API-Key': config.API_KEY})
        prevHash = response.json()[0]['payment_hash']
        response = None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching initial payment hash: {e}")
        return

    while True:
        try:
            print("Polling LNbits API for new payments")
            response = requests.get(config.API_URL, headers={'X-API-Key': config.API_KEY})
            if response.status_code == 200:
                rsJson = response.json()
                currHash = rsJson[0]['payment_hash']
                if currHash != prevHash:
                    prevHash = currHash
                    amount = rsJson[0]['amount'] / 1000
                    if amount == config.AMOUNT_THRESHOLD:
                        print(f"{amount} Sats received! Sending message '1' to app.py")
                        send_message_to_app("1")
                        time.sleep(config.POST_PAYMENT_DELAY)
                    else:
                        print(f"{str(amount)} Sats received, but one photo costs {config.AMOUNT_THRESHOLD}.\n Since no refund is implemented yet, pleas try again...")
                        time.sleep(config.CHECK_INTERVAL)
                        send_message_to_app("144")
                else:
                    print(f"No payment received! Fetching LNbits API again in {config.CHECK_INTERVAL} seconds...")
                    time.sleep(config.CHECK_INTERVAL)
            else:
                print(f"Failed to poll LNbits API: {response.status_code}")
                send_message_to_app("141")
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}")

        time.sleep(config.CHECK_INTERVAL)

if __name__ == '__main__':
    print("Starting the main loop")
    main_thread = threading.Thread(target=main_loop)
    main_thread.start()
