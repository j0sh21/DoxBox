import socket
import config
from datetime import datetime
from sh import gphoto2 as gp
import signal
import os
import subprocess
import sh
#sudo apt-get install gphoto2

cwd = ""

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
                print(f'Process with PID {pid} (gvfsd) killed.')
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
    shot_date = datetime.now().strftime("%Y-%m-%d")
    folder_name = shot_date
    save_pic_to = os.path.join(config.PICTURE_SAVE_DIRECTORY, folder_name)
    try:
        os.makedirs(save_pic_to)
    except FileExistsError:
        print(f"The folder '{save_pic_to}' already exists.")
    except Exception as e:
        print(f"An error occurred while creating the folder: {str(e)}")
        send_message_to_app("100")
    try:
        global cwd
        cwd = os.getcwd()
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
        send_message_to_app("100")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        send_message_to_app("100")

def make_picture():
    global cwd
    trigger_photo_cmd = config.TRIGGER_PHOTO_COMMAND
    download_pics_cmd = config.DOWNLOAD_PHOTOS_COMMAND
    clear_files_cmd = config.CLEAR_FILES_COMMAND

    try:
        start_trigger = datetime.now()
        print(f"Trigger photo NOW!")
        try:
            run_gphoto2_command(trigger_photo_cmd)
        except sh.ErrorReturnCode_1 as e:
            # Now we can check the contents of the error message
            error_message = str(e)

            if "Fokus" in error_message:
                # If the specific error message is found, print custom text
                print("Error: Camera has no Focus. Please ensure placing the subject on the focus mark and try again.")
                send_message_to_app("101")
            else:
                # If the error message does not match, print a generic error message or re-raise the exception
                print("An unexpected error occurred:", error_message)
                send_message_to_app("100")
                # Or, to propagate the error, you might use: raise
        end_trigger = datetime.now()
        print(f"Photo taken and saved on Camera in {(end_trigger - start_trigger).total_seconds()} Seconds.")
        start_download = datetime.now()
        run_gphoto2_command(download_pics_cmd)
        end_download = datetime.now()
        print(f"Copied file from Camera to RaspberryPi in {(end_download - start_download).total_seconds()} Seconds.")
        start_clear = datetime.now()
        run_gphoto2_command(clear_files_cmd)
        end_clear = datetime.now()
        print(f"Cleared file from Camera in {(end_clear - start_clear).total_seconds()} Seconds.")
    except Exception as e:
        print(f"An error occurred during picture taking process: {str(e)}")
        send_message_to_app("100")

def rename_pics():
    shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for filename in os.listdir("."):

            if len(filename) < 13:
                if filename.endswith(".JPG"):
                    try:
                        os.rename(filename, (shot_time + ".JPG"))
                        print("Picture renamed!")
                        os.chdir(cwd)
                        print(f"Changed Working Directory to: {os.getcwd()}")
                        send_message_to_app("4")
                    except FileNotFoundError:
                        print("Error: The Picture does not exist.")
                        send_message_to_app("100")
                    except PermissionError:
                        print("Error: Permission denied while renaming files.")
                        send_message_to_app("100")
                    except Exception as e:
                        print(f"An unexpected error occurred: {str(e)}")
                        send_message_to_app("100")

def main():

    clear_files_cmd = ["--folder", "/store_00020001/DCIM/100CANON", "-R", "--delete-all-files"]
    print("Kill old ghphoto2 processes")
    kill_process()
    print("Remove all files from the Camera")
    try:
        gp(clear_files_cmd)
    except sh.ErrorReturnCode_1 as e:
        # Now we can check the contents of the error message
        error_message = str(e)

        if "Keine Kamera gefunden" in error_message:
            # If the specific error message is found, print custom text
            print("Error: No camera found. Please ensure the camera is connected properly.")
            send_message_to_app("102")
        else:
            # If the error message does not match, print a generic error message or re-raise the exception
            print("An unexpected error occurred:", error_message)
            send_message_to_app("100")
            # Or, to propagate the error, you might use: raise
    print("Create output Folder if not already there")
    create_output_folder()
    print("Make Picture")
    make_picture()
    print("Rename the Picture")
    rename_pics()

if __name__ == '__main__':
    print("img_capture.py is now running")
    main()
    print("img_capture.py is now finished successfully")