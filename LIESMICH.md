# Projektübersicht

Dieses Projekt ist darauf ausgelegt, die Fähigkeiten eines Raspberry Pi oder eines anderen auf Debian basierenden Hostsystems zu nutzen, um mit einer DSLR-Kamera hochwertige Bilder aufzunehmen und gleichzeitig einen bestimmten Anwendungsablauf zu verwalten und mit diesem zu interagieren. Dieser Ablauf umfasst die Aufnahme von Bildern, das Drucken und die Interaktion mit einer dynamischen Benutzeroberfläche. Die Anwendung läuft auf Python und integriert sich mit verschiedenen externen Systemen und Bibliotheken, wie CUPS zum Drucken und gphoto2 zur Kamerasteuerung, um ihre Funktionalität bereitzustellen.

## Hauptkomponenten

- **main.py**: Dient als Einstiegspunkt der Anwendung und orchestriert die Ausführung verschiedener Komponenten basierend auf den Betriebsmodi.
- **app.py**: Verwaltet die grafische Benutzeroberfläche (GUI) der Anwendung, erleichtert die Benutzerinteraktionen und zeigt Informationen an.
- **switch.py**: Handhabt externe API-Interaktionen und führt bestimmte Aktionen aufgrund der empfangenen Daten aus, wie das Auslösen anderer Anwendungskomponenten.
- **img_capture.py**: Interagiert mit Kameras, um Bilder aufzunehmen, herunterzuladen und die Dateispeicherung zu verwalten, unter Verwendung von gphoto2.
- **print.py (In Bearbeitung)**: Kommuniziert mit Druckern über CUPS, um Bilder zu drucken, mit der Möglichkeit, Drucker auszuwählen und Druckaufträge zu verwalten.
- **config.py**: Enthält Konfigurationseinstellungen, die in der gesamten Anwendung verwendet werden, wie API-Schlüssel, Gerätenamen und Dateipfade.

## Hardware-Anforderungen

- **Host-System**: Die Kernplattform zur Ausführung der Anwendung (z. B. Raspberry Pi, Mini-PC), die die notwendigen Rechenressourcen und die Konnektivität für Peripheriegeräte bereitstellt.
- **DSLR-Kamera**: Wird für die Aufnahme hochwertiger Bilder verwendet. Stellen Sie sicher, dass sie mit gphoto2 kompatibel ist.
- **Webcam**: Eine Webcam muss angeschlossen und für die Funktionen zur Bildaufnahme konfiguriert sein.
- **Display**: Ein Display wird benötigt, um die GUI anzuzeigen, einschließlich Fotovorschauen und Animationen.
- **Drucker**: Ein Fotodrucker, der auf dem Host-System eingerichtet und für das Drucken von Bildern mit CUPS kompatibel ist.

## Einrichtungsanweisungen

1. **Repository klonen**: Beginnen Sie mit dem Klonen dieses Repositorys auf Ihren lokalen Computer.

   ```sh
   git clone https://github.com/j0sh21/DoxBox.git
    ```
2. **Abhängigkeiten installieren**: Stellen Sie sicher, dass Python auf Ihrem System installiert ist und installieren Sie dann die erforderlichen Python-Pakete.

    ```sh
    pip install -r requirements.txt
    ```
    **Hinweis**: Einige Komponenten erfordern möglicherweise zusätzliche systemweite Abhängigkeiten (z. B. gphoto2, CUPS).
   

   - Wenn Sie zusätzliche systemweite Abhängigkeiten automatisch installieren möchten, führen Sie stattdessen install.sh aus:
      ```sh
      chmod install.sh +x
      ./install.sh

3. **Konfigurieren**: Überprüfen und aktualisieren Sie config/cfg.ini mit Ihren spezifischen Einstellungen, wie Gerätenamen, API-Schlüsseln und Dateipfaden.
   ```sh
   nano cfg.ini
## Verwendung

Um die Anwendung auszuführen, navigieren Sie zum Projektverzeichnis und führen Sie main.py aus:

 ```sh
python main.py
```

Für spezielle Funktionen, wie das Aufnehmen eines Bildes oder das Drucken, können Sie die entsprechenden Skripte ausführen (z. B. python img_capture.py für die Bildaufnahme).
## Beispiel

1. Ein Bild aufnehmen Stellen Sie sicher, dass Ihre Kamera angeschlossen und von Ihrem System erkannt wird, und führen Sie dann aus:

        python img_capture.py

2. Ein Bild drucken: Aktualisieren Sie print.py mit dem Namen Ihres Druckers und dem Dateipfad des Bildes, und führen Sie dann aus
     ```
    python print.py
     ```

# Mitwirken

Beiträge zum Projekt sind willkommen! Bitte beachten Sie die Beitragshinweise für weitere Informationen zur Einreichung von Pull-Anfragen, zur Meldung von Problemen oder zur Vorschlagsverbesserung.
# Lizenz

Dieses Projekt steht unter der MIT-Lizenz - siehe die LICENSE-Datei für Details.
# Danksagung

Ein besonderer Dank geht an alle Beitragenden und Wartenden der externen Bibliotheken und Tools, die in diesem Projekt verwendet werden.