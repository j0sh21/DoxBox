import threading
from threading import Thread
import socket
import pigpio
import time
import config
import math

class RGBLEDController:
    def __init__(self, red_pin, green_pin, blue_pin, steps=config.fade_steps, brightness_steps=config.brightness_steps):
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


    def blink_led(self, blink_count=5, on_time = config.on_time, off_time = config.off_time):
        # Save the current LED state
        original_r, original_g, original_b = self.r, self.g, self.b

        for _ in range(blink_count):
            # Turn off the LED
            self.r, self.g, self.b = 0, 0, 0
            self.update_leds()
            time.sleep(off_time)  # LED is off for 'off_time' seconds

            # Restore the original LED state
            self.r, self.g, self.b = original_r, original_g, original_b
            self.update_leds()
            time.sleep(on_time)  # LED is on for 'on_time' seconds

        # Ensure the LED is left in the original state
        self.r, self.g, self.b = original_r, original_g, original_b
        self.update_leds()

    def breath_led(self, breath_count=5):
        original_r, original_g, original_b = self.r, self.g, self.b
        steps = config.BREATH_STEPS  # Number of steps in one breath cycle
        for cycle in range(breath_count):
            for step in range(steps):
                # Calculate scaling factor using a sinusoidal pattern for smooth transition
                scale = (math.sin(step / steps * math.pi))

                # Apply the scaling factor to each color component
                scaled_red = int(self.r * scale)
                scaled_green = int(self.g * scale)
                scaled_blue = int(self.b * scale)

                # Update LED colors with the scaled values
                self.set_lights(self.red_pin, scaled_red)
                self.set_lights(self.green_pin, scaled_green)
                self.set_lights(self.blue_pin, scaled_blue)

                time.sleep(config.BREATH_SPEED)  # Adjust for desired speed of the breathing effect
                # Ensure the LED is left in the original state
        self.r, self.g, self.b = original_r, original_g, original_b
        self.update_leds()
    
    def fade_led(self):
        while self.fade_active == 1:  # Check if fade loop should be active
            max_color = max(self.r, self.g, self.b)
            min_color = min(self.r, self.g, self.b)

            # Adjust colors to smoothly transition between states
            if self.r == max_color and self.g < max_color and self.b == min_color:
                self.g = min(self.g + self.steps, 255)  # Red to yellow
            elif self.g == max_color and self.r > min_color:
                self.r = max(self.r - self.steps, 0)  # Yellow to green
            elif self.g == max_color and self.b < max_color and self.r == min_color:
                self.b = min(self.b + self.steps, 255)  # Green to cyan
            elif self.b == max_color and self.g > min_color:
                self.g = max(self.g - self.steps, 0)  # Cyan to blue
            elif self.b == max_color and self.r < max_color and self.g == min_color:
                self.r = min(self.r + self.steps, 255)  # Blue to magenta
            elif self.r == max_color and self.b > min_color:
                self.b = max(self.b - self.steps, 0)  # Magenta to red

            # Update the LEDs based on the current colors
            self.update_leds()
            # Debugging: print(f"Set color to {self.r}, {self.g}, {self.b}")
            time.sleep(0.01)  # Small delay to prevent high CPU usage

    def start_fade_thread(self):
        fade_thread = threading.Thread(target=self.fade_led)
        fade_thread.start()

    def run(self):
        # Example initialization or setup code
        print("LED Controller is running...")
        self.set_color(103, 58, 183)  # Set to a default color (lnbits color)

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
                    print("Start fading LED")
                    self.led_controller.activate_fade()
                elif fade == 0:
                    self.led_controller.deactivate_fade()
                    print("End fading LED")
                else:
                    print("Fading state must be 0 = off or 1 = on.")
            elif parts[0] == "blink" and len(parts) == 2:
                blink = int(parts[1])
                if blink >= 1:
                    print("Start blinking LED")
                    self.led_controller.blink_led(blink_count=blink)
                else:
                    print("blinking count must be one or more.")
            elif parts[0] == "breath" and len(parts) == 2:
                breath = int(parts[1])
                if breath >= 1:
                    print("Start breathing LED")
                    self.led_controller.breath_led(breath_count=breath)
                else:
                    print("breath count must be one or more.")
            else:
                print(f"Unrecognized command: {command}")
        except ValueError as e:
            print(f"Error processing command '{command}': {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

def main():
    controller = RGBLEDController(config.red_pin, config.green_pin, config.blue_pin)
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
