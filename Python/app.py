from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtMultimedia import QCamera, QCameraInfo
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import sys
import threading
import socket

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
        pixmap = QPixmap(r"images/qr/madeirax3.png")  # Replace with your image path
        self.imageLabel.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))  # Resize QR code
        layout.addWidget(self.imageLabel)

        # Display text
        self.textLabel = QLabel("Your Text Here", self)
        self.textLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.textLabel)

        # Window settings
        self.setWindowTitle('Vending Machine Display')
        #self.setGeometry(100, 100, 1024, 600)  # Set fixed size for window
        self.showFullScreen()

    def onStateChanged(self, state):
        # Handle state changes here
        if state == "1":
            # For example, update the text label
            self.textLabel.setText("State changed to 1")
        # Add more state handling as needed

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
    server_socket.bind(('localhost', 9999))
    server_socket.listen(5)
    print("App server listening on port 9999")

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
