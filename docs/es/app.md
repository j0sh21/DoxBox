
# Documentación de app.py
## Visión general

`app.py` sirve como un módulo pivotal en la aplicación, orquestando la interfaz de usuario y facilitando las interacciones del usuario. Este módulo aprovecha el poderoso marco de trabajo PyQt5 para construir una interfaz gráfica de usuario (GUI) robusta y receptiva, convirtiéndolo en una pieza central para aplicaciones que requieren interacción del usuario a través de una interfaz visual.

## Propósito

El propósito principal de `app.py` es definir la estructura y el comportamiento de la GUI de la aplicación. Encapsula el diseño y la funcionalidad de varios componentes de la UI, incluyendo ventanas, widgets, layouts y manejadores de eventos, asegurando una experiencia de usuario fluida e intuitiva.

## Alcance

Dentro de `app.py`, encontrarás definiciones para clases y funciones clave que colectivamente construyen la interfaz frontal de la aplicación. Esto incluye:

- **AppState**: Una clase diseñada para gestionar el estado de la aplicación, permitiendo actualizaciones dinámicas e interacciones dentro de la GUI. Utiliza una señal `stateChanged` para notificar a otras partes de la aplicación cuando el estado cambia, promoviendo un diseño reactivo donde la UI puede ajustarse basada en el estado actual de la aplicación.
- **VendingMachineDisplay**: Una subclase personalizada de `QWidget` que actúa como el contenedor principal para los elementos de la UI de la aplicación, organizándolos en un layout coherente y funcional.

## Manejo del Estado

La clase `AppState` es central para la gestión del estado de la aplicación. Mantiene una variable `state` que refleja la condición o modo actual de la aplicación. Los cambios en este estado se propagan a través de la señal `stateChanged`, permitiendo que otros componentes, especialmente la UI, reaccionen y se actualicen en consecuencia. Este enfoque desacopla la gestión del estado de la lógica de la UI, mejorando la modularidad y mantenibilidad.

## Programación de Sockets y Comunicación Servidor-Cliente

La aplicación cuenta con un componente servidor que escucha conexiones entrantes utilizando la biblioteca `socket` de Python. La función `start_server` inicializa este servidor, que espera mensajes de los clientes. Al recibir un mensaje, la función `handle_client_connection` lo procesa y actualiza el `AppState`, aprovechando el sistema de gestión del estado para reflejar los cambios en la UI de manera dinámica. Esta configuración de servidor-cliente permite un control remoto o automatizado sobre la aplicación, ideal para escenarios de tipo quiosco o máquina expendedora.

## Características Clave

- **Diseño Modular**: `app.py` sigue un enfoque modular, separando las preocupaciones entre la gestión del estado y la presentación de la UI, lo que facilita el mantenimiento y la escalabilidad.
- **UI Basada en Estado**: La UI de la aplicación responde dinámicamente a los cambios en el estado de la aplicación, proporcionando una experiencia de usuario reactiva que se actualiza en tiempo real para reflejar el contexto y los datos actuales.
- **Integración con PyQt5**: Al utilizar PyQt5, `app.py` aprovecha un conjunto completo de herramientas y widgets para crear GUIs de grado profesional, incluyendo soporte para componentes multimedia, manejo de eventos y personalización de widgets.

## Dependencias

- **Qt Widgets**: Hereda de `QWidget` y puede usar otros widgets como `QLabel`, `QVBoxLayout`, `QHBoxLayout` de PyQt5.QtWidgets.
- **Qt Multimedia**: Potencialmente usa `QCamera`, `QCameraViewfinder` de PyQt5.QtMultimedia y `QCameraViewfinder` de PyQt5.QtMultimediaWidgets para integración con cámaras.
- **Qt Core**: Utiliza clases como `QPixmap`, `QMovie` de PyQt5.QtGui, y `Qt`, `QSize`, `QRect`, `QPoint` de PyQt5.QtCore para funcionalidades básicas de la GUI.

## Manejo de Multimedia y Animaciones GIF

La clase `VendingMachineDisplay` incorpora capacidades avanzadas de manejo de multimedia, notablemente para reproducir y gestionar animaciones GIF.

### Reproduciendo Animaciones GIF

La aplicación puede mostrar animaciones GIF como parte de su UI, proporcionando contenido visual dinámico. Esto se logra a través de la clase `QMovie` de PyQt5, que se utiliza para cargar y reproducir archivos GIF. La clase `VendingMachineDisplay` incluye métodos para comenzar a reproducir un GIF, calcular su duración y asegurar que se ajuste dentro de los elementos de la UI designados, ofreciendo una experiencia multimedia sin fisuras.

### Métodos Clave

- **send_msg_to_LED(host, port, command)**: Este método permite que la aplicación se comunique con dispositivos externos, como una tira de LED adjunta, a través de una red. Establece una conexión de socket al host y puerto especificados, luego envía un comando, que podría usarse para mostrar mensajes o controlar la tira de LED.

- **calculateDuration()**: Calcula la duración total de una animación GIF iterando a través de sus fotogramas. Esta información se puede usar para sincronizar la reproducción del GIF con otros eventos en la aplicación, asegurando una experiencia de usuario coherente.

- **handle_client_connection(client_socket, appState)**: Maneja las conexiones entrantes de los clientes. Esta función es una parte crítica de la arquitectura servidor-cliente, leyendo mensajes enviados por los clientes, actualizando el estado de la aplicación basado en estos mensajes y asegurando que la UI refleje estos cambios.

- **start_server(appState)**: Inicializa y comienza el servidor que escucha conexiones entrantes. Se enlaza a un puerto especificado y espera a que los clientes se conecten, creando un nuevo hilo para manejar cada conexión, permitiendo así que la aplicación continúe operando sin problemas mientras gestiona las solicitudes de los clientes.


### Lógica de Repetición de GIF

La lógica de repetición de GIF en DoxBox está diseñada para gestionar la reproducción de animaciones GIF basada en el estado actual de la aplicación y la duración de los GIFs. Esta lógica asegura que los GIFs más cortos se repitan un número especificado de veces para mantener el compromiso del usuario, mientras que los GIFs más largos transicionan suavemente al siguiente estado o GIF cuando se completan. A continuación, se ofrece un resumen de los componentes clave y las funcionalidades de la lógica de repetición de GIF.


#### Componentes:

- Objeto de Película: Representa la animación GIF que se va a reproducir. Es responsable de gestionar la reproducción del GIF.
- Etiqueta GIF: Un componente gráfico de la UI (etiqueta) que muestra la animación GIF.
- Gestión del Estado: La aplicación mantiene un estado que determina el contexto o la fase en la que se encuentra actualmente (por ejemplo, pago, cuenta regresiva, sonrisa).

#### Atributos Clave:

- `loopCount`: Rastrea el número de veces que se ha repetido el GIF actual.
- `desiredLoops`: El número deseado de veces que el GIF debe repetirse, que varía según la duración del GIF.
- `isreplay`: Una bandera que indica si la reproducción actual del GIF es una reproducción original (0) o una repetición (1).
- `total_duration`: La duración total del GIF actual. Se utiliza para determinar el número de bucles deseados para GIFs más cortos.
- `gif_path`: La ruta del archivo del GIF actual que se va a reproducir.

#### Funciones:

- `playGIF()`: Inicia la reproducción de un GIF. Si `isreplay` es 0, restablece `loopCount` y `desiredLoops` para un nuevo GIF. Si `isreplay` es 1, repite el GIF actual sin restablecer el contador de bucles.
- `updateGIF(state)`: Actualiza el GIF actual basado en el estado de la aplicación. Selecciona un GIF aleatorio de una subcarpeta especificada correspondiente al estado actual y lo prepara para la reproducción.
- `onGIFFinished()`: Se activa cuando un GIF termina de reproducirse. Gestiona la lógica para repetir o transicionar los GIFs basado en su duración y el estado de la aplicación.

#### Duración del GIF y Tiempos de Repetición:

- Duración < 0.6 segundos: Para GIFs más cortos que 0.6 segundos, el número deseado de repeticiones (`desiredLoops`) se establece en 6 veces. Esto asegura que los GIFs muy cortos se reproduzcan suficientes veces para ser notables y atractivos para el usuario.
- Duración entre 0.6 y 1.6 segundos: Para GIFs con una duración entre 0.6 segundos y 1.6 segundos, el GIF se repite 3 veces. Este rango de duración cubre GIFs moderadamente cortos que requieren menos repeticiones para mantener el compromiso del usuario.
- Duración entre 1.6 y 3.3 segundos: Los GIFs que caen dentro de este rango de duración se repiten 2 veces. Estos se consideran cortos pero no tan breves que requieran muchas repeticiones para ser efectivos.


## Mensajes Manejados por app.py

La aplicación utiliza cadenas numéricas como mensajes para representar diferentes estados y acciones dentro de la aplicación. Cada mensaje desencadena comportamientos específicos, correlacionando con diversas funcionalidades o retroalimentación visual a través de la GUI. A continuación, se muestra una tabla que resume los mensajes numéricos y sus efectos correspondientes dentro de la aplicación:

**Mensajes de Estado**:

| Mensaje | Descripción                                                                 |
|---------|-----------------------------------------------------------------------------|
| "0"     | representa un estado inicial o de bienvenida.                               |
| "1"     | indica un pago o transacción completada.                                    |
| "2"     | Iniciar la cuenta regresiva, fase de preparación después de un pago.        |
| "3"     | significa la finalización de una cuenta regresiva, avanzando hacia la captura de la foto. |
| "4"     | Foto capturada con éxito, comenzar a imprimir ahora.                        |
| "5"     | Impresión finalizada: "Gracias" o estado de finalización, el fin de una transacción. |
| "144"   | Insuficiente pago                                                          |
| "204"   | Imagen eliminada con éxito después de imprimir.                            |


**Mensajes de Error**:

| Mensaje | Descripción                                      |
|---------|--------------------------------------------------|
| "100"   | Error general en app.py.                         |
| "101"   | La cámara no encontró enfoque                    |
| "102"   | no se encontró la cámara                         |
| "103"   | archivo no encontrado                            |
| "104"   | permiso denegado                                 |
| "110"   | error general en print.py                        |
| "112"   | impresora no encontrada                          |
| "113"   | archivo no encontrado                            |
| "114"   | permiso denegado                                 |
| "115"   | error al copiar archivo                          |
| "116"   | Trabajo de impresión detenido o cancelado.       |
| "119"   | error al crear trabajo de impresión              |
| "120"   | error general en img_capture.py                  |
| "130"   | error general en led.py                          |
| "140"   | Error inesperado en switch.py                    |
| "141"   | El código de estado de respuesta de la API de LNbits no es 200 |
| "142"   | Error de conexión con la API de LNbits           |
| "143"   | Error de conexión inicial con la API de LNbits   |


Estos mensajes son procesados por la aplicación para actualizar el `AppState` y, por extensión, la UI y cualquier pantalla externa conectada a la aplicación. Las acciones específicas tomadas en respuesta a cada mensaje pueden variar dependiendo del contexto de la aplicación actual y el flujo de trabajo previsto.

## Uso

Los desarrolladores que trabajan con `app.py` pueden esperar interactuar con abstracciones de alto nivel para componentes de la UI, mecanismos sencillos para la gestión del estado y patrones de programación basados en eventos. Este módulo se invoca típicamente como parte del proceso de inicio de la aplicación, inicializando la GUI y vinculándola a la lógica subyacente y los modelos de datos.

# Documentación de la Clase AppState

## Visión general

La clase `AppState`, definida dentro de `app.py`, es un componente fundamental diseñado para gestionar el estado de la aplicación y habilitar la comunicación entre componentes en una aplicación GUI basada en Qt. Hereda de `QObject` para utilizar el mecanismo de señales y slots de Qt, lo que la hace adecuada para aplicaciones que requieren respuestas dinámicas a cambios de estado.

## Características

- **Gestión del Estado**: Centraliza la gestión del estado de la aplicación, proporcionando una única fuente de verdad para la lógica relacionada con el estado.
- **Emisión de Señales**: Emplea el mecanismo de señales de Qt (`pyqtSignal`) para emitir eventos cuando el estado de la aplicación cambia, permitiendo que otros componentes reaccionen a estos cambios de manera desacoplada.

## Definición de la Clase

### Propiedades

- `state`: Una propiedad que encapsula el estado actual de la aplicación. El acceso a esta propiedad se controla a través de un getter y un setter para asegurar que los cambios de estado se gestionen de manera consistente.

### Señales

- `stateChanged(str)`: Una señal emitida cada vez que el estado cambia, llevando el nuevo valor del estado como una cadena. Esta señal puede conectarse a slots o funciones dentro de otros componentes, permitiéndoles responder a cambios de estado.

## Uso

La clase `AppState` se instancia típicamente una vez y se utiliza en toda la aplicación para gestionar y observar el estado de la aplicación. Los componentes que necesitan responder a cambios de estado pueden conectar sus slots o funciones a la señal `stateChanged`.

### Ejemplo

```python
# Instanciación
app_state = AppState()

# Conectar una función a la señal stateChanged
def on_state_changed(new_state):
    print(f"El estado de la aplicación cambió a: {new_state}")

app_state.stateChanged.connect(on_state_changed)

# Actualizar el estado
app_state.state = "1"  # Esto emitirá la señal stateChanged e invocará on_state_changed
```

# Documentación de la Clase VendingMachineDisplay

## Visión general

La clase `VendingMachineDisplay`, definida dentro de `app.py`, es un componente crucial de la interfaz gráfica de usuario (GUI) de la aplicación. Hereda de `QWidget`, convirtiéndola en un contenedor versátil para varios elementos de la UI. Esta clase es responsable principalmente de construir y gestionar el layout, controles y otros elementos visuales que constituyen la interfaz de usuario de la aplicación.

## Dependencias

- **Qt Widgets**: Hereda de `QWidget` y puede usar otros widgets como `QLabel`, `QVBoxLayout`, `QHBoxLayout` de `PyQt5.QtWidgets`.
- **Qt Multimedia**: Potencialmente usa `QCamera`, `QCameraViewfinder` de `PyQt5.QtMultimedia` y `QCameraViewfinder` de `PyQt5.QtMultimediaWidgets` para integración con cámaras.
- **Qt Core**: Utiliza clases como `QPixmap`, `QMovie` de `PyQt5.QtGui`, y `Qt`, `QSize`, `QRect`, `QPoint` de `PyQt5.QtCore` para funcionalidades básicas de la GUI.

## Características

- **Gestión del Layout**: Gestiona la disposición de elementos de la UI usando layouts (por ejemplo, `QVBoxLayout`, `QHBoxLayout`), asegurando una presentación organizada y receptiva.
- **Integración con el Estado**: Se integra con la clase `AppState` para reflejar y potencialmente modificar el estado de la aplicación basado en interacciones del usuario u otros eventos.
- **Soporte Multimedia**: Si se utiliza la funcionalidad de cámara, puede incluir características como la visualización de la transmisión en vivo de la cámara, utilizando `QCamera` y `QCameraViewfinder`.

## Definición de la Clase

### Constructor

- `__init__(self, appState)`: Inicializa una nueva instancia de la clase `VendingMachineDisplay`, tomando un objeto `AppState` como argumento para facilitar la gestión del estado y la interacción.

### Métodos Clave

- La clase incluye métodos para inicializar componentes de la UI, configurar layouts y conectar señales a slots para el manejo de eventos (por ejemplo, clics de botones, cambios de estado).

## Uso

La clase `VendingMachineDisplay` se instancia como parte del proceso de configuración de la GUI de la aplicación, a menudo en el script principal o un módulo dedicado a la GUI. Requiere una instancia de `AppState` para permitir actualizaciones e interacciones de la UI basadas en el estado.

### Ejemplo

```python
app = QApplication(sys.argv)
app_state = AppState()
vending_machine_display = VendingMachineDisplay(app_state)
vending_machine_display.show()
sys.exit(app.exec_())
```
