# DoxBox - a bitcoin ⚡️ lightning photobox 

<p align="center">
<img src="https://raw.githubusercontent.com/j0sh21/DoxBox/main/docs/images/Box.jpeg" width="200">
</p>

The DoxBox prints captured pictures upon bitcoin lightning payments to its [LNbits wallet.](https://github.com/lnbits/lnbits)
You can set it up on any wedding, a conferece, a meetup or a festival. We built it in a modular way so that you can easily travel with it. 

## Hardware Requirements

- **Raspberry Pi 4** running the Debian-based operating system [available from Raspberry Pi's official software page.](https://www.raspberrypi.com/software/operating-systems/)
- **DSLR Camera**: Canon EOS 450D with at least 1GB SD-Card. If you use another one [ensure compatibility with gphoto2 on the official website](http://www.gphoto.org/proj/libgphoto2/support.php)
- **Display**: Waveshare 10.4" QLED Quantum Dot Capacitive Display (1600 x 720)
- **Printer**: Xiaomi-Instant-Photo-Printer-1S, supports CUPS printing system, 6" fotopaper
- **LED**: 4-channel RGB LED strip, along with a breadboard, connecting cables, and 4 Mosfets for control.
- **Construction Material**: Three sheets of 80x80cm plywood; access to a laser cutter may be beneficial.
- **Assembly Hardware**: 20 sets of corner magnets (2 pieces per set), 40 screws of 4mm diameter, and 120 nuts of 4mm diameter to secure the components.
- **spray colour**: 1 can of primer, 4 cans of actual colour

  <img src="https://github.com/j0sh21/DoxBox/assets/63317640/384280e0-cc6e-4bd0-9953-c318b5e12f15" height="200">

  <img src="https://github.com/j0sh21/DoxBox/assets/63317640/e446af16-d840-4cbc-87f9-3d5f67b3a15d" height="200">
  
  <img src="https://github.com/j0sh21/DoxBox/assets/63317640/4bcc6965-a1fa-41e5-8d07-cc7e3280bc58" height="200">

  
## Example program flow:

<img src="./docs/images/flowchart.JPG" height="1100">


## Setup Instructions

### Key Components

- **main.py**: Serves as the entry point of the application, orchestrating the execution of various components based on operational modes.
- **app.py**: Manages the graphical user interface (GUI) of the application, facilitating user interactions and displaying information.
- **switch.py**: Handles external API interactions and performs specific actions based on the received data, such as triggering other application components.
- **img_capture.py**: Interacts with cameras to capture images, download them, and manage file storage, leveraging gphoto2.
- **print.py (In Progress)**: Interfaces with printers using CUPS to print images, with functionality to select printers and manage print jobs.
- **config.py**: Contains configuration settings used across the application, such as API keys, device names, and file paths.

### Installation

1. **Clone the Repository**: Start by cloning this repository.

   ```sh
   git clone https://github.com/j0sh21/DoxBox.git
    ```
2. **Install Dependencies**: Ensure Python is installed on your system, install the required Python packages.

    ```sh

    pip install -r requirements.txt
    ```
    **Note**: Some components may require additional system-level dependencies (e.g., gphoto2, CUPS).
   

   - If you want to install additional system-level dependencies automaticlly run install.sh instead:
      ```sh
      cd DoxBox/install
      chmod u+x install.sh
      ./install.sh

3. **Configure**: Review and update config/cfg.ini with your specific settings, such as device names, API keys and file paths.
   ```sh
   nano cfg.ini
## Usage

To run the application, navigate to the project directory and execute main.py:

 ```sh
python3 main.py
 ```
For specific functionalities, such as capturing an image or printing, you can run the respective scripts (e.g., python img_capture.py for image capture).
Example Usage

**Capture an Image** Ensure your camera is connected and recognized by your system, then run:

 ```sh
python3 img_capture.py
 ```
**Print an Image**: Update print.py with your printer's name and the image file path, then execute:

    python print.py

## Contributing

Contributions to the project are welcome! Please refer to the contribution guidelines for information on how to submit pull requests, report issues, or suggest improvements.


## Changelog for DoxBox Project
### Version 0.1, released 25 Feb 2024

### Features
- Updated `app.py` to use new frame and new GIFs.
- Integrated new GIFs from @arbadacarbaYK, removing empty background frames and watermarks. Countdown GIFs now have consistent timing between numbers.
- Added `self.isreplay` to reset GIF loop count only once.
- Introduced new error codes from `switch.py` to the documentation in English, German, and Portuguese.
- Implemented new state 3.5: Transition to `img_capture.py` after the first smile GIF finishes.
- Implemented new state 3.9: Photo successfully transferred from camera, initiating print preparation.
- Advanced state 4: Triggered earlier to commence printing before the photo is deleted from the camera.
- Refactored camera-specific error handling in `img_capture.py`.
- Introduced maximum retry attempts and variable wait times for camera-related errors.

### Improvements
- Added network connectivity checks before polling LNbits API.
- Enhanced and cleaned up console output styling.
- Hidden mouse cursor for a cleaner UI.
- Improved log message clarity and detail.
- Removed corrupted files and performed general cleanup.
- Adjusted LED effects for better visual feedback.

### Fixes
- Corrected `def kill_process()` to ensure proper process termination.
- Fixed issue where multiple smile GIFs could be displayed simultaneously.
- Resolved a bug where state 204 could hang indefinitely on print job failure checks.

### Infrastructure
- Created an output folder for print jobs. **TODO:** Automate folder creation using `os.mkdir` instead of including an empty folder in the repository.
- **TODO:** Fine-tune `check_print_job_status` functionality.

## License
This project is licensed under the MIT License - see the LICENSE file for details. 
Contributions to the project are welcome! 

## Acknowledgments
Special thanks to [Ben Arc](https://github.com/arcbtc) for [LNbits](https://github.com/lnbits/lnbits) and all maintainers of the external libraries and tools also used in this project.

 ⚡️ [Tip this project](https://legend.lnbits.com/lnurlp/link/4Wc7ZE) if you like the DoxBox ⚡️
