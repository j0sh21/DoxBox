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

def print_image(printer_name, image_path):
    print("Connect to the CUPS printing Server")
    conn = cups.Connection()
    printers = conn.getPrinters()

    if printer_name not in printers:
        print(f"Printer {printer_name} not found. Available printers:")
        send_message_to_app("112")
        for printer in printers:
            print(f"{printer}\n")
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
        except Exception as e:
            print(f"Error in print job: {e}")
            send_message_to_app("119")
    else:
        print(f"DEBUG MODE: Simulate Print file {image_path} on {printer_name}. \nDEBUG MODE: Skip 45 sec waiting time...")

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
    print("Starting print process.")
    move_image()
    print("Print process completed.")