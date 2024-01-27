import config
import requests
import time
import threading
import socket

def send_message_to_app(message):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((config.HOST, config.PORT))
        client_socket.sendall(message.encode())
        client_socket.close()
    except Exception as e:
        print(f"Error in sending message to app: {e}")

def main_loop():
    prevHash = ''
    currHash = ''
    rsJson = ''
    response = requests.get(config.API_URL, headers={'X-API-Key': config.API_KEY})
    prevHash = response.json()[0]['payment_hash']
    response = None

    while True:
        response = requests.get(config.API_URL, headers={'X-API-Key': config.API_KEY})
        if (response.status_code == 200):
            rsJson = response.json()

            currHash = rsJson[0]['payment_hash']

            if (currHash != prevHash):
                prevHash = currHash

                amount = rsJson[0]['amount'] / 1000  # Amount in SATS

                if (amount == config.AMOUNT_THRESHOLD):
                    print("Starting DoxBox")
                    send_message_to_app("1")
                    # capture.main()
                    time.sleep(config.POST_PAYMENT_DELAY)
                else:
                    time.sleep(config.CHECK_INTERVAL)
            else:
                time.sleep(config.CHECK_INTERVAL)
        else:
            exit(response.status_code)

        # Example of sending a message to app.py
        # send_message_to_app("Update from switch.py")

if __name__ == '__main__':
    main_thread = threading.Thread(target=main_loop)
    main_thread.start()
