# Documentation for main.py

## Overview
This module serves as the entry point for the DoxBox, orchestrating the startup and management of various components, including an application server, LED server, and additional utilities for debugging and device control.

## Dependencies
- Python 3
- `subprocess` module for running scripts.
- `threading` module for concurrent execution.
- `pigpiod` for LED control (installed and run separately).
- **Project Modules**: `led.py`, `app.py`, `switch.py` (conditionally `./dev/process_mock.py` and `./dev/debug_client.py` for debugging)

## Key Components

### 1. Application Server
- **Functionality**: Manages the main application logic.
- **Script**: `app.py`


### 2. LED Server
- **Functionality**: Controls LED operations.
- **Script**: `led.py`
- **Dependencies**: Requires `pigpiod` daemon for GPIO pin control.


### 3. Debugging Tools
- **Functionality**: Provides debugging capabilities.
- **Scripts**: `debug_client.py` and `process_mock.py`
- **Modes**: Controlled by `DEBUG` variable in `config.py`.


### 4. Device Control
- **Functionality**: Manages device-specific operations like payment and printing.
- **Script**: `switch.py`


## Configuration
Configuration settings, including debug mode, are managed through `config.py`. Adjust settings in this file to control the application's behavior.


## Running the Application
- Start the application by running `main.py`.
- The script initializes the application server and LED server in separate threads.
- Depending on the debug mode set in `config.py`, it either launches debugging tools or the device control script.


## Debug Mode
- **Level 0**: Normal operation, `switch.py` is executed.
- **Level 1**: Basic debugging, `debug_client.py` is executed.
- **Level 2**: Extended debugging, both `debug_client.py` and `process_mock.py` are executed.


## Extending the Application
To add new functionalities:
1. Create a new script for the component.
2. Define a function in `main.py` to run the script, similar to `run_app()` or `start_led()`.
3. Add a thread or subprocess call in `main()` to execute the new function.


## Troubleshooting
- Ensure `pigpiod` is installed and can be started by the script.
- Verify all scripts referenced (`app.py`, `led.py`, `switch.py`, etc.) are present in the expected directories.
- Check `config.py` for correct debug mode settings.


## Features

- **Concurrent Execution**: Utilizes threads to run `app.py` and potentially a mock process in parallel.
- **Conditional Debugging**: Depending on the `DEBUG_MODE`, it can execute additional debugging processes to aid in development and testing.
- **Subprocess Management**: Executes key components (`app.py`, `switch.py`, or debug processes) as subprocesses, ensuring isolated and controlled execution environments.


## Running the Script

To execute the application, run the following command in the terminal:

```bash
python3 main.py
```
Ensure that all dependencies are properly installed and configured before running the script.