import subprocess
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

def check_connection():
    command = ['ping', '-c', '1', 'google.com']
    try:
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print("Connection check successful.")
        return True
    except subprocess.CalledProcessError:
        print("No Connection to the internet")
        return False

def main_loop():
    prevHash = ''
    currHash = ''
    rsJson = ''
    response = requests.get(config.API_URL, headers={'X-API-Key': config.API_KEY})
    prevHash = response.json()[0]['payment_hash']
    response = None

    while True:
        if check_connection():
            print("Polling LNbits API for new payments")
            response = requests.get(config.API_URL, headers={'X-API-Key': config.API_KEY})
            if (response.status_code == 200):
                rsJson = response.json()

                currHash = rsJson[0]['payment_hash']

                if (currHash != prevHash):
                    prevHash = currHash

                    amount = rsJson[0]['amount'] / 1000  # Amount in SATS

                    if (amount == config.AMOUNT_THRESHOLD):
                        print("Sats recieved! Sending msg = 1 to app.py!")
                        send_message_to_app("1")
                        time.sleep(config.POST_PAYMENT_DELAY)
                    else:
                        time.sleep(config.CHECK_INTERVAL)
                else:
                    time.sleep(config.CHECK_INTERVAL)
            else:
                print(f"LNbits API response status code: {response.status_code}")
                print(f"Polling LNbits API again in {config.CHECK_INTERVAL} seconds.")
                time.sleep(config.CHECK_INTERVAL)
        else:
            print(f"No Internet Connection, checking again in {config.CHECK_INTERVAL} seconds")
            time.sleep(config.CHECK_INTERVAL)
            if check_connection():
                print("Connection reestablished polling LNbits API")
            else:
                time.sleep(config.IMG_SLEEP_TIME_LONG)
                print(f"Sleeped {config.IMG_SLEEP_TIME_LONG+config.CHECK_INTERVAL} seconds. Try polling again...")


if __name__ == '__main__':
    print("switch.py is now running.")
    main_thread = threading.Thread(target=main_loop)
    main_thread.start()