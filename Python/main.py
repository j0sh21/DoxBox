import threading
import subprocess
import config

DEBUG = config.DEBUG_MODE  # Set to True to run debug_client.py instead of switch.py

def run_app2():
    print("Start process_mock CLIENT")
    subprocess.run(["python3", "./dev/process_mock.py"])


def run_app():
    print("Start APP SERVER")
    subprocess.run(["python3", "app.py"])

def run_switch_or_debug_as_subprocess():
    if DEBUG == 1:
        # Running debug_client.py as a subprocess when DEBUG is True
        print("Start DEBUG CLIENT")
        subprocess.run(["python3", r"./dev/debug_client.py"])
    else:
        print("Start SWITCH CLIENT")
        # Running switch.py as a subprocess when DEBUG is False
        subprocess.run(["python3", "switch.py"])

def main():
    # Starting app.py in a separate thread
    app_thread = threading.Thread(target=run_app)
    app_thread.start()

    if DEBUG == 2:
        app_thread2 = threading.Thread(target=run_app2())
        app_thread2.start()

    # Running switch.py or debug_client.py as a subprocess
    run_switch_or_debug_as_subprocess()

if __name__ == "__main__":
    main()