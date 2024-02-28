
# Documentación para img_capture.py

## Descripción General

El script `img_capture.py` es un componente integral de la aplicación DoxBox diseñado para gestionar flujos de trabajo de captura de imágenes. Se comunica con cámaras digitales a través de la utilidad de línea de comandos gphoto2, realizando tareas como capturar imágenes, descargarlas en un directorio designado y gestionar las convenciones de nomenclatura de archivos. Además, incorpora comunicación en red para transmitir actualizaciones de estado o errores a otras partes de la aplicación.

## Dependencias

- **Utilidades Externas**: Requiere gphoto2 instalado en el sistema (`sudo apt-get install gphoto2`).
- **Librerías Estándar**: `socket`, `datetime`, `os`, `subprocess`, `signal`
- **Módulos del Proyecto**: `config`

## Funcionalidades Clave

### Interacción con la Cámara

- Utiliza comandos gphoto2 para la interacción directa con la cámara, permitiendo operaciones como disparar la captura de imágenes, descargar imágenes y limpiar la tarjeta de memoria de la cámara.

### Gestión de Procesos

- Incluye funcionalidad para terminar procesos específicos del sistema que pueden interferir con el acceso a la cámara, asegurando el control exclusivo sobre la cámara durante la operación.

### Gestión de Archivos y Directorios

- Maneja la creación de directorios de salida para almacenar imágenes capturadas, con manejo de errores para problemas comunes como directorios existentes o errores de permisos.
- Implementa lógica de cambio de nombre de archivos para organizar y gestionar imágenes capturadas basadas en convenciones de nomenclatura predefinidas.

### Comunicación en Red

- Cuenta con una función para enviar mensajes a otros componentes de la aplicación a través de sockets TCP, facilitando la comunicación entre procesos y la notificación de estados.

## Funciones Clave

### `send_message_to_app(message)`

Envía mensajes de estado o códigos de error a otro componente de la aplicación `app.py`, mejorando el manejo de errores y los mecanismos de retroalimentación al usuario.

### `kill_process()`

Busca y termina un proceso específico por nombre, típicamente utilizado para asegurar que la cámara no esté siendo accedida por otro proceso.

### `create_output_folder()`

Crea un directorio para almacenar imágenes capturadas, manejando de manera elegante errores comunes del sistema de archivos.

### `run_gphoto2_command(command)`

Ejecuta un comando gphoto2 especificado para la interacción con la cámara, envuelto en lógica de manejo de errores para capturar y comunicar cualquier problema encontrado durante la ejecución.

### `rename_pics()`

Renombra imágenes capturadas basadas en un conjunto de criterios, como la fecha y la hora, para facilitar la organización y gestión de archivos.

## Uso

El script está diseñado para ser ejecutado como parte de un flujo de trabajo de aplicación más amplio, típicamente invocado cuando se requiere funcionalidad de captura de imagen. Opera en una secuencia de pasos que preparan el sistema y la cámara, ejecutan la captura de imagen y gestionan los archivos resultantes.

### Flujo de Trabajo de Ejemplo

1. Terminación de Proceso: Asegurar que no haya procesos en conflicto accediendo a la cámara.
2. Preparación de Directorio: Crear o validar la existencia del directorio de salida para almacenar imágenes.
3. Captura de Imagen: Disparar la captura de imagen y manejar la interacción con la cámara.
4. Gestión de Archivos: Descargar imágenes al directorio de salida y renombrarlas según los requisitos de la aplicación. Eliminar todos los archivos de la cámara.

## Consideraciones

- Asegúrese de que gphoto2 esté instalado y configurado correctamente en el sistema donde se ejecuta la aplicación.
- El script debe tener los permisos adecuados para interactuar con la cámara, el sistema de archivos y los sockets de red.
- Asegúrese de que ningún otro proceso gphoto2 esté bloqueando la cámara para matar el proceso use los comandos:
```bash
ps -A | grep gphoto
```
- Matar procesos como `gvfs-gphoto2-vo`, etc.

## Instalando gphoto2

Para habilitar la funcionalidad de control de cámaras DSLR del proyecto, necesitas instalar gphoto2 en tu Raspberry Pi o cualquier sistema basado en Debian. gphoto2 es una utilidad de línea de comandos versátil que facilita la interfaz con una amplia gama de cámaras digitales.

**Así es como se instala gphoto2**:

1. **Actualizar tu sistema**: Primero, asegúrate de que tus listas de paquetes y los paquetes instalados estén actualizados.

   ```sh
   sudo apt-get update
   ```

2. **Instalar gphoto2**: Usa el siguiente comando para instalar el paquete gphoto2 y sus dependencias.
    ```sh
    sudo apt-get install gphoto2
    ```

Este comando descargará e instalará automáticamente gphoto2, haciéndolo disponible en tu sistema.

Con gphoto2 instalado con éxito, tu Raspberry Pi o sistema basado en Debian será capaz de comunicarse y controlar cámaras DSLR para funcionalidades de captura de imágenes.

Para obtener más información detallada sobre gphoto2 y sus extensas capacidades, puedes [visitar el sitio web oficial de gPhoto](http://www.gphoto.org/doc/remote/).
