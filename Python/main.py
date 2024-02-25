import threading
import subprocess
import config
import socket

def send_message_to_mini_display(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('localhost', 6548))
        client_socket.sendall(command.encode('utf-8'))

def run_app():
    send_message_to_mini_display("Start APP SERVER")
    subprocess.run(["python3", "app.py"])

def start_led():
    try:
        subprocess.run(['sudo', 'pigpiod'])
        send_message_to_mini_display("pigpiod gestartet.")
    except Exception as e:
        send_message_to_mini_display("Fehler beim Starten von pigpiod:", e)

    send_message_to_mini_display("Start LED SERVER")
    subprocess.run(["python3", "led.py"])

def run_process_mock():
    send_message_to_mini_display("Start process_mock CLIENT")
    subprocess.run(["python3", "./dev/process_mock.py"])

def main():
    # Starting app.py in a separate thread
    app_thread = threading.Thread(target=run_app)
    app_thread.start()

    led_thread = threading.Thread(target=start_led)
    led_thread.start()

    if DEBUG in(1,2):
        send_message_to_mini_display("Start DEBUG CLIENT")
        subprocess.run(["python3", r"./dev/debug_client.py"])
    if DEBUG == 2:
        app_thread2 = threading.Thread(target=run_process_mock())
        app_thread2.start()
        send_message_to_mini_display("Start debug process without payment and printing")
    else:
        send_message_to_mini_display("Start BTC-SWITCH CLIENT")
        subprocess.run(["python3", "switch.py"])


if __name__ == "__main__":
    DEBUG = config.DEBUG_MODE  # Set to True to run debug_client.py instead of switch.py
    send_message_to_mini_display("Starting DoxBox...")
    main()
