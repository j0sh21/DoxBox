# Documentation for print.py

## Overview

The `DoxBoxPrintManager` (`print.py`) is an essential component of the DoxBox system, designed to seamlessly handle the printing of images immediately after they are captured. This Python script integrates with CUPS (Common UNIX Printing System) to manage print jobs and ensures that each image is printed successfully while providing real-time feedback on the job status. To ensure confidentiality and data security, the image is immediately deleted after being sent to the printer.

## Features

- **Direct Integration with CUPS**: Leverages the CUPS server to submit and manage print jobs, ensuring broad compatibility with various printers.
- **Real-Time Print Job Monitoring**: Tracks the status of each print job in real time, providing updates on completion, errors, or cancellations.
- **Error Handling and Reporting**: Comprehensive error handling mechanisms report issues back to the application, ensuring smooth operation.
- **Modular Design**: The script is structured into clear, concise functions, making it easy to understand, maintain, and extend.
- **Configurable**: Utilizes an external configuration module (`config.py`) for easy adjustments without altering the core script.
- **Debug Mode**: Includes a debug mode for testing and troubleshooting without sending actual print jobs to the printer.

## Components

- `send_message_to_app(message)`: Sends status messages or error codes to the main Photobox application for logging or user notification.
- `check_print_job_status(conn, job_id)`: Monitors the status of submitted print jobs, ensuring they complete successfully or handling errors as needed.
- `print_image(printer_name, image_path)`: Submits an image file to the specified printer and initiates the monitoring process.
- `copy_file(source_path, destination_path)`: Handles the secure transfer of image files from the capture location to the print queue.
- `move_image()`: Orchestrates the process of preparing images for printing, including file transfer and deletion post-printing.

## How It Works

1. **Image Capture**: Once an image is captured by the Photobox, it is stored in a predetermined directory.
2. **File Preparation**: The `move_image` function scans the directory for new images, preparing them for printing.
3. **Printing**: Images are sent to the `print_image` function, where they are submitted as print jobs to the configured printer.
4. **Monitoring**: Each print job's status is monitored in real-time by `check_print_job_status`, providing feedback on the job's progress and handling any issues that arise.
5. **Completion**: Upon successful printing, the image file is deleted, and the system is ready for the next capture.

## Configuration

The script relies on a separate `config.py` file for configuration settings, such as the CUPS server details, printer name, and directories for image storage and printing. This allows for easy adjustments to different environments or printers.

## Debugging and Logging

Debug mode can be activated for testing purposes, simulating the printing process without sending jobs to the printer. Console logging provides real-time feedback on the script's operation, and integrating a more sophisticated logging system is recommended for production use.

## Dependencies

- CUPS
- Python-CUPS (for interacting with the CUPS server from Python)
- Standard Python libraries: `datetime`, `shutil`, `socket`, `os`, `time`

## Example Usage

Example usage that demonstrates how to call the `print_image` function with hardcoded values for the printer name and image path. This example serves as a basic guide for integrating the printing functionality into broader application workflows.

```python
printer_name = "Your_Printer_Name_Here"
image_directory = "/path/to/image/directory"
image_file = "example.jpg"

image_path = os.path.join(image_directory, image_file)
print_image(printer_name, image_path)
```

## Getting Started

1. Ensure CUPS is installed and configured on your system.
2. Install Python-CUPS using pip: `pip install pycups`.
3. Adjust the `config.py` file to match your environment.
4. Run the script after an image is captured to initiate the printing process.

### Installing Required Dependencies on eg. Raspberry Pi:

To use pycups on your Raspberry Pi, you need to ensure that the required dependencies are installed. Here are the steps to do so:

1. **Update Your System**: Ensure your package lists and installed packages are up to date.

   ```bash
   sudo apt-get update
   sudo apt-get upgrade

This will ensure that your Raspberry Pi is running the latest software.

**Install CUPS and Development Tools**: Install CUPS (Common UNIX Printing System), the CUPS development libraries, and the Python development headers. These libraries are essential for compiling pycups.


    sudo apt-get install libcups2-dev libcupsimage2-dev gcc python3-dev

This command installs the necessary libraries and development tools.

Install pycups Using pip: After installing the necessary development packages, try installing pycups again using pip3.

    pip3 install pycups

By now, you should be able to successfully compile and install pycups.

Upgrade pip, setuptools, and wheel (If Needed): In some cases, you may need to ensure that your pip, setuptools, and wheel packages are up to date.

    pip3 install --upgrade pip setuptools wheel

After upgrading these packages, attempt to install pycups again.

If you encounter any issues during the installation process or if you have error messages, please provide them for further assistance.