# Documentation for img_capture.py

## Overview

The `img_capture.py` script is an integral component of the application designed for managing image capture workflows. It interfaces with digital cameras via the gphoto2 command-line utility, performing tasks such as capturing images, downloading them to a designated directory, and managing file naming conventions. Additionally, it incorporates network communication to relay status updates or errors to other parts of the application.

## Dependencies

- **External Utilities**: Requires gphoto2 installed on the system (`sudo apt-get install gphoto2`).
- **Standard Libraries**: `socket`, `datetime`, `os`, `subprocess`, `signal`
- **Project Modules**: `config`

## Key Functionalities

### Camera Interaction

- Utilizes gphoto2 commands for direct interaction with the camera, enabling operations like triggering image capture, downloading images, and clearing the camera's memory card.

### Process Management

- Includes functionality to terminate specific system processes that may interfere with camera access, ensuring exclusive control over the camera during operation.

### File and Directory Management

- Handles the creation of output directories for storing captured images, with error handling for common issues like existing directories or permissions errors.
- Implements file renaming logic to organize and manage captured images based on predefined naming conventions.

### Network Communication

- Features a function for sending messages to other application components via TCP sockets, facilitating inter-process communication and status reporting.

## Key Functions

### `send_message_to_app(message)`

Sends status messages or error codes to another component of the application, enhancing error handling and user feedback mechanisms.

### `kill_process()`

Searches for and terminates a specific process by name, typically used to ensure the camera is not being accessed by another process.

### `create_output_folder()`

Creates a directory for storing captured images, handling common file system errors gracefully.

### `run_gphoto2_command(command)`

Executes a specified gphoto2 command for camera interaction, wrapped in error handling logic to catch and communicate any issues encountered during execution.

### `rename_pics()`

Renames captured images based on a set of criteria, such as date and time, to facilitate file organization and management.

## Usage

The script is designed to be run as part of a larger application workflow, typically invoked when image capture functionality is required. It operates in a sequence of steps that prepare the system and camera, execute image capture, and manage the resulting files.

### Example Workflow

1. Process Termination: Ensure no conflicting processes are accessing the camera.
2. Directory Preparation: Create or validate the existence of the output directory for storing images.
3. Image Capture: Trigger image capture and handle the camera interaction.
4. File Management: Download images to the output directory and rename them according to the application's requirements.

## Considerations

- Ensure gphoto2 is installed and properly configured on the system where the application is running.
- The script should have appropriate permissions to interact with the camera, file system, and network sockets.

## Installing gphoto2

To enable the project's DSLR camera control functionality, you need to install gphoto2 on your Raspberry Pi or any Debian-based system. gphoto2 is a versatile command-line utility that facilitates interfacing with a wide range of digital cameras. 

**Here's how to install gphoto2**:

1. **Update Your System**: First, ensure your package lists and installed packages are up to date.

   ```sh
   sudo apt-get update

1. **Install gphoto2**: Use the following command to install the gphoto2 package and its dependencies.
    ```sh
    sudo apt-get install gphoto2

This command will automatically download and install gphoto2, making it available on your system.

With gphoto2 successfully installed, your Raspberry Pi or Debian-based system will be capable of communicating with and controlling DSLR cameras for image capturing functionalities.

For more detailed information on gphoto2 and its extensive capabilities, you can visit the official gPhoto website.
