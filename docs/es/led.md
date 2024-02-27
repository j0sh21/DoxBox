
# Documentación para led.py

¡Bienvenidos al módulo Controlador LED de DoxBox! Este documento está diseñado para ayudarte a entender e integrar los efectos de iluminación LED en tu cabina de fotos DoxBox, mejorando la experiencia del usuario durante el pago, la toma de fotos y otras interacciones.

## Primeros pasos

La clase `RGBLEDController` en este módulo controla los LED RGB para crear efectos visuales atractivos. Ya sea que estés agregando ambiente durante el proceso de toma de fotos o proporcionando señales visuales durante el pago, este módulo ofrece una variedad de animaciones como respiración, parpadeo y desvanecimiento.

### Prerrequisitos

Antes de comenzar, asegúrate de tener:

- Un Raspberry Pi configurado con LED RGB conectados a los pines GPIO especificados.
- Conocimientos básicos de programación en Python y configuración de pines GPIO.

## Componentes principales

### RGBLEDController

Este es el corazón del sistema de control LED. Gestiona los colores y animaciones de los LED conectados a tu Raspberry Pi.

#### Inicialización

```python
__init__(self, red_pin, green_pin, blue_pin, steps=config.fade_steps, brightness_steps=config.brightness_steps)
```

Inicializa el controlador con los pines GPIO conectados a tus LED RGB. `steps` y `brightness_steps` te permiten controlar la granularidad de las animaciones.

#### Configuración de Animaciones

- `set_fade_speed(self, speed)`: Ajusta la rapidez con la que los LED se desvanecen entre colores.
- `set_breath_speed(self, speed)`: Establece el ritmo del efecto de respiración, donde los LED se iluminan y atenúan gradualmente.
- `set_blink_times(self, on_time, off_time)`: Configura la duración de la animación de parpadeo para los LED encendidos y apagados.

#### Gestión de Animaciones

- `set_loop(self, animation_type)`: Elige el tipo de animación (por ejemplo, "respirar", "parpadear", "desvanecer").
- `activate_loop()`: Inicia el bucle de animación seleccionado. Precaución: Esta función ya se llama en set_loop()
- `interrupt_current_animation(self)`: Detiene cualquier animación en curso, útil para comentarios inmediatos del usuario.

#### Control Directo de LED

- `set_color(self, r, g, b)`: Establece directamente los LED al color RGB especificado.
- `update_leds(self)`: Actualiza los LED basándose en la configuración o animaciones actuales.

### ServerThread

Para configuraciones avanzadas, la clase `ServerThread` permite que el Controlador LED de DoxBox reciba comandos externos (por ejemplo, desde `app.py`) para cambiar los efectos LED de manera dinámica.

#### Configuración del Servidor

- `__init__(self, host, port, led_controller)`: Prepara el servidor con detalles de la red y lo vincula al RGBLEDController.
- `run(self)`: Lanza el servidor, haciendo que DoxBox responda a comandos de control LED externos.

## Manejo de Mensajes

**`led.py` toma acciones específicas si se envía un comando a través de un mensaje:**

| Comando                           | Acción                                                                              |
|-----------------------------------|-------------------------------------------------------------------------------------|
| "color 0 255 0"                   | establece el color a azul                                                           |
| "brightness 200"                  | establece el brillo a 200. Rango 0 - 255                                            |
| "fadespeed 0.8"                   | establece la velocidad de desvanecimiento a 0.8                                     |
| "fade 1"                          | inicia el desvanecimiento                                                           |
| "blinkspeed 0.5 0.5"              | Configura el tiempo de encendido y apagado en segundos para el efecto de parpadeo   |
| "blink 1"                         | inicia el parpadeo un número ilimitado de veces                                     |
| "blink 10"                        | inicia el parpadeo 10 veces                                                         |
| "breathbrightness 0.2 0.8"        | Configura el rango de brillo para el efecto de respiración del 20% al 80% de brillo |
| "breathspeed 0.5"                 | Establece la velocidad de respiración a 0.5                                         |
| "breath 1"                        | inicia la respiración un número ilimitado de veces                                  |
| "breath 5"                        | inicia la respiración 5 veces                                                       |
| "interrupt"                       | interrumpe el bucle de animación actual                                             |
| "fade 0", "breath 0" o "blink 0"  | detiene el bucle de animación dado                                                  |

## Ejemplo de Integración

Aquí tienes un ejemplo simple para integrar efectos LED en tu DoxBox:

```python
from led_controller import RGBLEDController, ServerThread

# Inicializa el controlador LED con pines GPIO
led_controller = RGBLEDController(red_pin=17, green_pin=27, blue_pin=22)

# Opcionalmente, inicia un servidor para comandos externos
server = ServerThread(host='0.0.0.0', port=12345, led_controller=led_controller)
server.run()

# Configura un efecto de respiración para el proceso de toma de fotos
led_controller.set_loop('breath')
led_controller.activate_loop()
```

## Consejos para una Excelente Experiencia de Usuario

- Usa efectos de respiración suaves y lentos para tiempos de inactividad y crear un ambiente acogedor.
- Parpadeos brillantes y rápidos pueden señalar el inicio de la secuencia de toma de fotos o un pago exitoso.
- Considera temas de color que coincidan con tu marca DoxBox o el tema del evento.

## Solución de Problemas

- LEDs no responden: Verifica tus conexiones GPIO y asegúrate de que tu Raspberry Pi tenga la configuración de pines correcta.
- Las animaciones no cambian: Asegúrate de llamar a `interrupt_current_animation` antes de cambiar de animaciones.
