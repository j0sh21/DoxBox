# Documentation for led.py

Welcome to the DoxBox LED Controller module! This document is designed to help you understand and integrate the LED lighting effects into your DoxBox photo booth, enhancing the user experience during payment, photo-taking, and other interactions.

## Getting Started

The `RGBLEDController` class in this module controls RGB LEDs to create engaging visual effects. Whether you're adding ambiance during the photo-taking process or providing visual cues during payment, this module offers a variety of animations like breathing, blinking, and fading.

### Prerequisites

Before diving in, ensure you have:

- A Raspberry Pi setup with RGB LEDs connected to the specified GPIO pins.
- Basic knowledge of Python programming and GPIO pin configuration.

## Core Components

### RGBLEDController

This is the heart of the LED control system. It manages the colors and animations of the LEDs connected to your Raspberry Pi.

#### Initialization

```python
__init__(self, red_pin, green_pin, blue_pin, steps=config.fade_steps, brightness_steps=config.brightness_steps)
```

Initializes the controller with the GPIO pins connected to your RGB LEDs. `steps` and `brightness_steps` allow you to control the granularity of the animations.

#### Configuring Animations


- `set_fade_speed(self, speed)`: Adjusts how quickly the LEDs fade between colors.
- `set_breath_speed(self, speed)`: Sets the pace of the breathing effect, where LEDs gradually brighten and dim.
- `set_blink_times(self, on_time, off_time)`: Configures the blink animation's duration for LEDs being on and off.


#### Managing Animations

- `set_loop(self, animation_type)`: Chooses the type of animation (e.g., "breath", "blink", "fade").
- `activate_loop()`: Starts the selected animation loop. Caution: This function is already called in set_loop()
- `interrupt_current_animation(self)`: Stops any ongoing animation, useful for immediate user feedback.

#### Direct LED Control

- `set_color(self, r, g, b)`: Directly sets the LEDs to the specified RGB color.
- `update_leds(self)`: Refreshes the LEDs based on current settings or animations.


### ServerThread

For advanced setups, the `ServerThread` class allows the DoxBox LED Controller to receive external commands (e.g., from `app.py`) to change LED effects dynamically.

#### Setting Up the Server

- `__init__(self, host, port, led_controller)`: Prepares the server with network details and binds it to the RGBLEDController.
- `run(self)`: Launches the server, making the DoxBox responsive to external LED control commands.
## Message Handling


**`led.py` takes specific actions if a command is sent via message:**

| Command                           | Action                                                                              |
|-----------------------------------|-------------------------------------------------------------------------------------|
| "color 0 255 0"                   | sets color to blue                                                                  |
| "brightness 200"                  | sets brightness to 200. Range 0 - 255                                               |
| "fadespeed 0.8"                   | set fade speed to 0.8                                                               |
| "fade 1"                          | start fade                                                                          |
| "blinkspeed 0.5 0.5"              | Setting on and off time in seconds for blink effect                                 |
| "blink 1"                         | start blinkt unlimited times                                                        |
| "blink 10"                        | start blink 10 times                                                                |
| "breathbrightness 0.2 0.8"        | Setting the brightness range for the breath effect to 20% to 80% brightness         |
| "breathspeed 0.5"                 | Setting the breathspeed to 0.5|
| "fade 0", "breath 0" or "blink 0" | stop the given animation loop                                                       |
| "breath 1"                        | start breath unlimited                                                              |
| "breath 5"                        | start breath 5 times                                                                |
| "interrupt"                       | interrupt current animation loop                                                    |
| "fade 0", "breath 0" or "blink 0" | stop the given animation loop                                                       |

## Integration Example

Here's a simple example to integrate LED effects into your DoxBox:

```python
from led_controller import RGBLEDController, ServerThread

# Initialize the LED controller with GPIO pins
led_controller = RGBLEDController(red_pin=17, green_pin=27, blue_pin=22)

# Optionally, start a server for external commands
server = ServerThread(host='0.0.0.0', port=12345, led_controller=led_controller)
server.run()

# Set up a breathing effect for the photo-taking process
led_controller.set_loop('breath')
led_controller.activate_loop()
```

## Tips for a Great User Experience

- Use soft, slow breathing effects for idle times to create a welcoming ambiance.
- Bright, fast blinks can signal the start of the photo-taking sequence or successful payment.
- Consider color themes that match your DoxBox branding or the event theme.

## Troubleshooting

- LEDs not responding: Check your GPIO connections and ensure your Raspberry Pi has the correct pin configuration.
- Animations not changing: Ensure `interrupt_current_animation` is called before switching animations.