import subprocess
import config
import requests
import time
import threading
import socket


def send_message_to_mini_display(command):
    if config.DEBUG_MODE == 0:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(('localhost', 6548))
            client_socket.sendall(command.encode('utf-8'))
    else:
        print(command)

def send_message_to_app(message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((config.HOST, config.PORT))
            client_socket.sendall(message.encode())
    except socket.error as e:
        send_message_to_mini_display(f"Error in sending message to app: {e}")

def check_connection():
    command = ['ping', '-c', '1', 'google.com']
    try:
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        send_message_to_mini_display("Connection check successful.")
        return True
    except subprocess.CalledProcessError:
        send_message_to_mini_display("No Connection to the internet")
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
            send_message_to_mini_display("Polling LNbits API for new payments")
            response = requests.get(config.API_URL, headers={'X-API-Key': config.API_KEY})
            if (response.status_code == 200):
                rsJson = response.json()

                currHash = rsJson[0]['payment_hash']

                if (currHash != prevHash):
                    prevHash = currHash

                    amount = rsJson[0]['amount'] / 1000  # Amount in SATS

                    if (amount == config.AMOUNT_THRESHOLD):
                        send_message_to_mini_display("Sats recieved! Sending msg = 1 to app.py!")
                        send_message_to_app("1")
                        time.sleep(config.POST_PAYMENT_DELAY)
                    else:
                        time.sleep(config.CHECK_INTERVAL)
                else:
                    time.sleep(config.CHECK_INTERVAL)
            else:
                send_message_to_mini_display(f"LNbits API response status code: {response.status_code}")
                send_message_to_mini_display(f"Polling LNbits API again in {config.CHECK_INTERVAL} seconds.")
                time.sleep(config.CHECK_INTERVAL)
        else:
            send_message_to_mini_display(f"No Internet Connection, checking again in {config.CHECK_INTERVAL} seconds")
            time.sleep(config.CHECK_INTERVAL)
            if check_connection():
                send_message_to_mini_display("Connection reestablished polling LNbits API")
            else:
                time.sleep(config.IMG_SLEEP_TIME_LONG)
                send_message_to_mini_display(f"Sleeped {config.IMG_SLEEP_TIME_LONG+config.CHECK_INTERVAL} seconds. Try polling again...")


if __name__ == '__main__':
    send_message_to_mini_display("switch.py is now running.")
    main_thread = threading.Thread(target=main_loop)
    main_thread.start()