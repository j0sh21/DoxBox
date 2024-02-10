import threading
from threading import Thread
import socket
import pigpio
import time


class RGBLEDController:
    def __init__(self, red_pin, green_pin, blue_pin, steps=1, brightness_steps=25):
        self.red_pin, self.green_pin, self.blue_pin = red_pin, green_pin, blue_pin
        self.r, self.g, self.b = 255.0, 0, 0
        self.pi = pigpio.pi()
        self.steps = steps
        self.brightness_steps = brightness_steps
        self.brightness, self.prev_brightness = 255, 255
        self.fade_active = 1  # Flag to control the fade loop

    def get_color(self):
        return self.r, self.g, self.b
    def activate_fade(self):
        print("Activating fade...")
        self.fade_active = 1  # Activate fade
        self.start_fade_thread()

    def deactivate_fade(self):
        print("Deactivating fade...")
        self.fade_active = 0  # Deactivate fade

    def set_lights(self, pin, brightness):
        real_brightness = int(brightness * (self.brightness / 255.0))
        self.pi.set_PWM_dutycycle(pin, real_brightness)

    def update_brightness(self, r, g, b):
        r = int(r * (self.brightness / 255.0))
        g = int(g * (self.brightness / 255.0))
        b = int(b * (self.brightness / 255.0))
        return r, g, b

    def set_color(self, r, g, b):
        if r or g or b:
            self.fade_active = False  # Pause the fade loop when a color is set directly
            self.r, self.g, self.b = self.update_brightness(r, g, b)
            self.set_lights(self.red_pin, self.r)
            self.set_lights(self.green_pin, self.g)
            self.set_lights(self.blue_pin, self.b)
        else:
            r, g, b = self.update_brightness(self.r, self.g, self.b)
            self.set_lights(self.red_pin, r)
            self.set_lights(self.green_pin, g)
            self.set_lights(self.blue_pin, b)

    def update_leds(self):
        r, g, b = self.update_brightness(self.r, self.g, self.b)
        # Update the LED colors based on the current state
        self.set_lights(self.red_pin, r)
        self.set_lights(self.green_pin, g)
        self.set_lights(self.blue_pin, b)

    def update_color(self, color, step):
        color += step
        if color > 255:
            return 255
        if color < 0:
            return 0
        return color

    def fade_led(self):
        while self.fade_active == 1:  # Check if fade loop should be active
            # Fade the LED colors
            # Fade logic
            if self.r == 255 and self.b == 0 and self.g < 255:
                self.g = self.update_color(self.g, self.steps)
            elif self.g == 255 and self.b == 0 and self.r > 0:
                self.r = self.update_color(self.r, -self.steps)
            elif self.r == 0 and self.g == 255 and self.b < 255:
                self.b = self.update_color(self.b, self.steps)
            elif self.r == 0 and self.b == 255 and self.g > 0:
                self.g = self.update_color(self.g, -self.steps)
            elif self.g == 0 and self.b == 255 and self.r < 255:
                self.r = self.update_color(self.r, self.steps)
            elif self.r == 255 and self.g == 0 and self.b > 0:
                self.b = self.update_color(self.b, -self.steps)
            # Update the LEDs based on the current colors
            self.update_leds()
            #print(f"Set color to {self.r}, {self.g}, {self.b}")
            time.sleep(0.01)  # Small delay to prevent high CPU usage

    def start_fade_thread(self):
        fade_thread = threading.Thread(target=self.fade_led)
        fade_thread.start()

    def run(self):
        # Example initialization or setup code
        print("LED Controller is running...")
        self.set_color(255, 255, 255)  # Set to a default color (white) or your choice

        # Start the fade process in a separate thread to keep the main loop responsive
        fade_thread = threading.Thread(target=self.fade_led)
        fade_thread.start()
        time.sleep(1)  # Sleep to prevent high CPU usage


class ServerThread(Thread):
    def __init__(self, host, port, led_controller):
        super().__init__()

        self.host = host
        self.port = port
        self.led_controller = led_controller
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

    def run(self):
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Connection from {address} has been established.")
            self.handle_client(client_socket)

    def handle_client(self, client_socket):
        with client_socket:
            while True:
                msg = client_socket.recv(1024).decode('utf-8')
                if not msg:
                    break
                print(f"Received: {msg}")
                self.parse_command(msg)

    def parse_command(self, command):
        try:
            parts = command.strip().lower().split()
            if parts[0] == "color" and len(parts) == 4:
                r, g, b = map(int, parts[1:])
                if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                    self.led_controller.set_color(r, g, b)
                    print(f"Set color to {r}, {g}, {b}")
                else:
                    print("Color values must be between 0 and 255.")
            elif parts[0] == "brightness" and len(parts) == 2:
                brightness = int(parts[1])
                if 0 <= brightness <= 255:
                    self.led_controller.brightness = brightness
                    self.led_controller.set_color(False, False, False)
                    print(f"Set brightness to {brightness}")
                else:
                    print("Brightness value must be between 0 and 255.")
            elif parts[0] == "fade" and len(parts) == 2:
                fade = int(parts[1])
                if fade == 1:
                    r, g, b = self.led_controller.get_color()
                    self.led_controller.set_color(r, g, b)
                    self.led_controller.activate_fade()
                    print("Start fading LED")
                elif fade == 0:
                    self.led_controller.deactivate_fade()
                    print("End fading LED")
                else:
                    print("Fading state must be 0 = off or 1 = on.")
            else:
                print(f"Unrecognized command: {command}")
        except ValueError as e:
            print(f"Error processing command '{command}': {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

def main():
    controller = RGBLEDController(red_pin=17, green_pin=22, blue_pin=24)
    server = ServerThread(host='0.0.0.0', port=12345, led_controller=controller)

    server.start()
    controller.run()
    server.led_controller.activate_fade()

    try:
        while True:
            time.sleep(1)  # Main loop doing other tasks
    except KeyboardInterrupt:
        server.deactivate_fade()
        print("LED Controller application stopped.")

if __name__ == "__main__":
    main()
