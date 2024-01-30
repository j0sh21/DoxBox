import socket
import config
from datetime import datetime
from sh import gphoto2 as gp
import signal
import os
import subprocess
#sudo apt-get install gphoto2

def send_message_to_app(message):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((config.HOST, config.PORT))
        client_socket.sendall(message.encode())
        client_socket.close()
    except Exception as e:
        print(f"Error in sending message to app: {e}")

def kill_process():
    try:
        p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        out, err = p.communicate()

        # Look for the process pid
        for line in out.split():
            if config.PROCESS_TO_KILL.encode() in line:
                # Kill the process
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)
                print(f'Process with PID {pid} (gvfsd-gphoto2) killed.')
    except subprocess.CalledProcessError as e:
        print(f"Error while executing 'ps': {str(e)}")
        send_message_to_app("100")
    except ValueError as e:
        print(f"Error parsing process PID: {str(e)}")
        send_message_to_app("100")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        send_message_to_app("100")

def create_output_folder():
    try:
        os.makedirs(save_pic_to)
    except FileExistsError:
        print(f"The folder '{save_pic_to}' already exists.")
    except Exception as e:
        print(f"An error occurred while creating the folder: {str(e)}")
        send_message_to_app("100")
    try:
        os.chdir(save_pic_to)
        print(f"Changed working directory to '{save_pic_to}'")
    except FileNotFoundError:
        print(f"Error: The specified directory '{save_pic_to}' does not exist.")
        send_message_to_app("100")
    except PermissionError:
        print(f"Error: Permission denied while changing the working directory.")
        send_message_to_app("100")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        send_message_to_app("100")

def run_gphoto2_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        send_message_to_app("100")

def make_picture():
    trigger_photo_cmd = config.TRIGGER_PHOTO_COMMAND
    download_pics_cmd = config.DOWNLOAD_PHOTOS_COMMAND
    clear_files_cmd = config.CLEAR_FILES_COMMAND

    try:
        start_download = datetime.now()
        run_gphoto2_command(trigger_photo_cmd)
        end_download = datetime.now()
        print(f"Photo taken and saved in {(end_download - start_download).total_seconds()} Seconds.")
        start_download = datetime.now()
        run_gphoto2_command(download_pics_cmd)
        end_download = datetime.now()
        print(f"Copied file in {(end_download - start_download).total_seconds()} Seconds.")
        run_gphoto2_command(clear_files_cmd)

    except Exception as e:
        print(f"An error occurred during picture taking process: {str(e)}")
        send_message_to_app("100")

def rename_pics():
    try:
        for filename in os.listdir("."):
            if len(filename) < 13:
                if filename.endswith(".JPG"):
                    os.rename(filename, (shot_time + ".JPG"))
                    print("Picture renamed!")
                    send_message_to_app("4")
                elif filename.endswith(".CR2"):
                    os.rename(filename, (shot_time + ".CR2"))
                    send_message_to_app("100")
                    print("Picture renamed!")
    except FileNotFoundError:
        print("Error: The specified file or directory does not exist.")
    except PermissionError:
        print("Error: Permission denied while renaming files.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


if __name__ == '__main__':
    shot_date = datetime.now().strftime("%Y-%m-%d")
    shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clear_files_cmd = ["--folder", "/store_00020001/DCIM/100CABON", "-R", "--delete-all-files"]
    folder_name = shot_date
    save_pic_to = os.path.join(config.PICTURE_SAVE_DIRECTORY, folder_name)
    kill_process()
    gp(clear_files_cmd)
    create_output_folder()
    make_picture()
    rename_pics()