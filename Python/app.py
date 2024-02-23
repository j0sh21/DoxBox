from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QSize, QPoint
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
        self.desiredLoops = 2
        self.appState = appState
        self.initUI()
        self.appState.stateChanged.connect(self.onStateChanged)
        self.movie = QMovie(self)
        self.movieLabel = QLabel()
        self.movie.frameChanged.connect(self.onFrameChanged)
        self.total_duration = 0
        self.gif_path = ""
        self.isreplay = 0
        self.LED_HOST = config.LED_SERVER_HOST
        self.LED_PORT = config.LED_SERVER_PORT

    def send_msg_to_LED(self, command):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Connect to the server
            client_socket.connect((self.LED_HOST, self.LED_PORT))
            print(f"Connected to server at {self.LED_HOST}:{self.LED_PORT}")
            # Send the command to the server
            print(f"Sending command to {self.LED_HOST}:{command.encode('utf-8')}")
            client_socket.sendall(command.encode('utf-8'))

    def calculateDuration(self):
        # Calculate the total duration of the GIF
        frame_count = self.movie.frameCount()
        frame_rate = self.movie.nextFrameDelay()  # Delay between frames in milliseconds
        self.total_duration = frame_count * frame_rate / 1000  # Total duration in seconds
        print(f"Start playing gif with {str(self.total_duration)} seconds total duration")

    def onFrameChanged(self):
        if self.movie.currentFrameNumber() == 0: # Check if this is the first frame
            self.calculateDuration()
        elif self.movie.currentFrameNumber() == self.movie.frameCount() - 1:  # Check if it's the last frame
            self.movie.stop()
            self.onGIFFinished()

    def onGIFFinished(self):
        self.loopCount += 1
        if self.total_duration < 3.0 and self.appState.state not in ("2", "3"):
            if self.movie.currentFrameNumber() == self.movie.frameCount() - 1:  # Last frame
                if self.loopCount == 1:
                    if self.total_duration < 0.5:
                        self.desiredLoops *= 6
                    elif self.total_duration < 1.5:
                        self.desiredLoops *= 3
                    elif self.total_duration < 3.0:
                        self.desiredLoops *= 2
                elif self.loopCount >= self.desiredLoops:
                    self.movie.stop()
                    if self.appState.state == "1":
                        print(f"({self.desiredLoops}x) Payment GIF finished, next state: 2 and Gif")
                        self.appState.state = "2"
                    self.isreplay = 0
                    print(f"({self.desiredLoops}x) Loops finished, next random GIF for state: {self.appState.state}")
                    self.updateGIF(self.appState.state)
                else:
                    print(f"Replay GIF ({self.desiredLoops}x), total duration is < 3 seconds")
                    self.isreplay = 1
                    self.playGIF()

        else:
            self.isreplay = 0
            if self.appState.state in("1","2","3"):
                if self.appState.state == "1":
                    print("Payment GIF finished, next state: 2 and GIF")
                    self.appState.state = "2"
                elif self.appState.state == "2":
                    print("Countdown GIF finished, next state: 3 and GIF")
                    self.appState.state = "3"
                else:
                    print("Smile GIF finished, capture photo very soon")
                    try:
                        if self.loopCount == 1: #Only after 1st Loop
                            self.send_msg_to_LED("fade 0")
                            photo_thread = threading.Thread(target=self.photo_subprocess)
                            photo_thread.start()
                    except Exception as e:
                        print(f"Failed to start img_capture.py: {e}")
                        appState.stateChanged.emit("100")
            elif self.appState.state in("4", "100", "0"):
                print(f"GIF for state {self.appState.state} finished play next gif for state {self.appState.state} until external state change")
                self.updateGIF(self.appState.state)
            elif self.appState.state == "5":
                print("Thank You - GIF finished, initial state 0, start welcome GIF")
                self.appState.state = "0"
            else:
                self.updateGIF(self.appState.state)

    def playGIF(self):
        if self.isreplay == 0:
            self.loopCount = 0
            self.desiredLoops = 2
        self.movie.setFileName(self.gif_path)
        self.gifLabel.setMovie(self.movie)
        self.gifLabel.setScaledContents(True)
        self.movie.start()

    def updateGIF(self, state):
        # Map states to subfolders TODO: Some status messages does not reflect a floder eg. 204 and everything > 100
        subfolder_map = {
            "0": "0_welcome",
            "1": "1_payment",
            "2": "2_countdown",
            "3": "3_smile",
            "4": "4_print",
            "5": "5_thx",
            "100": "100_error"
        }

        # default value if state not in subfolder map
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
                    self.gifLabel.show()  # Make sure the gifLabel is visible
                    self.playGIF()
                except Exception as e:
                    print(f"Error while trying to start playing GIF: {str(e)}")
            else:
                print("No GIFs found in the specified folder.")
        except FileNotFoundError:
            print(f"The folder {gif_folder_path} does not exist.")

    def updatePicture(self, imagePath):
        pixmap = QPixmap(imagePath)
        self.pictureLabel.setPixmap(pixmap.scaled(800, 600, Qt.KeepAspectRatio))
        self.pictureLabel.show()

    def initUI(self):
        # Set the layout
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Picture Label (used for .PNG) positioned into the window inside the transparent background frame
        self.pictureLabel = QLabel(self)
        self.pictureLabel.setAlignment(Qt.AlignCenter)
        PicturePixmap = QPixmap(rf"../images/gifs/0_welcome/welcome.png") # static image
        self.pictureLabel.setPixmap(PicturePixmap.scaled(1026, 530, Qt.KeepAspectRatio))
        self.pictureLabel.setGeometry(100, 98, 1026, 530)

        # GIF Label setup positioned into the window inside the transparent background frame
        self.gifLabel = QLabel(self)
        self.gifLabel.setAlignment(Qt.AlignCenter)
        self.gifLabel.setGeometry(100, 98, 1026, 530)
        self.gifLabel.hide()

        # Background setup
        self.backgroundLabel = QLabel(self)
        pixmap = QPixmap(rf"{config.PATH_TO_FRAME}")
        self.backgroundLabel.setPixmap(pixmap)
        self.backgroundLabel.setScaledContents(True)
        self.backgroundLabel.setAlignment(Qt.AlignCenter)
        self.backgroundLabel.setAttribute(Qt.WA_TranslucentBackground)
        self.backgroundLabel.setGeometry(0, 0, 1600, 720) # TODO: read resolution from cfg.ini
        self.backgroundLabel.raise_()  # Move image to the foreground

        self.setAttribute(Qt.WA_TranslucentBackground)  # make background transparent
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint) # remove window frame

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
                    print("An unexpected printer error occurred:", error_message)

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
        # state handling
        if state == "0":
            self.send_msg_to_LED("breath 0")
            self.send_msg_to_LED("blink 0")
            self.send_msg_to_LED("fade 0")
            print(f"{'_' * 10}State changed to 0: Welcome screen{'_' * 10}")
            self.send_msg_to_LED("color 226 0 116")  # Set to lnbits color
            self.send_msg_to_LED("breathbrightness 0.1 0.7")
            self.send_msg_to_LED("breathspeed 0.09")
            self.send_msg_to_LED("breath 1")
        if state == "1":
            print(f"{'_' * 10}State changed to 1: Payment recived{'_' * 10}")
            self.send_msg_to_LED("breath 0")
            self.send_msg_to_LED("breathbrightness 0.2 0.8")
            self.send_msg_to_LED("breathspeed 0.02")
            self.send_msg_to_LED("breath 1")
        if state == "2":
            print(f"{'_' * 10}State changed to 2: Start countdown{'_' * 10}")
            self.send_msg_to_LED("breath 0")
            self.send_msg_to_LED("blinkspeed 0.5 0.5")
            self.send_msg_to_LED("blink 1")
        if state == "3":
            print(f"{'_' * 10}State changed to 3: Smile now{'_' * 10}")
            self.send_msg_to_LED("fade 1")
        if state == "4":
            print(f"{'_' * 10}State changed to 4: Start printing{'_' * 10}")
            self.send_msg_to_LED("color 226 0 116")
            self.send_msg_to_LED("breathbrightness 0.35 0.8")
            self.send_msg_to_LED("breathspeed 0.12")
            self.send_msg_to_LED("breath 1")
            try:
                print_thread = threading.Thread(target=self.print_subprocess)
                print_thread.start()
            except Exception as e:
                print(f"Failed to start print.py: {e}")
                appState.stateChanged.emit("100")
        if state == "5":
            print(f"{'_' * 10}State changed to 5: Thank You!{'_' * 10}")
            self.send_msg_to_LED("breath 0")
            self.send_msg_to_LED("fade 1")
        if state in("100", "101", "102", "103", "104", "110", "112", "113", "114", "115", "119"):
            self.send_msg_to_LED("color 255 0 0")
            self.send_msg_to_LED("blink 1")
        
        self.movie.stop()
        self.updateGIF(state)

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
    print("Building app...")
    app = QApplication(sys.argv)
    print("Building app completed!")
    print("Building state object...")
    appState = AppState()
    print("Building state object completed!")
    print("Building Display...")
    ex = VendingMachineDisplay(appState)
    print("Building Display completed!")
    # Start the server in a separate thread
    print("Start server...")
    server_thread = threading.Thread(target=start_server, args=(appState,))
    server_thread.start()
    print("Start app (display)")
    sys.exit(app.exec_())