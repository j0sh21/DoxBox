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
    response = requests.get(config.API_URL, headers={'X-API-Key': config.API_KEY})
    prevHash = response.json()[0]['payment_hash']
    response = None

    while True:
        print("Request LNbits API for new payments")
        response = requests.get(config.API_URL, headers={'X-API-Key': config.API_KEY})
        if (response.status_code == 200):
            rsJson = response.json()

            currHash = rsJson[0]['payment_hash']

            if (currHash != prevHash):
                prevHash = currHash

                amount = rsJson[0]['amount'] / 1000  # Amount in SATS

                if (amount == config.AMOUNT_THRESHOLD):
                    print("Sats recieved, sending msg = 1 to app.py!")
                    send_message_to_app("1")
                    time.sleep(config.POST_PAYMENT_DELAY)
                else:
                    time.sleep(config.CHECK_INTERVAL)
            else:
                time.sleep(config.CHECK_INTERVAL)
        else:
            exit(response.status_code)

if __name__ == '__main__':
    print("switch.py is now running.")
    main_thread = threading.Thread(target=main_loop)
    main_thread.start()
