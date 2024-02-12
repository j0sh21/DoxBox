from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtMultimedia import QCamera, QCameraInfo, QCameraViewfinderSettings
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QSize, QRect, QPoint
import subprocess
import sys
import threading
import socket
import os
import random
import config  #config.py from the same directory

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

# Main application class (Display)
class VendingMachineDisplay(QWidget):
    def __init__(self, appState):
        super().__init__()
        self.loopCount = 0
        self.desiredLoops = 3
        self.appState = appState
        self.initUI()
        self.appState.stateChanged.connect(self.onStateChanged)
        self.movie = QMovie(self)
        self.movieLabel = QLabel()
        self.movie.frameChanged.connect(self.onFrameChanged)
        self.total_duration = 0
        self.gif_path = ""

    def send_msg_to_LED(self , host, port, command):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Connect to the server
            client_socket.connect((host, port))
            print(f"Connected to server at {host}:{port}")
            # Send the command to the server
            print(f"Sending command to {host}:{command.encode('utf-8')}")
            client_socket.sendall(command.encode('utf-8'))

    def calculateDuration(self, frame_number):
        if frame_number == 0:  # Check if this is the first frame
            # Calculate the total duration of the GIF
            frame_count = self.movie.frameCount()
            frame_rate = self.movie.nextFrameDelay()  # Delay between frames in milliseconds
            self.total_duration = frame_count * frame_rate / 1000  # Total duration in seconds
            print(f"Start playing gif with {str(self.total_duration)} total duration")

    def onFrameChanged(self, frameNumber):
        self.calculateDuration(self.movie.currentFrameNumber())
        if frameNumber == self.movie.frameCount() - 1:  # Check if it's the last frame
            self.movie.stop()
            self.onGIFFinished()

    def onGIFFinished(self):
        HOST, PORT = '127.0.0.1', 12345  # Change host and port if needed
        self.loopCount += 1
        if self.total_duration < 3.0 and self.appState.state not in ("2", "3"):
            if self.movie.currentFrameNumber() == self.movie.frameCount() - 1:  # Last frame
                if self.loopCount == 1:
                    if self.total_duration < 0.5:
                        self.desiredLoops *= 6
                    elif self.total_duration < 1.0:
                        self.desiredLoops *= 3
                    elif self.total_duration < 2.0:
                        self.desiredLoops *= 2
                if self.loopCount >= self.desiredLoops:
                    self.movie.stop()
                    if self.appState.state == "1":
                        print(f"({self.desiredLoops}x) Payment GIFF finished, next State: 2 and Gif")
                        self.appState.state = "2"
                    print(f"({self.desiredLoops}x) Loops finished, next random Gif for State: {self.appState.state}")
                    self.updateGIF(self.appState.state)
                else:
                    print(f"Replaying Gif ({self.desiredLoops}x), total duration is < 3 seconds")
                    self.playGIF()

        else:
            if self.appState.state in("1","2","3"):
                if self.appState.state == "1":
                    print("Payment GIFF finished, next State: 2 and Gif")
                    self.appState.state = "2"
                elif self.appState.state == "2":
                    print("Countdown GIFF finished, next State: 3 and Gif")
                    self.appState.state = "3"
                else:
                    print("Smile GIFF finished, capture Photo very soon")
                    try:
                        if self.loopCount == 1: #Only after 1st Loop
                            self.send_msg_to_LED(HOST, PORT, "color 255 255 255")
                            photo_thread = threading.Thread(target=self.photo_subprocess)
                            photo_thread.start()
                    except Exception as e:
                        print(f"Failed to start img_capture.py: {e}")
                        appState.stateChanged.emit("100")
            elif self.appState.state in("4", "100", "0"):
                print(f"Gif for state {self.appState.state} finished play next gif for state {self.appState.state} until external state change")
                self.updateGIF(self.appState.state)
            elif self.appState.state == "5":
                print("Thank You GIFF finished, initial State 0 and start welcome Gif")
                self.appState.state = "0"
            else:
                self.updateGIF(self.appState.state)

    def playGIF(self):
        self.movie.setFileName(self.gif_path)
        self.gifLabel.setMovie(self.movie)
        self.movie.setScaledSize(QSize(500, 500))
        self.movie.start()


    def initUI(self):
        # Set the layout
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
               
        # Background setup
        self.backgroundLabel = QLabel(self)
        pixmap = QPixmap(rf"{config.PATH_TO_FRAME}")
        self.backgroundLabel.setPixmap(pixmap)
        self.backgroundLabel.setScaledContents(True)
        self.backgroundLabel.setAlignment(Qt.AlignCenter)
        self.backgroundLabel.setAttribute(Qt.WA_TranslucentBackground)
        self.backgroundLabel.setGeometry(0, 0, 1600, 720)
        self.backgroundLabel.raise_()  # Bringe das Hintergrundbild nach vorne
        
        # Webcam Viewfinder setup
        self.viewfinder = QCameraViewfinder(self)
        viewfinderX = int((1600 - 1280) / 2)
        viewfinderY = int((720 - 720) / 2)
        self.setStyleSheet("""
            QCameraViewfinder {
                border-radius: 90px;
                background-color: transparent;
            }
        """)
        self.viewfinder.setGeometry(80, 70, int(1280*.79), int(720*.79))  # Korrektur der Größe


        # Initialize and start the camera
        self.camera = QCamera(QCameraInfo.defaultCamera())
        viewfinder_settings = QCameraViewfinderSettings()
        viewfinder_settings.setResolution(1280, 720)
        self.camera.setViewfinderSettings(viewfinder_settings)
        self.camera.setViewfinder(self.viewfinder)
        self.camera.start()
        
        # GIF Label setup within viewfinder
        self.gifLabel = QLabel(self.viewfinder)
        self.gifLabel.setAlignment(Qt.AlignCenter)
        gifLabelX = int((1280 - 500) / 2)  # Center the gif label within the viewfinder
        gifLabelY = int((720 - 500) / 2) 
        self.gifLabel.setGeometry(gifLabelX, gifLabelY, 500, 500)
        self.gifLabel.hide()

        # Setze Transparenz und Fenstereigenschaften auf das Hauptfenster (TODO:Funktioniert nicht wie gewünscht, wir nutzen den scharzen frame als "rahmen".)
        self.setAttribute(Qt.WA_TranslucentBackground)  # Fensterhintergrund transparent machen
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        if config.FULLSCREEN_MODE:
            self.showFullScreen()
        else:
            self.setWindowTitle(config.WINDOW_TITLE)
            self.show()


    def print_subprocess(self):
        if config.DEBUG_MODE == 1:
            print("DEBUG MODE: Simulate print")
            subprocess.run(["python3", "dev/printer_mock.py"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            try:
                result = subprocess.run(["python3", "print.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        text=True, check=True)
                print("Output:", result.stdout)
            except subprocess.CalledProcessError as e:
                # This block will run if the subprocess returns a non-zero exit status
                error_message = e.stderr  # Capture the stderr from the error

                if "No printer" in error_message:
                    print("Error: No printer found. Please ensure the printer is connected properly.")
                else:
                    print("An unexpected error with the printer occurred:", error_message)

    def photo_subprocess(self):
        if config.DEBUG_MODE == 1:
            print("DEBUG MODE: Simulate Photo")
        else:
            try:
                process = subprocess.Popen(["python3", "img_capture.py"],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print("img_capture.py started successfully.")
                # Reading the output and errors for debugging
                stdout, stderr = process.communicate()

                if stdout:
                    print("Output:", stdout.decode())
                if stderr:
                    print("Error:", stderr.decode())
            except Exception as e:
                print(f"Failed to start img_capture.py: {e}")
                appState.stateChanged.emit("100")

    def onStateChanged(self, state):
        HOST, PORT = '127.0.0.1', 12345  # Change host and port if needed
        # state handling
        if state == "0":
            print(f"{'_' * 10}State changed to 0: Welcome Screen{'_' * 10}")
            self.send_msg_to_LED(HOST, PORT, "color 103 58 183")  # Set to lnbits color
            self.send_msg_to_LED(HOST, PORT, "blink 1")
            self.send_msg_to_LED(HOST, PORT, "fade 1")
        if state == "1":
            print(f"{'_' * 10}State changed to 1: Payment recived{'_' * 10}")
            self.send_msg_to_LED(HOST, PORT, "color 0 255 0")
            self.send_msg_to_LED(HOST, PORT, "breath 3")
        if state == "2":
            print(f"{'_' * 10}State changed to 2: Start Countdown{'_' * 10}")
            self.send_msg_to_LED(HOST, PORT, "blink 10")
        if state == "3":
            print(f"{'_' * 10}State changed to 3: Smile Now{'_' * 10}")
        if state == "4":
            print(f"{'_' * 10}State changed to 4: Start printing{'_' * 10}")
            self.send_msg_to_LED(HOST, PORT, "breath 10")
            try:
                print_thread = threading.Thread(target=self.print_subprocess)
                print_thread.start()
            except Exception as e:
                print(f"Failed to start print.py: {e}")
                appState.stateChanged.emit("100")
        if state == "5":
            print(f"{'_' * 10}State changed to 5: Tahnk You!{'_' * 10}")
            self.send_msg_to_LED(HOST, PORT, "color 0 255 0")
            self.send_msg_to_LED(HOST, PORT, "fade 1")
        if state == "100":
            self.send_msg_to_LED(HOST, PORT, "color 255 0 0")

        self.movie.stop()
        self.updateGIF(state)

    def updateGIF(self, state):
        self.loopCount = 0  # Reset loop count each time a new GIF is played
        self.desiredLoops = 0 # Reset desired Loops count each time a new GIF is played
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
                self.gif_path = os.path.join(gif_folder_path, selected_gif)
                self.gifLabel.setAlignment(Qt.AlignCenter)  # Center the content
                # Load the GIF
                try:
                    # Position the gifLabel in the center of the viewfinder
                    vfCenter = self.viewfinder.geometry().center()
                    gifTopLeft = vfCenter - QPoint(250, 250)  # Adjust for the size of the gifLabel
                    self.gifLabel.move(gifTopLeft)
                    self.gifLabel.show()  # Make sure the gifLabel is visible
                    self.playGIF()
                except Exception as e:
                    print(f"Error while try to start playing Gif: {str(e)}")
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
    print("app.py is now running")
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
    print("Start app (display)")
    sys.exit(app.exec_())