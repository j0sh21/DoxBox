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
        self.steps, self.brightness_steps = steps, brightness_steps
        self.brightness, self.prev_brightness = 255, 255
        self.fade_active, self.blink_active, self.breath_active = False, False, False  # Flag to control the loops
        self.blink_count, self.breath_count = 0, 0
        self.loop_type = "False"
        self.breath_speed = config.BREATH_SPEED
        self.breath_upper_brightness = 1.0  # 100%
        self.breath_lower_brightness = 0.0  # 0%
        self.blink_ontime = config.on_time
        self.blink_offtime = config.off_time

    def set_breath_speed(self, speed):
        self.breath_speed = float(speed)

    def set_blink_times(self, on_time, off_time):
        self.blink_ontime = float(on_time)
        self.blink_offtime = float(off_time)

    def set_breath_lights(self, lower_brightness, upper_brightness):
        self.breath_lower_brightness = float(lower_brightness)
        self.breath_upper_brightness = float(upper_brightness)

    def set_blink_count(self, blink):
        self.deactivate_loop()
        self.loop_type = "blink"
        self.blink_count = int(blink)
        self.activate_loop()

    def set_breath_count(self, breath):
        self.deactivate_loop()
        self.loop_type = "breath"
        self.breath_count = int(breath)
        self.activate_loop()

    def set_fade(self):
        self.deactivate_loop()
        self.loop_type = "fade"
        self.activate_loop()

    def activate_loop(self):
        if self.loop_type == "fade":
            self.fade_active = 1
            print("Activating fade...")
            fade_thread = threading.Thread(target=self.fade_led)
            fade_thread.start()
        elif self.loop_type == "blink":
            self.blink_active = 1
            print("Activating fade...")
            blink_thread = threading.Thread(target=self.blink_led)
            blink_thread.start()
            print("Activating blink...")
        elif self.loop_type == "breath":
            self.breath_active = 1
            print("Activating breath...")
            breath_thread = threading.Thread(target=self.breath_led)
            breath_thread.start()

    def deactivate_loop(self):
        if self.loop_type == "fade":
            print("Deactivating fade...")
            self.fade_active = False  # Deactivate fade
        elif self.loop_type == "blink":
            print("Deactivating blink...")
            self.blink_active = False  # Deactivate fade
        elif self.loop_type == "breath":
            print("Deactivating breath...")
            self.breath_active = False  # Deactivate fade
        else:
            print("No loop to stop")

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
            self.deactivate_loop()  # Pause the loop when a color is set directly
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

    def blink_led(self):
        original_r, original_g, original_b = self.r, self.g, self.b

        while self.blink_active == 1:
            # Turn off the LED
            self.r, self.g, self.b = 0, 0, 0
            self.update_leds()
            time.sleep(self.blink_offtime)  # LED is off for 'off_time' seconds

            # Restore the original LED state
            self.r, self.g, self.b = original_r, original_g, original_b
            self.update_leds()
            time.sleep(self.blink_ontime)  # LED is on for 'on_time' seconds

            if self.blink_count > 1:
                self.blink_count -= 1
            # If a specific number of blinks is set, break after completing them
            if self.blink_count == 1:
                self.blink_count -= 1
                # This part is reached when self.blink_active is no longer 1
                self.r, self.g, self.b = original_r, original_g, original_b
                self.update_leds()
                break

        # Ensure the LED is left in the original state, in case the loop exited early
        self.r, self.g, self.b = original_r, original_g, original_b
        self.update_leds()
        time.sleep(0.01)  # Small delay to prevent high CPU usage

    def breath_led(self):
        original_r, original_g, original_b = self.r, self.g, self.b
        while self.breath_active == 1:

            steps = config.BREATH_STEPS  # Number of steps in one breath cycle
            min_scale = self.breath_lower_brightness
            max_scale = self.breath_upper_brightness

            for step in range(steps):
                scale = (math.sin(step / steps * math.pi) * (max_scale - min_scale)) + min_scale
                scaled_red = int(original_r * scale)
                scaled_green = int(original_g * scale)
                scaled_blue = int(original_b * scale)
                self.set_lights(self.red_pin, scaled_red)
                self.set_lights(self.green_pin, scaled_green)
                self.set_lights(self.blue_pin, scaled_blue)
                time.sleep(self.breath_speed)

            if self.breath_count > 1:
                self.breath_count -= 1
            else:
                if self.breath_count == 1:
                    self.breath_count -= 1
                    self.r, self.g, self.b = original_r, original_g, original_b
                    self.update_leds()
                    time.sleep(0.01)
                    break  # Exit after one cycle if breath_count is set to 1

        # This part is reached when self.breath_active is no longer 1
        self.r, self.g, self.b = original_r, original_g, original_b
        self.update_leds()
        time.sleep(0.01)

    def fade_led(self):
        # fade until loop is broken
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


    def run(self):
        # Example initialization or setup code
        print("LED Controller is running...")
        self.set_color(226, 0, 116)  # Set to a default color (lnbits color)
        # Start the fade process in a separate thread to keep the main loop responsive
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
                    self.led_controller.set_fade()
                elif fade == 0:
                    self.led_controller.deactivate_loop()
                else:
                    print("Fading state must be 0 = off or 1 = on.")
            elif parts[0] == "blink" and len(parts) == 2:
                blink = int(parts[1])
                if blink >= 1:
                    self.led_controller.set_blink_count(blink)
                elif blink == 0:
                    self.led_controller.deactivate_loop()
                else:
                    print("blinking count must be one or more.")
            elif parts[0] == "blinkspeed" and len(parts) == 3:
                on, off = map(int, parts[1:])
                if on > 0 and off > 0:
                    self.led_controller.set_blink_times(on, off)
                else:
                    print("on and off time must both be bigger than 0 seconds.")
            elif parts[0] == "breath" and len(parts) == 2:
                breath = int(parts[1])
                if breath >= 1:
                    self.led_controller.set_breath_count(breath)
                elif breath == 0:
                    self.led_controller.deactivate_loop()
                else:
                    print("breath count must be one or more.")
            elif parts[0] == "breathspeed" and len(parts) == 2:
                speed = int(parts[1])
                if speed > 0:
                    self.led_controller.set_breath_speed(speed)
                else:
                    print("breath speed must be bigger than 0.")
            elif parts[0] == "breathbrightness" and len(parts) == 3:
                lower, upper = map(int, parts[1:])
                if lower+upper > 0 and lower < 1 and upper < 1 and lower < upper:
                    self.led_controller.set_breath_lights(lower, upper)
                else:
                    print("upper and / or lower brighntess must be >= 0 and <= 1.")

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

    try:
        while True:
            time.sleep(1)  # Main loop doing other tasks
    except KeyboardInterrupt:
        server.deactivate_loop()
        print("LED Controller application stopped.")

if __name__ == "__main__":
    main()
