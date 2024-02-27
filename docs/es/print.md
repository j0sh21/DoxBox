
# Documentación para print.py

## Descripción General

El `DoxBoxPrintManager` (`print.py`) es un componente esencial del sistema DoxBox, diseñado para manejar de manera fluida la impresión de imágenes inmediatamente después de ser capturadas. Este script de Python se integra con CUPS (Common UNIX Printing System) para administrar trabajos de impresión y asegura que cada imagen se imprima con éxito mientras proporciona retroalimentación en tiempo real sobre el estado del trabajo. Para garantizar la confidencialidad y la seguridad de los datos, la imagen se elimina inmediatamente después de ser enviada a la impresora.

## Características

- **Integración Directa con CUPS**: Aprovecha el servidor CUPS para enviar y administrar trabajos de impresión, asegurando una amplia compatibilidad con diversas impresoras.
- **Monitoreo de Trabajos de Impresión en Tiempo Real**: Rastrea el estado de cada trabajo de impresión en tiempo real, proporcionando actualizaciones sobre la finalización, errores o cancelaciones.
- **Manejo de Errores e Informes**: Mecanismos de manejo de errores integrales informan problemas a la aplicación, asegurando un funcionamiento fluido.
- **Diseño Modular**: El script está estructurado en funciones claras y concisas, lo que facilita su comprensión, mantenimiento y extensión.
- **Configurable**: Utiliza un módulo de configuración externo (`config.py`) para ajustes fáciles sin alterar el script principal.
- **Modo de Depuración**: Incluye un modo de depuración para pruebas y resolución de problemas sin enviar trabajos de impresión reales a la impresora.

## Componentes

- `send_message_to_app(message)`: Envía mensajes de estado o códigos de error a la aplicación principal de DoxBox `app.py` para registro o notificación al usuario.
- `check_print_job_status(conn, job_id)`: Monitorea el estado de los trabajos de impresión enviados, asegurando que se completen con éxito o manejando errores según sea necesario.
- `print_image(printer_name, image_path)`: Envía un archivo de imagen a la impresora especificada e inicia el proceso de monitoreo.
- `copy_file(source_path, destination_path)`: Maneja la transferencia segura de archivos de imagen desde el lugar de captura a la cola de impresión.
- `move_image()`: Orquesta el proceso de preparación de imágenes para la impresión, incluyendo la transferencia de archivos y la eliminación después de la impresión.

## Cómo Funciona

1. **Captura de Imagen**: Una vez que se captura una imagen con DoxBox, se almacena en un directorio predeterminado.
2. **Preparación de Archivos**: La función `move_image` escanea el directorio en busca de nuevas imágenes, preparándolas para la impresión.
3. **Impresión**: Las imágenes se envían a la función `print_image`, donde se envían como trabajos de impresión a la impresora configurada.
4. **Monitoreo**: El estado de cada trabajo de impresión se monitorea en tiempo real por `check_print_job_status`, proporcionando retroalimentación sobre el progreso del trabajo y manejando cualquier problema que surja.
5. **Finalización**: Una vez que se completa la impresión con éxito, el archivo de imagen se elimina y el sistema está listo para la próxima captura.

## Configuración

El script depende de un archivo `config.py` separado para los ajustes de configuración, como los detalles del servidor CUPS, el nombre de la impresora y los directorios para el almacenamiento y la impresión de imágenes. Esto permite ajustes fáciles a diferentes entornos o impresoras.

## Depuración y Registro

El modo de depuración se puede activar para fines de prueba, simulando el proceso de impresión sin enviar trabajos a la impresora. El registro en consola proporciona retroalimentación en tiempo real sobre la operación del script.

## Dependencias

- CUPS
- Python-CUPS (para interactuar con el servidor CUPS desde Python)
- Bibliotecas estándar de Python: `datetime`, `shutil`, `socket`, `os`, `time`

## Ejemplo de Uso

Ejemplo de uso que demuestra cómo llamar a la función `print_image` con valores codificados para el nombre de la impresora y la ruta de la imagen. Este ejemplo sirve como guía básica para integrar la funcionalidad de impresión en flujos de trabajo de aplicaciones más amplios.

```python
printer_name = "Su_Nombre_De_Impresora_Aquí"
image_directory = "/ruta/a/directorio/de/imagen"
image_file = "ejemplo.jpg"

image_path = os.path.join(image_directory, image_file)
print_image(printer_name, image_path)
```

## Para Empezar

1. Asegúrese de que CUPS esté instalado y configurado en su sistema.
2. Instale Python-CUPS usando pip: `pip install pycups`.
3. Ajuste el archivo `config.py` para que coincida con su entorno.
4. Ejecute el script después de que se capture una imagen para iniciar el proceso de impresión.

1. **Actualice Su Sistema**: Asegúrese de que sus listas de paquetes y los paquetes instalados estén actualizados.

   ```bash
   sudo apt-get update
   sudo apt-get upgrade
   ```

Esto asegurará que su Raspberry Pi esté ejecutando el software más reciente.

**Instale CUPS y Herramientas de Desarrollo**: Instale CUPS (Common UNIX Printing System), las bibliotecas de desarrollo de CUPS y los encabezados de desarrollo de Python. Estas bibliotecas son esenciales para compilar pycups.

```bash
sudo apt-get install libcups2-dev libcupsimage2-dev gcc python3-dev
```

Este comando instala las bibliotecas y herramientas de desarrollo necesarias.

**Instale pycups Usando pip**: Después de instalar los paquetes de desarrollo necesarios, intente instalar pycups nuevamente usando pip3.

```bash
pip3 install pycups
```

Ahora debería poder compilar e instalar pycups con éxito.

**Actualice pip, setuptools y wheel (Si es Necesario)**: En algunos casos, es posible que necesite asegurarse de que sus paquetes pip, setuptools y wheel estén actualizados.

```bash
pip3 install --upgrade pip setuptools wheel
```

Después de actualizar estos paquetes, intente instalar pycups nuevamente.
