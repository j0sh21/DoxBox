
## Übersicht

Der `DoxBoxPrintManager` (`print.py`) ist eine wesentliche Komponente des DoxBox-Systems, die darauf ausgelegt ist, das Drucken von Bildern unmittelbar nach deren Erfassung nahtlos zu handhaben. Dieses Python-Skript integriert sich in CUPS (Common UNIX Printing System), um Druckaufträge zu verwalten und sicherzustellen, dass jedes Bild erfolgreich gedruckt wird, während es Echtzeit-Feedback zum Status des Auftrags gibt. Um Vertraulichkeit und Datensicherheit zu gewährleisten, wird das Bild unmittelbar nach dem Senden an den Drucker gelöscht.

## Funktionen

- **Direkte Integration mit CUPS**: Nutzt den CUPS-Server, um Druckaufträge einzureichen und zu verwalten, was eine breite Kompatibilität mit verschiedenen Druckern gewährleistet.
- **Echtzeit-Überwachung von Druckaufträgen**: Verfolgt den Status jedes Druckauftrags in Echtzeit und bietet Updates zu Fertigstellung, Fehlern oder Stornierungen.
- **Fehlerbehandlung und Berichterstattung**: Umfassende Fehlerbehandlungsmechanismen melden Probleme zurück an die Anwendung und gewährleisten einen reibungslosen Betrieb.
- **Modulares Design**: Das Skript ist in klare, prägnante Funktionen strukturiert, was es leicht verständlich, wartbar und erweiterbar macht.
- **Konfigurierbar**: Verwendet ein externes Konfigurationsmodul (`config.py`) für einfache Anpassungen ohne Änderung des Kernskripts.
- **Debug-Modus**: Beinhaltet einen Debug-Modus für Tests und Fehlerbehebung ohne tatsächliche Druckaufträge an den Drucker zu senden.

## Komponenten

- `send_message_to_app(message)`: Sendet Statusmeldungen oder Fehlercodes an die Hauptanwendung DoxBox `app.py` zum Protokollieren oder zur Benachrichtigung des Benutzers.
- `check_print_job_status(conn, job_id)`: Überwacht den Status der eingereichten Druckaufträge, um sicherzustellen, dass sie erfolgreich abgeschlossen werden oder Fehler bei Bedarf behandelt werden.
- `print_image(printer_name, image_path)`: Reicht eine Bilddatei beim angegebenen Drucker ein und initiiert den Überwachungsprozess.
- `copy_file(source_path, destination_path)`: Verwaltet den sicheren Transfer von Bilddateien vom Erfassungsort zur Druckwarteschlange.
- `move_image()`: Orchestriert den Prozess der Vorbereitung von Bildern zum Drucken, einschließlich Dateitransfer und Löschung nach dem Drucken.

Der Debug-Modus kann für Testzwecke aktiviert werden, um den Druckprozess zu simulieren, ohne Aufträge an den Drucker zu senden. Die Konsolenprotokollierung bietet Echtzeit-Feedback zum Betrieb des Skripts.
## Funktionsweise

1. **Bildaufnahme**: Sobald ein Bild von der DoxBox aufgenommen wurde, wird es in einem vordefinierten Verzeichnis gespeichert.
2. **Dateivorbereitung**: Die Funktion `move_image` scannt das Verzeichnis nach neuen Bildern und bereitet sie zum Drucken vor.
3. **Drucken**: Bilder werden an die Funktion `print_image` gesendet, wo sie als Druckaufträge an den konfigurierten Drucker übermittelt werden.
4. **Überwachung**: Der Status jedes Druckauftrags wird in Echtzeit von `check_print_job_status` überwacht, wobei Rückmeldungen zum Fortschritt des Auftrags gegeben und auftretende Probleme behandelt werden.
5. **Abschluss**: Nach erfolgreichem Druck wird die Bilddatei gelöscht und das System ist bereit für die nächste Aufnahme.

## Konfiguration
Das Skript stützt sich auf eine separate `config.py`-Datei für Konfigurationseinstellungen, wie die CUPS-Serverdetails, den Druckernamen und Verzeichnisse für die Bildspeicherung und den Druck. Dies ermöglicht einfache Anpassungen an unterschiedliche Umgebungen oder Drucker.

## Debugging und Protokollierung

Der Debug-Modus kann für Testzwecke aktiviert werden, um den Druckprozess zu simulieren, ohne Aufträge an den Drucker zu senden. Die Konsolenprotokollier
## Abhängigkeiten

- CUPS
- Python-CUPS (für die Interaktion mit dem CUPS-Server von Python aus)
- Standard Python-Bibliotheken: `datetime`, `shutil`, `socket`, `os`, `time`

## Beispielverwendung

Ein Beispiel, das zeigt, wie die Funktion `print_image` mit festen Werten für den Druckernamen und den Bildpfad aufgerufen wird. Dieses Beispiel dient als grundlegende Anleitung für die Integration der Druckfunktionalität in umfassendere Anwendungsworkflows.

```python
printer_name = "Ihr_Druckername_Hier"
image_directory = "/pfad/zum/bildverzeichnis"
image_file = "beispiel.jpg"

image_path = os.path.join(image_directory, image_file)
print_image(printer_name, image_path)
```

## Erste Schritte

1. Stellen Sie sicher, dass CUPS auf Ihrem System installiert und konfiguriert ist.
2. Installieren Sie Python-CUPS mit pip: `pip install pycups`.
3. Passen Sie die Datei `config.py` an Ihre Umgebung an.
4. Führen Sie das Skript aus, nachdem ein Bild aufgenommen wurde, um den Druckprozess zu initiieren.

### Erforderliche Abhängigkeiten auf z.B. Raspberry Pi installieren:

Um pycups auf Ihrem Raspberry Pi zu verwenden, müssen Sie sicherstellen, dass die erforderlichen Abhängigkeiten installiert sind. Hier sind die Schritte dazu:

1. **Aktualisieren Sie Ihr System**: Stellen Sie sicher, dass Ihre Paketlisten und installierten Pakete auf dem neuesten Stand sind.

   ```bash
   sudo apt-get update
   sudo apt-get upgrade

Dies stellt sicher, dass Ihr Raspberry Pi die neueste Software ausführt.

**CUPS und Entwicklungswerkzeuge installieren**: Installieren Sie CUPS (Common UNIX Printing System), die CUPS-Entwicklungsbibliotheken und die Python-Entwicklungsheader. Diese Bibliotheken sind für die Kompilierung von pycups unerlässlich.

    sudo apt-get install libcups2-dev libcupsimage2-dev gcc python3-dev

Dieser Befehl installiert die notwendigen Bibliotheken und Entwicklungswerkzeuge.

Installieren Sie pycups mit pip: Nachdem Sie die erforderlichen Entwicklungspakete installiert haben, versuchen Sie, pycups erneut mit pip3 zu installieren.

    pip3 install pycups

Jetzt sollten Sie in der Lage sein, pycups erfolgreich zu kompilieren und zu installieren.

Upgrade pip, setuptools und wheel (falls erforderlich): In einigen Fällen müssen Sie möglicherweise sicherstellen, dass Ihre pip-, setuptools- und wheel-Pakete auf dem neuesten Stand sind.

    pip3 install --upgrade pip setuptools wheel

Nach dem Upgrade dieser Pakete versuchen Sie erneut, pycups zu installieren.