import datetime
import shutil
import socket
import cups
import os
import config
import time

def send_message_to_app(message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((config.HOST, config.PORT))
            client_socket.sendall(message.encode())
    except socket.error as e:
        print(f"Error in sending message to app: {e}")

def check_print_job_status(conn, job_id):
    # Initial wait time in seconds before checking the job status for the first time
    initial_wait = 9
    time.sleep(initial_wait)
    while True:
        jobs = conn.getJobs(which_jobs='not-completed')

        if not jobs:
            print("No not-completed print jobs")
            break

        if job_id not in jobs:
            # Job is no longer in the list of uncompleted jobs, so it must be completed
            print(f"Print job {job_id} status changed to 'successfully'.")
            break
        else:
            job = jobs[job_id]
            print(f"Print job {job_id} status: {job['job-state']}, {job['job-state-reasons']}")
            if 'job-completed' in job['job-state-reasons']:
                print(f"Print job {job_id} completed successfully.")
                send_message_to_app("5")
                break
            elif 'job-stopped' in job['job-state-reasons'] or 'job-canceled' in job['job-state-reasons']:
                print(f"Print job {job_id} stopped or canceled.")
                send_message_to_app("140")
                break
            elif 'job-error' in job['job-state-reasons']:
                print(f"Print job {job_id} encountered an error.")
                send_message_to_app("110")
                break
        # Wait some time before checking the status again
        time.sleep(10)

def print_image(printer_name, image_path):
    print("Connect to the CUPS printing server")
    conn = cups.Connection()
    printers = conn.getPrinters()
    if printer_name not in printers:
        print(f"Printer {printer_name} not found. Available printers:")
        send_message_to_app("112")
        for printer in printers:
            print(f"{printer}\\n")
        return

    print(f"Successfully Connected to the print Server {printer_name}")
    if config.DEBUG_MODE == 0:
        if not os.path.exists(image_path):
            print(f"Error: File {image_path} not found.")
            send_message_to_app("113")
            return
        try:
            print_job_id = conn.printFile(printer_name, image_path, "Photo Print", {})
            print(f"Print job submitted. Job ID: {print_job_id} - {image_path} on {printer_name}")
            # Check the status of the print job
            check_print_job_status(conn, printer_name, print_job_id)
        except Exception as e:
            print(f"Error in print job: {e}")
            send_message_to_app("119")
    else:
        print(
            f"DEBUG MODE: Simulate print file {image_path} on {printer_name}. \\nDEBUG MODE: Skip 45 sec waiting time...")

def copy_file(source_path, destination_path):
    if not os.path.exists(source_path):
        print(f"Error: The file {source_path} does not exist.")
        send_message_to_app("113")
        return False
    try:
        shutil.move(source_path, destination_path)
        print(f"Successfully copied {source_path} to {destination_path}")
        return True
    except PermissionError:
        print(f"Error: Permission denied for {source_path}.")
        send_message_to_app("114")
    except Exception as e:
        print(f"Error copying {source_path}: {e}")
        send_message_to_app("115")
    return False

def move_image():
    pic_dir = os.path.abspath(os.path.join(config.PICTURE_SAVE_DIRECTORY, datetime.datetime.now().strftime("%Y-%m-%d")))
    printer_name = config.PRINTER_NAME

    for filename in os.listdir(pic_dir):
        source_path = os.path.join(pic_dir, filename)
        destination_path = os.path.join(config.PRINT_DIR, filename)


        if copy_file(source_path, destination_path):
            print_image(printer_name, destination_path)
            os.remove(destination_path)
            print(f'Removed {filename} after creating and sending print Job.')
            send_message_to_app("204")

if __name__ == '__main__':
    time.sleep(8)
    print("print.py is now running.")
    print(f"Preparing print job")
    move_image()
    print(f"Printing now up to 45 seconds ...")
    print("print.py is now finished successfully")