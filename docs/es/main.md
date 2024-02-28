
# Documentación para main.py

## Visión general
Este módulo sirve como punto de entrada para DoxBox, orquestando el inicio y la gestión de varios componentes, incluyendo un servidor de aplicaciones, servidor LED y utilidades adicionales para depuración y control de dispositivos.

## Dependencias
- Python 3
- Módulo `subprocess` para ejecutar scripts.
- Módulo `threading` para ejecución concurrente.
- `pigpiod` para control de LEDs (instalado y ejecutado por separado).
- **Módulos del Proyecto**: `led.py`, `app.py`, `switch.py` (condicionalmente `./dev/process_mock.py` y `./dev/debug_client.py` para depuración)

## Componentes clave

### 1. Servidor de aplicaciones
- **Funcionalidad**: Gestiona la lógica principal de la aplicación.
- **Script**: `app.py`


### 2. Servidor LED
- **Funcionalidad**: Controla las operaciones de los LEDs.
- **Script**: `led.py`
- **Dependencias**: Requiere el daemon `pigpiod` para el control de los pines GPIO.


### 3. Herramientas de depuración
- **Funcionalidad**: Proporciona capacidades de depuración.
- **Scripts**: `debug_client.py` y `process_mock.py`
- **Modos**: Controlado por la variable `DEBUG` en `config.py`.


### 4. Control de dispositivos
- **Funcionalidad**: Gestiona operaciones específicas del dispositivo como pagos e impresión.
- **Script**: `switch.py`


## Configuración
Los ajustes de configuración, incluido el modo de depuración, se gestionan a través de `config.py`. Ajusta los ajustes en este archivo para controlar el comportamiento de la aplicación.


## Ejecutando la aplicación
1. Inicia la aplicación ejecutando `main.py`.
2. El script inicializa el servidor de aplicaciones y el servidor LED en hilos separados.
3. Dependiendo del modo de depuración establecido en `config.py`, se lanzan las herramientas de depuración o el script de control de dispositivos.


## Modo de depuración
- **Nivel 0**: Operación normal, se ejecuta `switch.py`.
- **Nivel 1**: Depuración básica, se ejecuta `debug_client.py`.
- **Nivel 2**: Depuración extendida, se ejecutan tanto `debug_client.py` como `process_mock.py`.


## Ampliando la aplicación
Para añadir nuevas funcionalidades:
1. Crea un nuevo script para el componente.
2. Define una función en `main.py` para ejecutar el script, similar a `run_app()` o `start_led()`.
3. Añade una llamada de hilo o subproceso en `main()` para ejecutar la nueva función.


## Solución de problemas
- Asegúrate de que `pigpiod` esté instalado y pueda ser iniciado por el script.
- Verifica que todos los scripts referenciados (`app.py`, `led.py`, `switch.py`, etc.) estén presentes en los directorios esperados.
- Revisa `config.py` para asegurarte de que los ajustes del modo de depuración sean correctos.


## Características

1. **Ejecución concurrente**: Utiliza hilos para ejecutar `app.py` y potencialmente un proceso simulado en paralelo.
2. **Depuración condicional**: Dependiendo del `DEBUG_MODE`, puede ejecutar procesos de depuración adicionales para ayudar en el desarrollo y las pruebas.
3. **Gestión de subprocesos**: Ejecuta componentes clave (`app.py`, `switch.py` o procesos de depuración) como subprocesos, asegurando entornos de ejecución aislados y controlados.


## Ejecutando el script

Para ejecutar la aplicación, corre el siguiente comando en la terminal:

```bash
python3 main.py
```
Asegúrate de que todas las dependencias estén correctamente instaladas y configuradas antes de ejecutar el script.
