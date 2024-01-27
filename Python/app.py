from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtMultimedia import QCamera, QCameraInfo
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import sys
import threading
import socket
import os
import random

# Import the configuration variables
import config  # Assuming config.py is in the same directory

# A class for managing the application state and communication
class AppState(QObject):
    stateChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._state = "0"

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        self.stateChanged.emit(self._state)

# Main application class
class VendingMachineDisplay(QWidget):
    def __init__(self, appState):
        super().__init__()
        self.appState = appState
        self.initUI()
        self.appState.stateChanged.connect(self.onStateChanged)

    def initUI(self):
        # Set the layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Set up the webcam viewfinder
        self.viewfinder = QCameraViewfinder(self)
        layout.addWidget(self.viewfinder)

        # Initialize and start the camera
        self.camera = QCamera(QCameraInfo.defaultCamera())
        self.camera.setViewfinder(self.viewfinder)
        self.camera.start()

        # Display a static image (e.g., QR code) with a smaller size
        self.imageLabel = QLabel(self)
        pixmap = QPixmap(config.IMAGE_PATH)  # Use the image path from config.py
        self.imageLabel.setPixmap(pixmap.scaled(config.IMAGE_WIDTH, config.IMAGE_HEIGHT, Qt.KeepAspectRatio))  # Use image dimensions from config.py
        layout.addWidget(self.imageLabel)

        # Initialize the QLabel for displaying GIFs
        self.gifLabel = QLabel(self)
        layout.addWidget(self.gifLabel)  # Add the gifLabel to the layout

        # Display text
        self.textLabel = QLabel(config.DEFAULT_TEXT, self)  # Use the default text from config.py
        self.textLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.textLabel)

        # Window configurations
        if config.FULLSCREEN_MODE:  # Check if fullscreen mode is enabled in config.py
            self.showFullScreen()
        else:
            self.setWindowTitle(config.WINDOW_TITLE)  # Use the window title from config.py
            self.show()  # Show in windowed mode if fullscreen is not enabled

    def onStateChanged(self, state):
        # Handle state changes here
        if state == "1":
            # For example, update the text label
            self.textLabel.setText("State changed to 1")
        # Add more state handling as needed

        # Update GIF based on the state
        self.updateGIF(state)

    def updateGIF(self, state):
        # Map states to subfolders
        subfolder_map = {
            "0": "0_welcome",
            "1": "1_payment",
            "2": "2_countdown",
            "3": "3_smile",
            "4": "4_print",
            "5": "5_thx",
            "100": "100_error"
        }

        #default value if state not in subfolder map
        subfolder = subfolder_map.get(state, "0_welcome")


        # Construct the path to the subfolder
        gif_folder_path = os.path.join("..", "images", "gifs", subfolder)

        # List all GIF files in the subfolder
        try:
            gifs = [file for file in os.listdir(gif_folder_path) if file.endswith(".gif")]
            if gifs:
                # Randomly select a GIF
                selected_gif = random.choice(gifs)
                gif_path = os.path.join(gif_folder_path, selected_gif)

                # Use QMovie to display the selected GIF
                movie = QMovie(gif_path)
                self.gifLabel.setMovie(movie)
                movie.start()
            else:
                print("No GIF files found in the specified folder.")
        except FileNotFoundError:
            print(f"The folder {gif_folder_path} does not exist.")

def handle_client_connection(client_socket, appState):
    try:
        message = client_socket.recv(1024).decode()
        print(f"Received message: {message}")
        appState.state = message
        client_socket.close()
    except Exception as e:
        print(f"Error in handling client connection: {e}")

def start_server(appState):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((config.SERVER_HOST, config.SERVER_PORT))  # Use server host and port from config.py
    server_socket.listen(config.MAX_CONNECTIONS)  # Use max connections from config.py
    print(f"App server listening on {config.SERVER_HOST}:{config.SERVER_PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection established with {addr}")
        client_thread = threading.Thread(target=handle_client_connection, args=(client_socket, appState))
        client_thread.start()

if __name__ == '__main__':
    print("building app...")
    app = QApplication(sys.argv)
    print("building app completed!")
    print("building state object...")
    appState = AppState()
    print("building state object completed!")
    print("building Display...")
    ex = VendingMachineDisplay(appState)
    print("building Display completed!")

    # Start the server in a separate thread
    print("Start server...")
    server_thread = threading.Thread(target=start_server, args=(appState,))
    server_thread.start()
    print("Start app")
    sys.exit(app.exec_())
