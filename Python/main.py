import threading
import subprocess
import config

def run_app():
    print("Start APP SERVER")
    subprocess.run(["python3", "app.py"])

def start_led():
    try:
        subprocess.run(['sudo', 'pigpiod'])
        print("pigpiod gestartet.")
    except Exception as e:
        print("Fehler beim Starten von pigpiod:", e)

    print("Start LED SERVER")
    subprocess.run(["python3", "led.py"])

def run_process_mock():
    print("Start process_mock CLIENT")
    subprocess.run(["python3", "./dev/process_mock.py"])

def main():
    # Starting app.py in a separate thread
    app_thread = threading.Thread(target=run_app)
    app_thread.start()

    led_thread = threading.Thread(target=start_led)
    led_thread.start()

    if DEBUG in(1,2):
        print("Start DEBUG CLIENT")
        subprocess.run(["python3", r"./dev/debug_client.py"])
    if DEBUG == 2:
        app_thread2 = threading.Thread(target=run_process_mock())
        app_thread2.start()
        print("Start debug process without payment and printing")
    else:
        print("Start BTC-SWITCH CLIENT")
        subprocess.run(["python3", "switch.py"])


if __name__ == "__main__":
    DEBUG = config.DEBUG_MODE  # Set to True to run debug_client.py instead of switch.py
    print("Starting DoxBox...")
    main()
