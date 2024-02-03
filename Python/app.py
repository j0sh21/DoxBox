import subprocess
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtMultimedia import QCamera, QCameraInfo, QCameraViewfinderSettings
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QSize, QRect, QPoint
import sys
import threading
import socket
import os
import random
import img_capture

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
        self.loopCount = 0
        self.desiredLoops = 2
        self.appState = appState
        self.initUI()
        self.appState.stateChanged.connect(self.onStateChanged)
        self.movie = QMovie(self)
        self.movieLabel = QLabel()
        self.movie.frameChanged.connect(self.onFrameChanged)

    def onFrameChanged(self, frameNumber):
        if frameNumber == self.movie.frameCount() - 1:  # Check if it's the last frame
            self.movie.stop()
            self.onGIFFinished()

    def onGIFFinished(self):
        self.updateGIF(appState.state)
        print("GIFF finished")

    def playGIF(self, gifPath):
        self.movie.setFileName(gifPath)
        self.gifLabel.setMovie(self.movie)
        self.loopCount = 0  # Reset loop count each time a new GIF is played
        self.movie.setScaledSize(QSize(500, 500))
        self.movie.start()

    def initUI(self):
        # Set the layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Header setup
        header = QLabel("Header")  # Or use a QWidget and customize it
        header.setFixedHeight(50)
        # Set the background color of the header to dark purple
        header.setStyleSheet("background-color: #301934; color: white;")  # Added color: white for the text
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Content area with sidebar and viewfinder
        contentLayout = QHBoxLayout()

        # Sidebar setup
        sidebar = QWidget()
        sidebar.setFixedWidth(150)
        sidebar.setStyleSheet("background-color: #301934; color: white;")  # Added color: white for the text
        sidebarLayout = QVBoxLayout(sidebar)
        sidebarLayout.setContentsMargins(0, 0, 0, 0)  # Remove any margins to ensure the QR code is at the very top
        sidebarLayout.setSpacing(0)  # Remove spacing between widgets in the sidebar

        # QR Code setup
        self.qrCodeLabel = QLabel(sidebar)
        pixmap = QPixmap(config.IMAGE_PATH)  # Use the image path from config.py
        self.qrCodeLabel.setPixmap(pixmap.scaled(config.IMAGE_WIDTH, config.IMAGE_HEIGHT,
                                                Qt.KeepAspectRatio))  # Use image dimensions from config.py
        self.qrCodeLabel.setAlignment(Qt.AlignCenter)  # Center the QR code horizontally in the sidebar
        # Add the QR code to the sidebar layout
        sidebarLayout.addWidget(self.qrCodeLabel)

        # Set up the webcam viewfinder
        self.viewfinder = QCameraViewfinder(self)
        layout.addWidget(self.viewfinder)

        contentLayout.addWidget(sidebar)
        contentLayout.addWidget(self.viewfinder, 1)  # The '1' makes the viewfinder expand

        # Add the content layout to the main layout
        layout.addLayout(contentLayout)

        # Initialize and start the camera
        self.camera = QCamera(QCameraInfo.defaultCamera())

        #build viewfinder instance
        viewfinder_settings = QCameraViewfinderSettings()
        viewfinder_settings.setResolution(1280, 720)  # Set Resolution

        # Vewfinder Settings
        self.camera.setViewfinderSettings(viewfinder_settings)
        self.camera.setViewfinder(self.viewfinder)

        self.camera.start()

        # Initialize the QLabel for displaying GIFs with the viewfinder as its parent
        self.gifLabel = QLabel(self.viewfinder)
        self.gifLabel.setAlignment(Qt.AlignCenter)  # Center the content
        self.gifLabel.setGeometry(QRect(0, 0, 500, 500))  # Set the geometry to 500x500 pixels
        self.gifLabel.hide()  # Initially hide the gifLabel

        # Display text in the middle of the screen, always on top
        self.textLabel = QLabel(config.DEFAULT_TEXT, self)
        self.textLabel.setAlignment(Qt.AlignCenter)
        self.textLabel.setStyleSheet(
            "background-color: rgba(255, 255, 255, 128);")  # Optional: Semi-transparent background
        self.textLabel.adjustSize()  # Adjust size based on text content
        self.repositionTextLabel()
        self.textLabel.raise_()

        # Window configurations
        if config.FULLSCREEN_MODE:  # Check if fullscreen mode is enabled in config.py
            self.showFullScreen()
        else:
            self.setWindowTitle(config.WINDOW_TITLE)
            self.show()

    def repositionTextLabel(self):
        # Center the textLabel within the window
        rect = self.textLabel.rect()
        self.textLabel.move((self.width() - rect.width()) // 2, (self.height() - rect.height()) // 2)

    def onStateChanged(self, state):
        # Mapping of states to messages
        state_messages = {
            "0": "State changed to 0",
            "1": "State changed to 1",
            "2": "State changed to 2",
            "3": "State changed to 3",
            "4": "State changed to 4",
            "5": "State changed to 5",
            "100": "State changed to 100"
        }

        # Update the text label based on the state
        message = state_messages.get(state, "Unknown state")
        print(str(state))
        self.textLabel.setText(message)

        # Add more state handling as needed
        self.movie.stop()
        self.updateGIF(state)

        if state == "1":
            print("State changed to 1")
        elif state == "2":
            try:
                if config.DEBUG_MODE > 1:
                    print("Simulate Photo")
                else:
                    subprocess.Popen(["python", "img_capture.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    print("img_capture.py started successfully.")
            except Exception as e:
                print(f"Failed to start img_capture.py: {e}")
        elif state == "3":
            time.sleep(2)
            print("take photo")
            img_capture.main()
        elif state == "4":
            if config.DEBUG_MODE > 2:
                print("Simulate print")
                subprocess.run(["python3", "./dev/printer_mock.py"])
            else:
                subprocess.run(["python3", ".print.py"])
        elif state == "5":
            print("Tahnk You!")

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
        try:
            print(str(state))
        except Exception as e:
            print(str(e))

        subfolder = subfolder_map.get(state, "dddd_welcome")

        # Construct the path to the subfolder
        gif_folder_path = os.path.join("..", "images", "gifs", subfolder)

        # List all GIF files in the subfolder
        try:
            gifs = [file for file in os.listdir(gif_folder_path) if file.endswith(".gif")]
            if gifs:
                # Randomly select a GIF
                selected_gif = random.choice(gifs)
                gif_path = os.path.join(gif_folder_path, selected_gif)
                self.gifLabel.setAlignment(Qt.AlignCenter)  # Center the content
                # Load the GIF
                try:
                    # Position the gifLabel in the center of the viewfinder
                    vfCenter = self.viewfinder.geometry().center()
                    gifTopLeft = vfCenter - QPoint(250, 250)  # Adjust for the size of the gifLabel
                    self.gifLabel.move(gifTopLeft)
                    self.gifLabel.show()  # Make sure the gifLabel is visible
                    self.playGIF(gif_path)
                except Exception as e:
                    print(str(e))
                print(f"{gif_path}")
            else:
                print("No GIF files found in the specified folder.")
        except FileNotFoundError:
            print(f"The folder {gif_folder_path} does not exist.")

def send_message_to_app(message):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((config.HOST, config.PORT))
        client_socket.sendall(message.encode())
        client_socket.close()
    except Exception as e:
        print(f"Error in sending message to app: {e}")

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
