import socket
import time
import config
from datetime import datetime
from sh import gphoto2 as gp
import signal
import os
import subprocess
import sh
#Make sure to install gphoto2


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

def send_msg_to_LED(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((config.LED_SERVER_HOST, config.LED_SERVER_PORT))
        client_socket.sendall(command.encode('utf-8'))

def kill_process():
    try:
        output = subprocess.check_output(['ps', '-A'], text=True)
        for line in output.splitlines():
            if config.PROCESS_TO_KILL in line:
                send_message_to_mini_display("Kill the old ghphoto2 server processes to prevent connection issues with camera")
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGTERM)
                os.kill(pid, signal.SIGKILL)
                send_message_to_mini_display(f'Process with PID {pid} ({config.PROCESS_TO_KILL}) killed.\nWaiting 330ms to continue...')
                time.sleep(0.33)
    except subprocess.CalledProcessError as e:
        send_message_to_mini_display(f"Error while executing 'ps': {str(e)}")
        send_message_to_app("100")
    except ValueError as e:
        send_message_to_mini_display(f"Error parsing process PID: {str(e)}")
        send_message_to_app("100")
    except Exception as e:
        send_message_to_mini_display(f"An unexpected error occurred: {str(e)}")
        send_message_to_app("100")

def create_output_folder():
    shot_date = datetime.now().strftime("%Y-%m-%d")
    folder_name = shot_date
    save_pic_to = os.path.join(config.PICTURE_SAVE_DIRECTORY, folder_name)
    try:
        os.makedirs(save_pic_to)
    except FileExistsError:
        send_message_to_mini_display(f"The folder '{save_pic_to}' already exists.")
    except PermissionError:
        send_message_to_mini_display(f"Error: Permission denied to create folder {save_pic_to}.")
        send_message_to_app("104")
    except Exception as e:
        send_message_to_mini_display(f"An error occurred while creating the folder: {str(e)}")
        send_message_to_app("100")
    try:
        global cwd
        cwd = os.getcwd()
        os.chdir(save_pic_to)
        send_message_to_mini_display(f"Changed working directory to '{save_pic_to}'")
    except FileNotFoundError:
        send_message_to_mini_display(f"Error: The specified directory '{save_pic_to}' does not exist.")
        send_message_to_app("103")
    except PermissionError:
        send_message_to_mini_display(f"Error: Permission denied while changing the working directory.")
        send_message_to_app("104")
    except Exception as e:
        send_message_to_mini_display(f"An unexpected error occurred: {str(e)}")
        send_message_to_app("100")

def run_gphoto2_command(command, retries=0, max_retries=config.MAX_RETRIES):
    try:
        subprocess.run(command, shell=True, check=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode()
        if retries < max_retries:
            handle_error(error_message, retries)
            run_gphoto2_command(command, retries + 1, max_retries)
        else:
            send_message_to_mini_display(f"Error and Max retries {str(retries)} reached, aborting.\n{error_message}")

def handle_error(error_message, retries):
        if "focus" in error_message:
            send_message_to_mini_display(f"\nError: Camera has no Focus. Please ensure placing the subject on the focus mark and try again.\nSLEEP for 10 SECONDS NOW!\nRetry number {str(retries)} Photo in 10 seconds...")
            send_message_to_app("101")
            time.sleep(config.IMG_SLEEP_TIME_SHORT)
        elif "failed to release" in error_message:
            send_message_to_mini_display("Error: Capture failed to release\nSLEEP for 10 SECONDS NOW!\nRetry Photo in 10 seconds...")
            time.sleep(config.IMG_SLEEP_TIME_SHORT)
            send_message_to_app("101")
        elif "Keine Kamera gefunden" in error_message:
            send_message_to_mini_display("\n\nError: No camera found. Please ensure the camera is connected properly.\n\nSLEEP for 3 MINUTES NOW!\n\nRetry Photo in 3 minutes...")
            send_message_to_app("102")
            time.sleep(config.IMG_SLEEP_TIME_LONG)
            kill_process()
        elif "Zugriff verweigert" in error_message:
            send_message_to_mini_display("\nError: Access to camera denied.\nSLEEP for 10 SECONDS NOW!\nRetry Photo in 10 seconds...")
            send_message_to_app("104")
            time.sleep(config.IMG_SLEEP_TIME_SHORT)
        else:
            send_message_to_mini_display("An unexpected error occurred:", error_message)
            send_message_to_app("100")

def make_picture():
    global cwd
    trigger_photo_cmd = config.TRIGGER_PHOTO_COMMAND
    download_pics_cmd = config.DOWNLOAD_PHOTOS_COMMAND
    start_trigger = datetime.now()
    send_msg_to_LED("blink 0")
    send_message_to_mini_display(f"{'_'*10}\n|Trigger photo NOW!|\n{'_'*10}")
    run_gphoto2_command(trigger_photo_cmd)
    end_trigger = datetime.now()
    send_message_to_mini_display(f"Photo taken and saved on camera in {(end_trigger - start_trigger).total_seconds()} seconds.\n")
    send_message_to_app("3.9")
    send_msg_to_LED("breathbrightness 0.5 1.0")
    send_msg_to_LED("breathspeed 0.003")
    send_msg_to_LED("breath 1")
    start_download = datetime.now()
    run_gphoto2_command(download_pics_cmd)
    end_download = datetime.now()
    send_message_to_mini_display(f"Copied file from Camera to RaspberryPi in {(end_download - start_download).total_seconds()} Seconds.\n")

def rename_pics():
    shot_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    for filename in os.listdir("."):
            if len(filename) < 13 and filename.endswith(".JPG"):
                try:
                    os.rename(filename, (shot_time + ".JPG"))
                    send_message_to_mini_display("Picture renamed! to " + shot_time + ".JPG\n")
                    return True
                except FileNotFoundError:
                    send_message_to_mini_display("Error: The Picture does not exist.")
                    send_message_to_app("103")
                    return False
                except PermissionError:
                    send_message_to_mini_display("Error: Permission denied while renaming files.")
                    send_message_to_app("104")
                    return False
                except Exception as e:
                    send_message_to_mini_display(f"An unexpected error occurred: {str(e)}")
                    send_message_to_app("100")
                    return False
    os.chdir(cwd)
    send_message_to_mini_display(f"Changed Working Directory to: {os.getcwd()}")

def main():
    send_msg_to_LED("color 255 255 255")
    send_msg_to_LED("blinkspeed 0.05 0.05 ")
    send_msg_to_LED("blink 1 ")
    # kill gphoto2 process and deletes alle old files from camera, before proceeding with create_output_folder and make_picture
    kill_process()
    start_clear = datetime.now()
    clear_files_cmd = ["--folder", "/store_00020001/DCIM/100CANON", "-R", "--delete-all-files"]
    send_message_to_mini_display("\nRemove all files from the Camera\n")
    try:
        gp(clear_files_cmd)
        end_clear = datetime.now()
        send_message_to_mini_display(f"Cleared file from Camera in {(end_clear - start_clear).total_seconds()} seconds.\n\n")
    except sh.ErrorReturnCode_1 as e:
        # checking the contents of the error message (The language of the error message is controlled by your camera settings)
        error_message = str(e)
        if "Keine Kamera gefunden" in error_message:
            send_message_to_mini_display("Error: No camera found. Please ensure the camera is connected properly.")
            send_message_to_app("102")
        else:
            send_message_to_mini_display("An unexpected error occurred:", error_message)
            send_message_to_app("100")

    create_output_folder()
    send_message_to_mini_display("Make Picture")
    make_picture()
    send_message_to_mini_display("Rename the Picture on the Raspberry Pi")
    if rename_pics():
        send_message_to_app("4")
    start_clear = datetime.now()
    gp(clear_files_cmd)
    end_clear = datetime.now()
    send_message_to_mini_display(f"Cleared file from Camera in {(end_clear - start_clear).total_seconds()} seconds.\n\n")


if __name__ == '__main__':
    cwd = ""
    send_message_to_mini_display("img_capture.py is now running")
    main()
    send_message_to_mini_display("img_capture.py is now finished successfully")
