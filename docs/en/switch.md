# Documentation for switch.py

## Overview

The `switch.py` module is a critical component of the DoxBox application, responsible for monitoring external `LNbitsAPI data`, detecting significant changes, and communicating with other parts of the DoxBox e.g. `app.py` to trigger specific actions (e.g. Take Photo) based on these changes. It uses network requests, threading, and socket programming to achieve its objectives.

## Dependencies

- **Standard Libraries**: requests, time, threading, socket
- **Project Modules**: config

## Configuration

The module relies on various settings defined in the `config` module, including:

- `API_URL`: The URL of the external API to monitor.
- `API_KEY`: The key required for API authentication.
- `HOST, PORT`: Network settings for socket communication.
- `AMOUNT_THRESHOLD`: A specific threshold value that triggers an action when met.
- `CHECK_INTERVAL`, `POST_PAYMENT_DELAY`: Time intervals for operational pacing.

## Key Functions

### `send_message_to_app(message)`

Sends a message to another application component `app.py` using socket programming. This function encapsulates the network communication logic, including error handling.

### `main_loop()`

The core function that runs in a continuous loop, performing the following actions:

1. Fetches data from an external API using the `requests` library.
2. Monitors for changes in data, specifically looking for changes in a `payment_hash` value.
3. When a change is detected and certain conditions are met (e.g., an amount threshold), triggers an action by sending a message to another component.
4. Incorporates delay mechanisms to manage the frequency of API requests and subsequent actions.

## Execution Flow

1. Initializes and starts the main loop in a separate thread to ensure non-blocking execution.
2. Continuously monitors an external API for changes, using a hash value as an indicator.
3. Communicates with other application components via sockets to coordinate actions based on detected changes.

## Running the Module

To run `switch.py`, execute the following command in a terminal:

```bash
python3 switch.py
