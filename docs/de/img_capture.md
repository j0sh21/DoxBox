# Dokumentation für img_capture.py

## Übersicht

Das Skript `img_capture.py` ist ein integraler Bestandteil der Anwendung zur Verwaltung von Bildaufnahmeworkflows. Es kommuniziert mit digitalen Kameras über das Kommandozeilenprogramm gphoto2 und führt Aufgaben wie das Erfassen von Bildern, das Herunterladen in ein bestimmtes Verzeichnis und das Verwalten von Dateinamenskonventionen aus. Darüber hinaus beinhaltet es Netzwerkkommunikation, um Statusaktualisierungen oder Fehler an andere Teile der Anwendung weiterzuleiten.

## Abhängigkeiten

- **Externe Dienstprogramme**: Erfordert gphoto2 auf dem System installiert (`sudo apt-get install gphoto2`).
- **Standardbibliotheken**: `socket`, `datetime`, `os`, `subprocess`, `signal`
- **Projektmodule**: `config`

## Hauptfunktionen

### Kamerainteraktion

- Verwendet gphoto2-Befehle zur direkten Interaktion mit der Kamera, um Operationen wie das Auslösen der Bildaufnahme, das Herunterladen von Bildern und das Löschen der Speicherkarte der Kamera zu ermöglichen.

### Prozessverwaltung

- Enthält Funktionen zum Beenden bestimmter Systemprozesse, die die Kamerazugriff stören könnten, um während des Betriebs die exklusive Kontrolle über die Kamera sicherzustellen.

### Datei- und Verzeichnisverwaltung

- Erstellt Ausgabeverzeichnisse zur Speicherung erfasster Bilder und behandelt häufig auftretende Probleme wie bereits vorhandene Verzeichnisse oder Berechtigungsfehler.
- Implementiert Logik zur Umbenennung von erfassten Bildern, um diese gemäß vordefinierter Namenskonventionen zu organisieren und zu verwalten.

### Netzwerkkommunikation

- Verfügt über eine Funktion zum Senden von Nachrichten an andere Komponenten der Anwendung über TCP-Sockets, um die Kommunikation zwischen Prozessen und die Statusberichterstattung zu erleichtern.

## Hauptfunktionen

### `send_message_to_app(message)`

Sendet Statusnachrichten oder Fehlercodes an eine andere Komponente der Anwendung, um die Fehlerbehandlung und die Benutzerfeedback-Mechanismen zu verbessern.

### `kill_process()`

Sucht nach einem bestimmten Prozess nach Namen und beendet ihn, was in der Regel dazu dient, sicherzustellen, dass die Kamera nicht von einem anderen Prozess verwendet wird.

### `create_output_folder()`

Erstellt ein Verzeichnis zur Speicherung erfasster Bilder und behandelt häufig auftretende Dateisystemfehler gracefully.

### `run_gphoto2_command(command)`

Führt einen angegebenen gphoto2-Befehl für die Kamerainteraktion aus, eingebettet in Fehlerbehandlungslogik, um auftretende Probleme während der Ausführung zu erkennen und zu kommunizieren.

### `rename_pics()`

Benennt erfasste Bilder basierend auf einer Reihe von Kriterien, wie z.B. Datum und Uhrzeit, um die Dateiorganisation und -verwaltung zu erleichtern.

## Verwendung

Das Skript ist darauf ausgelegt, als Teil eines größeren Anwendungs-Workflows ausgeführt zu werden und wird in der Regel aufgerufen, wenn die Funktion zur Bildaufnahme erforderlich ist. Es arbeitet in einer Abfolge von Schritten, die das System und die Kamera vorbereiten, die Bildaufnahme ausführen und die resultierenden Dateien verwalten.

### Beispielworkflow

1. Prozessbeendigung: Stellen Sie sicher, dass keine konkurrierenden Prozesse auf die Kamera zugreifen.
2. Verzeichnisvorbereitung: Erstellen oder überprüfen Sie die Existenz des Ausgabeverzeichnisses zur Speicherung von Bildern.
3. Bildaufnahme: Trigger-Bildaufnahme und Behandlung der Kamerainteraktion.
4. Dateiverwaltung: Laden Sie Bilder in das Ausgabeverzeichnis herunter und benennen Sie sie gemäß den Anforderungen der Anwendung um.

## Überlegungen

- Stellen Sie sicher, dass gphoto2 auf dem System installiert und ordnungsgemäß konfiguriert ist, auf dem die Anwendung ausgeführt wird.
- Das Skript sollte die entsprechenden Berechtigungen haben, um mit der Kamera, dem Dateisystem und den Netzwerk-Sockets zu interagieren.

## Installation von gphoto2

Um die Funktion zur Steuerung von DSLR-Kameras des Projekts zu aktivieren, müssen Sie gphoto2 auf Ihrem Raspberry Pi oder einem Debian-basierten System installieren. Gphoto2 ist ein vielseitiges Kommandozeilenprogramm, das die Kommunikation mit einer Vielzahl von digitalen Kameras erleichtert.

**So installieren Sie gphoto2**:

1. **Aktualisieren Sie Ihr System**: Stellen Sie zunächst sicher, dass Ihre Paketlisten und installierten Pakete auf dem neuesten Stand sind.

   ```sh
   sudo apt-get update

2. **Installieren Sie gphoto2**: Verwenden Sie den folgenden Befehl, um das Paket gphoto2 und seine Abhängigkeiten zu installieren.
    ```sh
    sudo apt-get install gphoto2

Dieser Befehl lädt automatisch gphoto2 herunter und installiert es auf Ihrem System.

Mit gphoto2 erfolgreich installiert, wird Ihr Raspberry Pi oder Debian-basiertes System in der Lage sein, mit DSLR-Kameras zu kommunizieren und die Funktionen zur Bildaufnahme zu steuern.

Für weitere ausführliche Informationen zu gphoto2 und seinen umfangreichen Fähigkeiten können Sie die offizielle gPhoto-Website besuchen.
