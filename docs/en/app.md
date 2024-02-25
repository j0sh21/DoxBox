
# Documentation for app.py
## Overview 

`app.py` serves as a pivotal module in the application, orchestrating the user interface and facilitating user interactions. This module leverages the powerful PyQt5 framework to build a robust and responsive graphical user interface (GUI), making it a central piece for applications requiring user interaction through a visual interface.

## Purpose

The primary purpose of `app.py` is to define the structure and behavior of the application's GUI. It encapsulates the design and functionality of various UI components, including windows, widgets, layouts, and event handlers, ensuring a seamless and intuitive user experience.

## Scope

Within `app.py`, you'll find definitions for key classes and functions that collectively build up the application's front-end. This includes:

- **AppState**: A class designed for managing the application's state, allowing for dynamic updates and interactions within the GUI. It uses a `stateChanged` signal to notify other parts of the application when the state changes, promoting a reactive design where the UI can adjust based on the current application state.
- **VendingMachineDisplay**: A custom `QWidget` subclass that acts as the main container for the application's UI elements, organizing them into a coherent and functional layout.

## State Handling

The `AppState` class is central to the application's state management. It holds a `state` variable that reflects the current condition or mode of the application. Changes to this state are propagated through the `stateChanged` signal, enabling other components, especially the UI, to react and update accordingly. This approach decouples the state management from the UI logic, enhancing modularity and maintainability.

## Socket Programming and Server-Client Communication

The application features a server component that listens for incoming connections using Python's `socket` library. The `start_server` function initializes this server, which awaits messages from clients. Upon receiving a message, the `handle_client_connection` function processes it and updates the `AppState`, leveraging the state management system to reflect changes in the UI dynamically. This server-client setup allows for remote or automated control over the application, ideal for kiosk-like or vending machine scenarios.

## Key Features

- **Modular Design**: `app.py` follows a modular approach, separating concerns between state management and UI presentation, which facilitates maintainability and scalability.
- **State-Driven UI**: The application's UI dynamically responds to changes in application state, providing a reactive user experience that updates in real time to reflect the current context and data.
- **Integration with PyQt5**: By utilizing PyQt5, `app.py` leverages a comprehensive set of tools and widgets for creating professional-grade GUIs, including support for multimedia components, event handling, and custom widget styling.

## Dependencies

- **Qt Widgets**: Inherits from `QWidget` and may use other widgets such as `QLabel`, `QVBoxLayout`, `QHBoxLayout` from PyQt5.QtWidgets.
- **Qt Multimedia**: Potentially uses `QCamera`, `QCameraViewfinder` from PyQt5.QtMultimedia and `QCameraViewfinder` from PyQt5.QtMultimediaWidgets for camera integration.
- **Qt Core**: Utilizes classes like `QPixmap`, `QMovie` from PyQt5.QtGui, and `Qt`, `QSize`, `QRect`, `QPoint` from PyQt5.QtCore for core GUI functionalities.

## Multimedia Handling and GIF Animations

The `VendingMachineDisplay` class incorporates advanced multimedia handling capabilities, notably for playing and managing GIF animations.

### Playing GIF Animations

The application can display GIF animations as part of its UI, providing dynamic visual content. This is achieved through the `QMovie` class from PyQt5, which is used to load and play GIF files. The `VendingMachineDisplay` class includes methods to start playing a GIF, calculate its duration, and ensure it fits within the designated UI elements, offering a seamless multimedia experience.

### Key Methods

- **send_msg_to_LED(host, port, command)**: This method allows the application to communicate with external devices, such as an LED strip attached, over a network. It establishes a socket connection to the specified host and port, then sends a command, which could be used to display messages or control the LED strip.

- **calculateDuration()**: Calculates the total duration of a GIF animation by iterating through its frames. This information can be used to synchronize the GIF playback with other events in the application, ensuring a coherent user experience.

- **handle_client_connection(client_socket, appState)**: Handles incoming connections from clients. This function is a critical part of the server-client architecture, reading messages sent by clients, updating the application state based on these messages, and ensuring the UI reflects these changes.

- **start_server(appState)**: Initializes and starts the server that listens for incoming connections. It binds to a specified port and waits for clients to connect, creating a new thread to handle each connection, thus allowing the application to continue operating smoothly while managing client requests.


### GIF Replay Logic

The GIF replay logic in the DoxBox is designed to manage the playback of GIF animations based on the application's current state and the duration of the GIFs. This logic ensures that shorter GIFs are replayed a specified number of times to maintain user engagement, while longer GIFs transition smoothly to the next state or GIF when completed. Below is an overview of the key components and functionalities of the GIF replay logic.

#### Components:

- Movie Object: Represents the GIF animation to be played. It is responsible for managing the GIF playback.
- GIF Label: A graphical UI component (label) that displays the GIF animation.
- State Management: The application maintains a state that determines the context or phase it is currently in (e.g., payment, countdown, smile).

#### Key Attributes:

- `loopCount`: Tracks the number of times the current GIF has been replayed.
- `desiredLoops`: The desired number of times the GIF should be replayed, which varies based on the GIF's duration.
- `isreplay`: A flag indicating whether the current GIF playback is an original play (0) or a replay (1).
- `total_duration`: The total duration of the current GIF. Used to determine the number of desired loops for shorter GIFs.
- `gif_path`: The file path of the current GIF to be played.

#### Functions:

- `playGIF()`: Initiates the playback of a GIF. If `isreplay` is 0, it resets `loopCount` and `desiredLoops` for a new GIF. If `isreplay` is 1, it replays the current GIF without resetting the loop count.
- `updateGIF(state)`: Updates the current GIF based on the application's state. It selects a random GIF from a specified subfolder corresponding to the current state and sets it up for playback.
- `onGIFFinished()`: Triggered when a GIF finishes playing. It manages the logic for replaying or transitioning GIFs based on their duration and the application's state.

#### GIF Duration and Replay Times:

- Duration < 0.6 seconds: For GIFs shorter than 0.6 seconds, the desired number of replays (`desiredLoops`) is set to 6 times. This ensures that very short GIFs are played enough times to be noticeable and engaging to the user.
- Duration between 0.6 and 1.6 seconds: For GIFs with a duration between 0.6 seconds and 1.6 seconds, the GIF is replayed 3 times. This duration range covers moderately short GIFs that require fewer replays to maintain user engagement.
- Duration between 1.6 and 3.3 seconds: GIFs falling within this duration range are replayed 2 times. These are considered short but not so brief that they require many replays to be effective.

#### Logic Flow with Specific Durations:

- Initial Playback: Upon selecting a new GIF, `playGIF()` is called with `isreplay` set to 0. This initializes the playback, setting `loopCount` to 0 and `desiredLoops` to 1.
- Determining Replay Needs: When a GIF completes (`onGIFFinished()`), the logic checks the total duration (`total_duration`) of the GIF and the current application state. If the state is not "2" or "3" and the GIF's duration is less than 3.3 seconds, it proceeds to determine the number of replays based on the specific duration brackets mentioned above.
- Replay Execution: If the GIF meets the criteria for replay, `isreplay` is set to 1, and `playGIF()` is called again. This increments `loopCount` each time the GIF completes a loop. The replay continues until `loopCount` reaches `desiredLoops`.
- Transition or Update: After completing the desired number of replays, or if the GIF does not meet the replay criteria (either due to its duration being longer than 3.3 seconds or the application state), the application either transitions to a new state or selects a new GIF based on the current state.


## Messages Handled by app.py

The application uses numeric strings as messages to represent different states and actions within the application. Each message triggers specific behaviors, correlating with various functionalities or visual feedback through the GUI. Below is a table summarizing the numeric messages and their corresponding effects within the application:

**State Messages**:

| Message | Description                                                                   |
|---------|-------------------------------------------------------------------------------|
| "0"     | represents an initial or welcome state.                                       |
| "1"     | indicate a payment or transaction completed.                                  |
| "2"     | Start the countdown, preparation phase following a payment.                   |
| "3"     | signifies the completion of a countdown, moving towards capturing the photo.  |
| "4"     | Photo captured successfully, start to print now.                              |
| "5"     | Printing finished: "Thank You" or completion state, the end of a transaction. |
| "144"   | Underpaid                                                                     |
| "204"   | Image deleted successfully after print.                                       |


**Error Messages**:

| Message | Description                                |
|---------|--------------------------------------------|
| "100"   | General Error in app.py.                   |
| "101"   | Camera found no focus                      |
| "102"   | no Camera found                            |
| "103"   | file not found                             |
| "104"   | permission denied                          |
| "110"   | general error in print.py                  |
| "112"   | printer not found                          |
| "113"   | file not found                             |
| "114"   | permission denied                          |
| "115"   | error copy file                            |
| "116"   | Print job stopped or canceled.             |
| "119"   | error while creating print job             |
| "120"   | general error in img_capture.py            |
| "130"   | general error in led.py                    |
| "140"   | Unexpected error in switch.py              |
| "141"   | LNbits API Response status code is not 200 |
| "142"   | Connection error with LNbits API           |
| "143"   | initial Connection error with LNbits API   |


These messages are processed by the application to update the `AppState` and, by extension, the UI and any external displays connected to the application. The specific actions taken in response to each message can vary depending on the current application context and the intended workflow.

## Usage

Developers working with `app.py` can expect to interact with high-level abstractions for UI components, straightforward mechanisms for state management, and event-driven programming patterns. This module is typically invoked as part of the application's startup process, initializing the GUI and binding it to the underlying logic and data models.

# AppState Class Documentation

## Overview

The `AppState` class, defined within `app.py`, is a fundamental component designed for managing the application's state and enabling inter-component communication in a Qt-based GUI application. It inherits from `QObject` to utilize Qt's signal-slot mechanism, making it suitable for applications that require dynamic responses to state changes.

## Features

- **State Management**: Centralizes the management of the application's state, providing a single source of truth for the state-related logic.
- **Signal Emission**: Employs Qt's signal mechanism (`pyqtSignal`) to emit events when the application's state changes, allowing other components to react to these changes in a decoupled manner.

## Class Definition

### Properties

- `state`: A property that encapsulates the application's current state. Access to this property is controlled through a getter and a setter to ensure that state changes are managed consistently.

### Signals

- `stateChanged(str)`: A signal emitted whenever the state changes, carrying the new state value as a string. This signal can be connected to slots or functions within other components, enabling them to respond to state changes.

## Usage

The `AppState` class is typically instantiated once and used throughout the application to manage and observe the application's state. Components that need to respond to state changes can connect their slots or functions to the `stateChanged` signal.

### Example

```python
# Instantiation
app_state = AppState()

# Connect a function to the stateChanged signal
def on_state_changed(new_state):
    print(f"Application state changed to: {new_state}")

app_state.stateChanged.connect(on_state_changed)

# Update the state
app_state.state = "1"  # This will emit the stateChanged signal and invoke on_state_changed
```

# VendingMachineDisplay Class Documentation

## Overview

The `VendingMachineDisplay` class, defined within `app.py`, is a crucial component of the application's graphical user interface (GUI). It inherits from `QWidget`, making it a versatile container for various UI elements. This class is primarily responsible for constructing and managing the layout, controls, and other visual elements that constitute the application's user interface.

## Dependencies

- **Qt Widgets**: Inherits from `QWidget` and may use other widgets such as `QLabel`, `QVBoxLayout`, `QHBoxLayout` from PyQt5.QtWidgets.
- **Qt Multimedia**: Potentially uses `QCamera`, `QCameraViewfinder` from PyQt5.QtMultimedia and `QCameraViewfinder` from PyQt5.QtMultimediaWidgets for camera integration.
- **Qt Core**: Utilizes classes like `QPixmap`, `QMovie` from PyQt5.QtGui, and `Qt`, `QSize`, `QRect`, `QPoint` from PyQt5.QtCore for core GUI functionalities.

## Features

- **Layout Management**: Manages the arrangement of UI elements using layouts (e.g., `QVBoxLayout`, `QHBoxLayout`), ensuring a responsive and organized display.
- **State Integration**: Integrates with the `AppState` class to reflect and potentially modify the application's state based on user interactions or other events.
- **Multimedia Support**: If camera functionality is used, it may include features like live camera feed display, utilizing `QCamera` and `QCameraViewfinder`.

## Class Definition

### Constructor

- `__init__(self, appState)`: Initializes a new instance of the `VendingMachineDisplay` class, taking an `AppState` object as an argument to facilitate state management and interaction.

### Key Methods

- The class includes methods to initialize UI components, set up layouts, and connect signals to slots for event handling (e.g., button clicks, state changes).

## Usage

The `VendingMachineDisplay` class is instantiated as part of the application's GUI setup process, often in the main script or a dedicated GUI module. It requires an `AppState` instance to allow for state-based UI updates and interactions.

### Example

```python
app = QApplication(sys.argv)
app_state = AppState()
vending_machine_display = VendingMachineDisplay(app_state)
vending_machine_display.show()
sys.exit(app.exec_())
```