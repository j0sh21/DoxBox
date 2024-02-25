import datetime
import shutil
import socket
import cups
import os
import config
import time

def send_message_to_mini_display(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('localhost', 6548))
        client_socket.sendall(command.encode('utf-8'))

def send_message_to_app(message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((config.HOST, config.PORT))
            client_socket.sendall(message.encode())
    except socket.error as e:
        send_message_to_mini_display(f"Error in sending message to app: {e}")

def check_print_job_status(conn, job_id):
    try:
        initial_wait = 20
        time.sleep(initial_wait)
        while True:
            jobs = conn.getJobs(which_jobs='not-completed')
            send_message_to_mini_display(f"Checking print job status: {len(jobs)} not-completed print jobs found")
            if not jobs:
                send_message_to_mini_display("No not-completed print jobs")
                break

            if job_id not in jobs:
                send_message_to_mini_display(f"Print job {job_id} status changed to 'successful'.")
                break
            else:
                job = jobs[job_id]
                send_message_to_mini_display(f"Print job {job_id} status: {job['job-state']}, {job['job-state-reasons']}")
                if 'job-completed' in job['job-state-reasons']:
                    send_message_to_mini_display(f"Print job {job_id} completed successfully.")
                    send_message_to_app("5")
                    break
                elif 'job-stopped' in job['job-state-reasons'] or 'job-canceled' in job['job-state-reasons']:
                    send_message_to_mini_display(f"Print job {job_id} stopped or canceled.")
                    send_message_to_app("116")
                    break
                elif 'job-error' in job['job-state-reasons']:
                    send_message_to_mini_display(f"Print job {job_id} encountered an error.")
                    send_message_to_app("110")
                    break
            time.sleep(1)
    except Exception as e:
        send_message_to_mini_display(f"Error while checking print job Status: {e}\n\n Sleeping 45 seconds...\nPhoto should be printed finish correctly in about 45 seconds... ")
        time.sleep(45)
        send_message_to_app("5")
        send_message_to_mini_display("Waiting 45 seconds finished print ready!")

def print_image(printer_name, image_path):
    send_message_to_mini_display("Connecting to the CUPS printing server...")
    conn = cups.Connection()
    printers = conn.getPrinters()
    if printer_name not in printers:
        send_message_to_mini_display(f"Printer {printer_name} not found. Available printers:")
        send_message_to_app("112")
        for printer in printers:
            send_message_to_mini_display(f"{printer}\\n")
        return

    send_message_to_mini_display(f"Successfully connected to the print server {printer_name}")
    if config.DEBUG_MODE == 0:
        if not os.path.exists(image_path):
            send_message_to_mini_display(f"Error: File {image_path} not found.")
            send_message_to_app("113")
            return
        try:
            print_job_id = conn.printFile(printer_name, image_path, "Photo Print", {})
            send_message_to_mini_display(f"Print job submitted. Job ID: {print_job_id} - {image_path} on {printer_name}")
            # Check the status of the print job
            check_print_job_status(conn, print_job_id)
        except Exception as e:
            send_message_to_mini_display(f"Error in print job: {e}")
            send_message_to_app("119")
    else:
        send_message_to_mini_display(
            f"DEBUG MODE: Simulate print file {image_path} on {printer_name}. \\nDEBUG MODE: Skip 45 sec waiting time...")

def copy_file(source_path, destination_path):
    if not os.path.exists(source_path):
        send_message_to_mini_display(f"Error: The file {source_path} does not exist.")
        send_message_to_app("113")
        return False
    try:
        shutil.move(source_path, destination_path)
        send_message_to_mini_display(f"Successfully copied {source_path} to {destination_path}")
        return True
    except PermissionError:
        send_message_to_mini_display(f"Error: Permission denied for {source_path}.")
        send_message_to_app("114")
    except Exception as e:
        send_message_to_mini_display(f"Error copying {source_path}: {e}")
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
            send_message_to_mini_display(f'Removed {filename} after creating and sending print job and waiting 65 Seconds.')

if __name__ == '__main__':
    send_message_to_mini_display("print.py is now running.")
    send_message_to_mini_display(f"Preparing print job")
    move_image()
    send_message_to_mini_display(f"Printing now, can take up to 45 seconds ...")
    send_message_to_mini_display("print.py finished successfully")
