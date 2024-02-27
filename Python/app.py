from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import subprocess
import sys
import threading
import socket
import os
import random
import config  #config.py from the same directory


# A class for managing the DoxBox state and communication with other python subprocesses
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

# Main DoxBox class (Display)
class VendingMachineDisplay(QWidget):
    def __init__(self, appState):
        super().__init__()
        self.loopCount = 0
        self.desiredLoops = 1
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

    def send_message_to_mini_display(self, command):
        if config.DEBUG_MODE == 0:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect(('localhost', 6548))
                client_socket.sendall(command.encode('utf-8'))
        else:
            print(command)

    def send_msg_to_LED(self, command):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.LED_HOST, self.LED_PORT))
            client_socket.sendall(command.encode('utf-8'))

    def calculateDuration(self):
        frame_count = self.movie.frameCount()
        frame_rate = self.movie.nextFrameDelay()  # Delay between frames in milliseconds
        self.total_duration = frame_count * frame_rate / 1000
        if not self.appState.state == 0:
            if self.total_duration > 0.16:
                self.send_message_to_mini_display(f"Start playing gif with {str(self.total_duration)} seconds total duration")

    def onFrameChanged(self):
        if self.movie.currentFrameNumber() == 0:
            self.calculateDuration()
        elif self.movie.currentFrameNumber() == self.movie.frameCount() - 1:
            self.movie.stop()
            self.onGIFFinished()

    def onGIFFinished(self):
        self.loopCount += 1
        last_gif_frame = self.movie.currentFrameNumber() == self.movie.frameCount() - 1
        if self.total_duration < 3.3 and self.appState.state not in ("2", "3") and last_gif_frame:
            if self.loopCount == 1:
                if self.total_duration < 0.6:
                    self.desiredLoops *= 6
                elif self.total_duration < 1.6:
                    self.desiredLoops *= 3
                else:
                    self.desiredLoops *= 2
            if self.loopCount >= self.desiredLoops:
                self.movie.stop()
                self.isreplay = 0
                if self.appState.state == "1":
                    self.send_message_to_mini_display(f"({self.desiredLoops}x) Loops of Payment GIF finished, next state: 2 and GIF")
                    self.appState.state = "2"
                    self.updateGIF(self.appState.state)
                elif self.appState.state == "5":
                    self.appState.state = "0"
                    self.send_message_to_mini_display(f"({self.desiredLoops}x) Loops of the Thank You - GIF finished, initial state 0, start welcome PNG")
                else:
                    self.send_message_to_mini_display(f"({self.desiredLoops}x) Loops finished, next random GIF for state: {self.appState.state}")
                    self.updateGIF(self.appState.state)
            else:
                self.send_message_to_mini_display(f"Replay GIF ({self.desiredLoops}x), total duration is < 3 seconds")
                self.isreplay = 1
                self.playGIF()
        elif last_gif_frame:
            self.isreplay = 0
            if self.appState.state == "1":
                self.send_message_to_mini_display("Payment GIF finished, next state: 2 and GIF")
                self.appState.state = "2"
                self.updateGIF(self.appState.state)
            elif self.appState.state == "2":
                self.send_message_to_mini_display("Countdown GIF finished, next state: 3 and GIF")
                self.appState.state = "3"
                self.updateGIF(self.appState.state)
            elif self.appState.state == "3":
                self.send_message_to_mini_display("Smile GIF finished, capture photo very soon")
                try:
                    if self.loopCount == 1: #Only after 1st Loop
                        self.send_msg_to_LED("fade 0")
                        self.appState.state = "3.5"
                        photo_thread = threading.Thread(target=self.photo_subprocess)
                        photo_thread.start()
                except Exception as e:
                    self.send_message_to_mini_display(f"Failed to start img_capture.py: {e}")
                    self.appState.state = "100"
                    self.updateGIF(self.appState.state)
            elif self.appState.state in("4", "100", "0", "3.9", "204"):
                self.send_message_to_mini_display(f"GIF for state {self.appState.state} finished play next gif for state {self.appState.state} until external state change")
                self.updateGIF(self.appState.state)
            elif self.appState.state == "5":
                self.send_message_to_mini_display("Thank You - GIF finished, initial state 0, start welcome GIF")
                self.appState.state = "0"
                self.updateGIF(self.appState.state)
            else:
                self.updateGIF(self.appState.state)

    def playGIF(self):
        if self.isreplay == 0:
            self.send_message_to_mini_display("Play GIF")
            self.loopCount = 0
            self.desiredLoops = 1
        else:
            self.send_message_to_mini_display("Replay GIF")

        self.movie.setFileName(self.gif_path)
        self.gifLabel.setMovie(self.movie)
        self.gifLabel.setScaledContents(True)
        self.movie.start()

    def updateGIF(self, state):
        if state != "3.5":
            subfolder_map = {
                "0": "0_welcome",
                "1": "1_payment",
                "2": "2_countdown",
                "3": "3_smile",
                "3.5": "3_smile",
                "3.9": "4_print",
                "4": "4_print",
                "204": "4_print",
                "5": "5_thx",
                "100": "100_error"
            }

            subfolder = subfolder_map.get(state, "100_error")
            gif_folder_path = os.path.join("..", "images", "gifs", subfolder)

            try:
                gifs = [file for file in os.listdir(gif_folder_path) if file.endswith(".gif")]
                if gifs:
                    selected_gif = random.choice(gifs)
                    self.gif_path = os.path.join(gif_folder_path, selected_gif)
                    self.gifLabel.setAlignment(Qt.AlignCenter)
                    try:
                        self.gifLabel.show()
                        self.playGIF()
                    except Exception as e:
                        self.send_message_to_mini_display(f"Error while trying to start playing GIF: {str(e)}")
                else:
                    self.send_message_to_mini_display("No GIFs found in the specified folder.")
            except FileNotFoundError:
                self.send_message_to_mini_display(f"The folder {gif_folder_path} does not exist.")
        else:
            self.send_message_to_mini_display("Replay same smile gif...")
            self.playGIF()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Picture Label (used for .PNG) positioned into the window inside the transparent background frame
        self.pictureLabel = QLabel(self)
        self.pictureLabel.setAlignment(Qt.AlignCenter)
        PicturePixmap = QPixmap(rf"{config.IMAGE_PATH}") # static image
        self.pictureLabel.setPixmap(PicturePixmap.scaled(1026, 530, Qt.KeepAspectRatio)) #TODO: read resolution from cfg.ini
        self.pictureLabel.setGeometry(100, 98, 1026, 530) #TODO: read resolution from cfg.ini

        # GIF Label setup positioned into the window inside the transparent background frame
        self.gifLabel = QLabel(self)
        self.gifLabel.setAlignment(Qt.AlignCenter)
        self.gifLabel.setGeometry(100, 98, 1026, 530) #TODO: read resolution from cfg.ini
        self.gifLabel.hide()

        # Background setup
        self.backgroundLabel = QLabel(self)
        pixmap = QPixmap(rf"{config.PATH_TO_FRAME}")
        self.backgroundLabel.setPixmap(pixmap)
        self.backgroundLabel.setScaledContents(True)
        self.backgroundLabel.setAlignment(Qt.AlignCenter)
        self.backgroundLabel.setAttribute(Qt.WA_TranslucentBackground)
        self.backgroundLabel.setGeometry(0, 0, 1600, 720) # TODO: read resolution from cfg.ini
        self.backgroundLabel.raise_()

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        if config.FULLSCREEN_MODE:
            self.showFullScreen()
            self.setCursor(Qt.BlankCursor)
        else:
            self.setWindowTitle(config.WINDOW_TITLE)
            self.show()

    def print_subprocess(self):
        if config.DEBUG_MODE == 1:
            self.send_message_to_mini_display("DEBUG MODE: Simulate print")
            subprocess.run(["python3", "dev/printer_mock.py"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            try:
                result = subprocess.run(["python3", "print.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        text=True, check=True)
                self.send_message_to_mini_display("Output:", result.stdout)
            except subprocess.CalledProcessError as e:
                error_message = e.stderr

                if "No printer" in error_message:
                    self.send_message_to_mini_display("Error: No printer found. Please ensure the printer is connected properly.")
                else:
                    self.send_message_to_mini_display("An unexpected printer error occurred:", error_message)

    def photo_subprocess(self):
        if config.DEBUG_MODE == 1:
            self.send_message_to_mini_display("DEBUG MODE: Simulate Photo")
        else:
            try:
                process = subprocess.Popen(["python3", "img_capture.py"],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.send_message_to_mini_display("img_capture.py started successfully.")
                stdout, stderr = process.communicate()

                if stdout:
                    self.send_message_to_mini_display("Output:", stdout.decode())
                if stderr:
                    self.send_message_to_mini_display("Error:", stderr.decode())
            except Exception as e:
                self.send_message_to_mini_display(f"Failed to start img_capture.py: {e}")
                appState.stateChanged.emit("100")

    def onStateChanged(self, state):
        # state handling
        if state == "0":
            self.send_msg_to_LED("breath 0")
            self.send_msg_to_LED("blink 0")
            self.send_msg_to_LED("fade 0")
            self.send_message_to_mini_display(f"{'_' * 10}State changed to 0: Welcome screen{'_' * 10}")
            self.send_msg_to_LED("color 226 0 116")  # Set to lnbits color
            self.send_msg_to_LED("breathbrightness 0.1 0.7")
            self.send_msg_to_LED("breathspeed 0.02")
            self.send_msg_to_LED("breath 1")
        if state == "1":
            self.send_message_to_mini_display(f"{'_' * 10}State changed to 1: Payment recived{'_' * 10}")
            self.send_msg_to_LED("breath 0")
            self.send_msg_to_LED("breathbrightness 0.2 0.8")
            self.send_msg_to_LED("breathspeed 0.005")
            self.send_msg_to_LED("breath 1")
        if state == "2":
            self.send_message_to_mini_display(f"{'_' * 10}State changed to 2: Start countdown{'_' * 10}")
            self.send_msg_to_LED("breath 0")
            self.send_msg_to_LED("blinkspeed 0.5 0.5")
            self.send_msg_to_LED("blink 1")
        if state == "3":
            self.send_message_to_mini_display(f"{'_' * 10}State changed to 3: Smile now{'_' * 10}")
            self.send_msg_to_LED("fadespeed 2.3")
            self.send_msg_to_LED("fade 1")
        if state == "4":
            self.send_message_to_mini_display(f"{'_' * 10}State changed to 4: Start printing{'_' * 10}")
            self.send_msg_to_LED("color 226 0 116")
            self.send_msg_to_LED("breathbrightness 0.35 0.8")
            self.send_msg_to_LED("breathspeed 0.1")
            self.send_msg_to_LED("breath 1")
            try:
                print_thread = threading.Thread(target=self.print_subprocess)
                print_thread.start()
            except Exception as e:
                self.send_message_to_mini_display(f"Failed to start print.py: {e}")
                appState.stateChanged.emit("100")
        if state == "5":
            self.send_message_to_mini_display(f"{'_' * 10}State changed to 5: Thank You!{'_' * 10}")
            self.send_msg_to_LED("breath 0")
            self.send_msg_to_LED("fadespeed 1")
            self.send_msg_to_LED("fade 1")
        if state in("100", "101", "102", "103", "104", "110", "112", "113", "114", "115", "119"):
            self.send_msg_to_LED("color 255 0 0")
            self.send_msg_to_LED("blinkspeed 0.5 0.5")
            self.send_msg_to_LED("blink 1")
        
        self.movie.stop()
        self.updateGIF(state)


def send_message_to_mini_display(command):
    if config.DEBUG_MODE == 0:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(('localhost', 6548))
            client_socket.sendall(command.encode('utf-8'))
    else:
        print(command)

def handle_client_connection(client_socket, appState):
    try:
        message = client_socket.recv(1024).decode()
        send_message_to_mini_display(f"Received message: {message}")
        appState.state = message
        client_socket.close()
    except Exception as e:
        send_message_to_mini_display(f"Error in handling client connection: {e}")

def start_server(appState):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((config.SERVER_HOST, config.SERVER_PORT))
    server_socket.listen(config.MAX_CONNECTIONS)
    send_message_to_mini_display(f"App server listening on {config.SERVER_HOST}:{config.SERVER_PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        if config.DEBUG_MODE != 0:
            send_message_to_mini_display(f"Connection established with {addr}")
        client_thread = threading.Thread(target=handle_client_connection, args=(client_socket, appState))
        client_thread.start()


if __name__ == '__main__':
    send_message_to_mini_display("app.py is now running")
    send_message_to_mini_display("Building app...")
    app = QApplication(sys.argv)
    send_message_to_mini_display("Building app completed!")
    send_message_to_mini_display("Building state object...")
    appState = AppState()
    send_message_to_mini_display("Building state object completed!")
    send_message_to_mini_display("Building Display...")
    ex = VendingMachineDisplay(appState)
    send_message_to_mini_display("Building Display completed!")
    send_message_to_mini_display("Start server...")
    server_thread = threading.Thread(target=start_server, args=(appState,))
    server_thread.start()
    send_message_to_mini_display("Start app (display)")
    sys.exit(app.exec_())