# Project Overview

This project is designed to leverage the capabilities of a Raspberry Pi or any other Debian based host system to interact with a DSLR camera for high-quality image capture while  managing and interacting with a specific application workflow, which includes image capture, printing, and dynamic user interface interaction. The application runs on Python and integrates with various external systems and libraries, such as CUPS for printing and gphoto2 for camera control, to deliver its functionality.

## Key Components

- **main.py**: Serves as the entry point of the application, orchestrating the execution of various components based on operational modes.
- **app.py**: Manages the graphical user interface (GUI) of the application, facilitating user interactions and displaying information.
- **switch.py**: Handles external API interactions and performs specific actions based on the received data, such as triggering other application components.
- **img_capture.py**: Interacts with cameras to capture images, download them, and manage file storage, leveraging gphoto2.
- **print.py (In Progress)**: Interfaces with printers using CUPS to print images, with functionality to select printers and manage print jobs.
- **config.py**: Contains configuration settings used across the application, such as API keys, device names, and file paths.

## Hardware Requirements

- **Host System**: The core platform for running the application (e.g. Raspberry Pi, mini pc), providing the necessary compute resources and connectivity for peripherals.
- **DSLR Camera**: Used for capturing high-quality images. Ensure compatibility with gphoto2 for integration.
- **Webcam**: A webcam must be attached and configured for image capture functionalities.
- **Display**: A display is required for showing the GUI, including photo previews and animations.
- **Printer**: A photo printer set up and configured on the Host System for printing images, compatible with CUPS.

## Setup Instructions

1. **Clone the Repository**: Start by cloning this repository to your local machine.

   ```sh
   git clone https://github.com/j0sh21/DoxBox.git
    ```
2. **Install Dependencies**: Ensure Python is installed on your system, and then install the required Python packages.

    ```sh

    pip install -r requirements.txt
    ```
    **Note**: Some components may require additional system-level dependencies (e.g., gphoto2, CUPS).
   

   - If you want to install  additional system-level dependencies automaticlly than run install.sh instead:
      ```sh
      cd DoxBox/install
      chmod u+x install.sh
      ./install.sh

3. **Configure**: Review and update config/cfg.ini with your specific settings, such as device names, API keys, and file paths.
   ```sh
   nano cfg.ini
## Usage

To run the application, navigate to the project directory and execute main.py:

 ```sh
python main.md
 ```
For specific functionalities, such as capturing an image or printing, you can run the respective scripts (e.g., python img_capture.py for image capture).
Example Usage

**Capture an Image** Ensure your camera is connected and recognized by your system, then run:

 ```sh
python img_capture.py
 ```
**Print an Image**: Update print.py with your printer's name and the image file path, then execute:

    python print.py

## Contributing
Contributions to the project are welcome! Please refer to the contributing guidelines for more information on how to submit pull requests, report issues, or suggest enhancements.
## License
This project is licensed under the MIT License - see the LICENSE file for details.
## Acknowledgments
Special thanks to all contributors and maintainers of the external libraries and tools used in this project.
