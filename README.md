# Doxbox - a bitcoin ⚡️ lightning photobox 

<p align="center">
<img src="https://github.com/j0sh21/DoxBox/assets/63317640/7eda15cf-c3a2-4236-9e24-a084b4512d96" width="200">
</p>

The Doxbox prints captured pictures upon bitcoin lightning payments to its [LNbits](https://github.com/lnbits/lnbits) wallet. 
You can set it up on any wedding, a conferece, a meetup or a festival. We build it in a modular way so that you can easily travel with it. 


## Hardware Requirements

- **Raspberry Pi 4** running [debian firmware](https://www.raspberrypi.com/software/operating-systems/)
- **DSLR Camera**: Canon EOS 450D with at least 1GB SD-Card. If you use another one ensure compatibility with gphoto2 
- **Display**: Waveshare 10.4" QLED Quantum Dot Capacitive Display (1600 x 720) 
- **Printer**: Xiaomi-Instant-Photo-Printer-1S, compatible with CUPS, 6" fotopaper
- **LED**: 4 pole RGB line, breadboard, cables, 4 Mosfets
- **wood**: 3 x 80x80cm plywood, possibly a lasercutter 
- **magnets**: 20 corner magnets (each 2pc), 40 x 4mm screws, 120 x 4mm nuts
- **spray colour**: 1 can grounding colour, 4 cans actual colour

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

## License
This project is licensed under the MIT License - see the LICENSE file for details. 
Contributions to the project are welcome! 

## Acknowledgments
Special thanks to [Ben Arc](https://github.com/arcbtc) for [LNbits](https://github.com/lnbits/lnbits) and all maintainers of the external libraries and tools also used in this project.

 ⚡️ [Tip this project](https://legend.lnbits.com/lnurlp/link/4Wc7ZE) if you like the DoxBox ⚡️
