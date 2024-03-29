
# DoxBox - una fotocabina de bitcoin ⚡️ lightning

<p align="center">
<img src="https://raw.githubusercontent.com/j0sh21/DoxBox/main/docs/images/Box.jpeg" width="200">
</p>

La DoxBox imprime fotos capturadas tras recibir pagos a través de bitcoin lightning en su billetera [LNbits](https://github.com/lnbits/lnbits).
Puedes configurarla en cualquier boda, conferencia, meetup o festival. La hemos construido de manera modular para que puedas viajar fácilmente con ella.


## Requisitos de Hardware

- **Raspberry Pi 4** ejecutando el sistema operativo basado en Debian [disponible en la página oficial de software de Raspberry Pi](https://www.raspberrypi.com/software/operating-systems/).
- **Cámara DSLR**: Canon EOS 450D con al menos 1GB de tarjeta SD. Si usas otra, [asegúrate de verificar la compatibilidad con gphoto2 en la página oficial](http://www.gphoto.org/proj/libgphoto2/support.php).
- **Pantalla**: Waveshare 10.4" QLED Quantum Dot Display Capacitivo (1600 x 720).
- **Impresora**: Xiaomi-Instant-Photo-Printer-1S, compatible con el sistema de impresión CUPS, papel fotográfico de 6".
- **LED**: Tira de LED RGB de 4 canales, junto con una protoboard, cables de conexión y 4 Mosfets para el control.
- **Material de Construcción**: Tres láminas de madera contrachapada de 80x80cm; el acceso a una cortadora láser puede ser beneficioso.
- **Hardware de Montaje**: 20 sets de imanes de esquina (2 piezas por set), 40 tornillos de 4mm de diámetro y 120 tuercas de 4mm de diámetro para asegurar los componentes.
- **Color de spray**: 1 lata de imprimación, 4 latas del color real.


  
<img src="https://github.com/j0sh21/DoxBox/assets/63317640/384280e0-cc6e-4bd0-9953-c318b5e12f15" height="200">
<img src="https://github.com/j0sh21/DoxBox/assets/63317640/e446af16-d840-4cbc-87f9-3d5f67b3a15d" height="200">
<img src="https://github.com/j0sh21/DoxBox/assets/63317640/4bcc6965-a1fa-41e5-8d07-cc7e3280bc58" height="200">


## Ejemplo de flujo del programa:

<img src="docs/images/flowchart.JPG" height="1100">


## Instrucciones de Configuración

### Componentes Clave

- **main.py**: Sirve como el punto de entrada de la aplicación, orquestando la ejecución de varios componentes basados en los modos operativos.
- **app.py**: Gestiona la interfaz gráfica de usuario (GUI) de la aplicación, facilitando las interacciones del usuario y mostrando información.
- **switch.py**: Maneja interacciones con APIs externas y realiza acciones específicas basadas en los datos recibidos, como activar otros componentes de la aplicación.
- **img_capture.py**: Interactúa con cámaras para capturar imágenes, descargarlas y gestionar el almacenamiento de archivos, aprovechando gphoto2.
- **print.py (En Progreso)**: Se comunica con impresoras usando CUPS para imprimir imágenes, con funcionalidad para seleccionar impresoras y gestionar trabajos de impresión.
- **config.py**: Contiene configuraciones utilizadas a lo largo de la aplicación, como claves de API, nombres de dispositivos y rutas de archivos.

### Instalación

1. **Clonar el Repositorio**: Comienza clonando este repositorio.

   ```sh
   git clone https://github.com/j0sh21/DoxBox.git
    ```
2. **Instalar Dependencias**: Asegúrate de que Python esté instalado en tu sistema, instala los paquetes de Python requeridos.

    ```sh

    pip install -r requirements.txt
    ```
    **Nota**: Algunos componentes pueden requerir dependencias adicionales a nivel de sistema (por ejemplo, gphoto2, CUPS).
   

   - Si deseas instalar dependencias a nivel de sistema automáticamente, ejecuta install.sh en su lugar:
      ```sh
      cd DoxBox/install
      chmod u+x install.sh
      ./install.sh

3. **Configurar**: Revisa y actualiza config/cfg.ini con tus configuraciones específicas, como nombres de dispositivos, claves de API y rutas de archivos.
   ```sh
   nano cfg.ini
## Uso

Para ejecutar la aplicación, navega al directorio del proyecto y ejecuta main.py:

 ```sh
python3 main.py
 ```
Para funcionalidades específicas, como capturar una imagen o imprimir, puedes ejecutar los scripts respectivos (por ejemplo, python img_capture.py para captura de imágenes).
Ejemplo de Uso

**Capturar una Imagen** Asegúrate de que tu cámara esté conectada y reconocida por tu sistema, luego ejecuta:

 ```sh
python3 img_capture.py
 ```
**Imprimir una Imagen**: Actualiza print.py con el nombre de tu impresora y la ruta del archivo de imagen, luego ejecuta:
 ```sh
  python print.py
 ```

## Registro de cambios para el proyecto DoxBox
### Versión 0.1, lanzada el 25 de febrero de 2024

### Características
- Actualizado `app.py` para usar nuevos marcos y nuevos GIFs.
- Integrados nuevos GIFs de @arbadacarbaYK, eliminando marcos de fondo vacíos y marcas de agua. Los GIFs de cuenta regresiva ahora tienen una temporización consistente entre números.
- Añadido `self.isreplay` para restablecer el conteo de bucles del GIF solo una vez.
- Introducidos nuevos códigos de error de `switch.py` en la documentación en inglés, alemán y portugués.
- Implementado nuevo estado 3.5: Transición a `img_capture.py` después de finalizar el primer GIF de sonrisa.
- Implementado nuevo estado 3.9: Foto transferida con éxito desde la cámara, iniciando la preparación para la impresión.
- Avanzado estado 4: Activado antes para comenzar la impresión antes de que la foto sea eliminada de la cámara.
- Refactorizado el manejo de errores específicos de la cámara en `img_capture.py`.
- Introducidos máximos intentos de reintentos y tiempos de espera variables para errores relacionados con la cámara.

### Mejoras
- Añadidas verificaciones de conectividad de red antes de consultar la API de LNbits.
- Mejorado y limpiado el estilo de salida de la consola.
- Cursor del ratón oculto para una interfaz más limpia.
- Mejorada la claridad y el detalle de los mensajes de log.
- Eliminados archivos corruptos y realizada una limpieza general.
- Ajustados efectos de LED para un mejor feedback visual.

### Correcciones
- Corregido `def kill_process()` para asegurar una terminación adecuada del proceso.
- Solucionado el problema donde se podían mostrar múltiples GIFs de sonrisa simultáneamente.
- Resuelto un bug donde el estado 204 podía quedar colgado indefinidamente en las comprobaciones de fallos de trabajos de impresión.

### Infraestructura
- Creada una carpeta de salida para trabajos de impresión. **POR HACER:** Automatizar la creación de carpetas usando `os.mkdir` en lugar de incluir una carpeta vacía en el repositorio.
- **POR HACER:** Ajustar la funcionalidad de `check_print_job_status`.

## Contribuir

¡Las contribuciones al proyecto son bienvenidas! Consulte las pautas de contribución para obtener información sobre cómo enviar solicitudes de extracción, informar de problemas o sugerir mejoras.

## Licencia
Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para detalles. 
¡Las contribuciones al proyecto son bienvenidas! 

## Agradecimientos
Un agradecimiento especial a [Ben Arc](https://github.com/arcbtc) por [LNbits](https://github.com/lnbits/lnbits) y a todos los mantenedores de las bibliotecas y herramientas externas también utilizadas en este proyecto.

 ⚡️ [Dona a este proyecto](https://legend.lnbits.com/lnurlp/link/4Wc7ZE) si te gusta la DoxBox ⚡️

