
# Documentación para switch.py

## Visión general

El módulo `switch.py` es un componente crítico de la aplicación DoxBox, responsable de monitorear los datos externos de `LNbitsAPI`, detectar cambios significativos y comunicarse con otras partes de DoxBox, por ejemplo, `app.py` para activar acciones específicas (por ejemplo, Tomar foto) basadas en estos cambios. Utiliza solicitudes de red, hilos y programación de sockets para lograr sus objetivos.

## Dependencias

- **Bibliotecas estándar**: requests, time, threading, socket
- **Módulos del proyecto**: config

## Configuración

El módulo se basa en varias configuraciones definidas en el módulo `config`, incluyendo:

- `API_URL`: La URL de la API externa a monitorear.
- `API_KEY`: La clave requerida para la autenticación de la API.
- `HOST, PORT`: Configuraciones de red para la comunicación por socket.
- `AMOUNT_THRESHOLD`: Un valor umbral específico que activa una acción cuando se alcanza.
- `CHECK_INTERVAL`, `POST_PAYMENT_DELAY`: Intervalos de tiempo para el ritmo operacional.

## Funciones clave

### `send_message_to_app(message)`

Envía un mensaje a otro componente de la aplicación `app.py` utilizando programación de sockets. Esta función encapsula la lógica de comunicación de red, incluido el manejo de errores.

### `main_loop()`

La función principal que se ejecuta en un bucle continuo, realizando las siguientes acciones:

1. Obtiene datos de una API externa utilizando la biblioteca `requests`.
2. Monitorea los cambios en los datos, específicamente buscando cambios en un valor de `payment_hash`.
3. Cuando se detecta un cambio y se cumplen ciertas condiciones (por ejemplo, un umbral de cantidad), activa una acción enviando un mensaje a otro componente.
4. Incorpora mecanismos de retraso para gestionar la frecuencia de las solicitudes de la API y las acciones subsiguientes.

## Flujo de ejecución

1. Inicializa y comienza el bucle principal en un hilo separado para asegurar la ejecución no bloqueante.
2. Monitorea continuamente una API externa en busca de cambios, utilizando un valor hash como indicador.
3. Se comunica con otros componentes de la aplicación a través de sockets para coordinar acciones basadas en los cambios detectados.

## Ejecutando el Módulo

Para ejecutar `switch.py`, ejecute el siguiente comando en una terminal:

```bash
python3 switch.py
```
