# Documentation for main.py

## Overview

The `main.py` script serves as the central entry point for the application, orchestrating various components and managing their execution based on operational modes. It leverages threading and subprocesses to run different parts of the application concurrently, providing flexibility in debugging and functionality testing.

## Dependencies

- **Standard Libraries**: threading, subprocess
- **Project Modules**: config, app.py, switch.py (conditionally `./dev/process_mock.py` and `./dev/debug_client.py` for debugging)

## Configuration

The script utilizes configuration settings from the `config` module, particularly the `DEBUG_MODE` flag, to determine the operational mode (debug or standard).

## Features

- **Concurrent Execution**: Utilizes threads to run `app.py` and potentially a mock process in parallel.
- **Conditional Debugging**: Depending on the `DEBUG_MODE`, it can execute additional debugging processes to aid in development and testing.
- **Subprocess Management**: Executes key components (`app.py`, `switch.py`, or debug processes) as subprocesses, ensuring isolated and controlled execution environments.

## Functions

### `run_app()`

Runs `app.py` as a subprocess. This script contains the core functionality of the application and is always executed regardless of the debug mode.

### `run_app2()`

Executes a mock process (`./dev/process_mock.py`) as a subprocess, intended for use in debug mode for development or testing purposes.

### `run_switch_or_debug_as_subprocess()`

Determines whether to run `switch.py` or the debug client (`./dev/debug_client.py`) based on the `DEBUG` flag from the configuration. In standard mode, `switch.py` is executed, which might be responsible for controlling hardware or network switches or other pivotal application functions. In debug mode, the debug client is executed to facilitate debugging and development.

## Execution Flow

1. **Initialization**: The script starts by launching `app.py` in a separate thread to ensure its core functionality runs concurrently with other components.
2. **Debug Mode Check**: If the application is in debug mode, it additionally starts a mock process in another thread for development or testing.
3. **Component Execution**: Depending on the operational mode, `main.py` executes either `switch.py` for standard operations or a debug client for debugging purposes.

## Running the Script

To execute the application, run the following command in the terminal:

```bash
python main.md
```
Ensure that all dependencies are properly installed and configured before running the script.