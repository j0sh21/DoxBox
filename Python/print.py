import datetime

import cups
import os
import config

def print_image(printer_name, image_path):

    print("Connect to the CUPS printing Server")
    # Connect to CUPS
    conn = cups.Connection()
    # Get a list of all printers
    printers = conn.getPrinters()
    print(f"Sucessfully Connected to the print Server {printer_name}")

    # Check if specified printer is available
    if printer_name not in printers:
        print(f"Printer {printer_name} not found. Available printers:")
        for printer in printers:
            print(f"{printer}\n")
        return

    if config.DEBUG_MODE == 0:
        # Print the image
        print_job_id = conn.printFile(printer_name, image_path, "Photo Print", {})
        print(f"Print job submitted to Printer. Job ID: {print_job_id}\nStart printing {image_path} on {printer_name}")
    else:
        print(f"DEBUG MODE: Simulate Print file {image_path} on {printer_name}. \nDEBUG MODE: Skip 45 sec waiting time...")

def move_image():
    pic_dir = os.path.join(config.PICTURE_SAVE_DIRECTORY, datetime.datetime.now().strftime("%Y-%m-%d"))
    print_dir = config.PRINT_DIR
    printer_name = config.PRINTER_NAME
    cwd = os.getcwd()
    os.chdir(pic_dir)
    print(f"Change directory to {pic_dir}")
    for filename in os.listdir():
        picture_name = filename
    # Construct the full source and destination paths
        source_picture_path = os.path.join(pic_dir, picture_name)
        destination_picture_path = os.path.join(print_dir, picture_name)

    # Use os.rename() to move the picture, delete after print with os.remove
        try:
            os.rename(source_picture_path, destination_picture_path)
            print(f'Successfully moved {picture_name} from {pic_dir} to {print_dir}')
            image_path = os.path.join(print_dir, picture_name)
            print_image(printer_name, image_path)
            os.remove(destination_picture_path)
            print(f'Successfully removed {picture_name} from Disk.')
        except FileNotFoundError:
            print(f'Error: {picture_name} not found in {pic_dir}')
        except PermissionError:
            print(f'Permission denied when accessing {filename}. Check file permissions.')
        except Exception as e:
            print(f'An error occurred while move {picture_name} to {print_dir}: {str(e)}')
    os.chdir(cwd)
    print(f"Change directory back to {cwd}")

if __name__ == '__main__':
    print("print.py is now running.")
    print(f"preparing print Job")
    move_image()
    print(f"Printing now up to 45 seconds ...")
    print("print.py is now finished successfully")