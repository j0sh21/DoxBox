import threading
import subprocess
import config

DEBUG = config.DEBUG_MODE  # Set to True to run debug_client.py instead of switch.py


def run_app2():
    subprocess.run(["python3", "./dev/process_mock.py"])


def run_app():
    subprocess.run(["python3", "app.py"])

def run_switch_or_debug_as_subprocess():
    if DEBUG:
        # Running debug_client.py as a subprocess when DEBUG is True
        subprocess.run(["python3", r"./dev/debug_client.py"])
    else:
        # Running switch.py as a subprocess when DEBUG is False
        subprocess.run(["python3", "switch.py"])

def main():
    # Starting app.py in a separate thread
    app_thread = threading.Thread(target=run_app)
    app_thread.start()

    if DEBUG:
        app_thread2 = threading.Thread(target=run_app2())
        app_thread2.start()


    # Running switch.py or debug_client.py as a subprocess
    run_switch_or_debug_as_subprocess()



if __name__ == "__main__":
    main()