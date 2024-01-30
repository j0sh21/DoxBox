import cups
import os

def print_image(printer_name, image_path):
    # Connect to CUPS
    conn = cups.Connection()

    # Get a list of all printers
    printers = conn.getPrinters()

    # Check if specified printer is available
    if printer_name not in printers:
        print(f"Printer {printer_name} not found. Available printers:")
        for printer in printers:
            print(printer)
        return

    # Print the image
    print_job_id = conn.printFile(printer_name, image_path, "Photo Print", {})
    print(f"Print job submitted. Job ID: {print_job_id}")

# Example usage
printer_name = "Xiaomi_Instant_Photo_Printer_1S_0057_"  # Replace with your printer's name
image_directory = "../images/print"  # Replace with your image directory
image_file = "IMG_0911.jpg"  # Replace with your image file name

# Construct the full image path
image_path = os.path.join(image_directory, image_file)

# Call the print function
print_image(printer_name, image_path)
