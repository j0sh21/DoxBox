import requests
import time
import threading
import socket
#import img_capture as capture

# Existing variables and functionalities

inKey = '74001006d12743e1a1f5ac3eea8def9c'
apiUrl = 'http://lnbits.twnty.one/api/v1/payments?limit=1'

def send_message_to_app(message):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 9999))
        client_socket.sendall(message.encode())
        client_socket.close()
    except Exception as e:
        print(f"Error in sending message to app: {e}")

def main_loop():
    prevHash = ''
    currHash = ''
    rsJson = ''
    response = requests.get(apiUrl, headers={'X-API-Key': inKey})
    prevHash = response.json()[0]['payment_hash']
    response = None

    while True:
        response = requests.get(apiUrl, headers={'X-API-Key': inKey})
        if (response.status_code == 200):
            rsJson = response.json()

            currHash = rsJson[0]['payment_hash']

            if (currHash != prevHash):
                prevHash = currHash

                amount = rsJson[0]['amount'] / 1000  # Amount in SATS

                if (amount == 1.00):
                    print("Starting DoxBox")
                    send_message_to_app("1")
                    # capture.main()
                    time.sleep(50)
                else:
                    time.sleep(5)
            else:
                time.sleep(5)
        else:
            exit(response.status_code)

        # Example of sending a message to app.py
        # send_message_to_app("Update from switch.py")

if __name__ == '__main__':
    main_thread = threading.Thread(target=main_loop)
    main_thread.start()
