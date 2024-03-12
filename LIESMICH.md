# DoxBox - eine Bitcoin ⚡️ Lightning Fotobox

<p align="center">
<img src="https://raw.githubusercontent.com/j0sh21/DoxBox/main/docs/images/Box.jpeg" width="200">
</p>

Die DoxBox druckt aufgenommene Bilder aus, sobald Bitcoin Lightning-Zahlungen an sein LNbits-Wallet getätigt werden. Sie können es auf jeder Hochzeit, einer Konferenz, einem Treffen oder einem Festival einrichten. Wir haben es modular konstruiert, damit Sie es problemlos mitnehmen können.

## Schlüsselkomponenten

- **main.py**: Dient als Einstiegspunkt der Anwendung und koordiniert die Ausführung verschiedener Komponenten basierend auf Betriebsmodi.
- **app.py**: Verwaltet die grafische Benutzeroberfläche (GUI) der Anwendung, erleichtert Benutzerinteraktionen und zeigt Informationen an.
- **switch.py**: Behandelt externe API-Interaktionen und führt spezifische Aktionen basierend auf den empfangenen Daten aus, wie das Auslösen anderer Anwendungskomponenten.
- **img_capture.py**: Interagiert mit Kameras, um Bilder aufzunehmen, herunterzuladen und die Dateispeicherung zu verwalten, nutzt gphoto2.
- **print.py (In Arbeit)**: Verbindet sich mit Druckern über CUPS, um Bilder zu drucken, mit Funktionen zur Druckerauswahl und Druckauftragsverwaltung.
- **config.py**: Enthält Konfigurationseinstellungen, die in der gesamten Anwendung verwendet werden, wie API-Schlüssel, Gerätenamen und Dateipfade.

## Hardware-Anforderungen

- **Raspberry Pi 4**, läuft mit dem Debian-basierten Betriebssystem, [verfügbar auf der offiziellen Raspberry Pi-Softwareseite.](https://www.raspberrypi.com/software/operating-systems/)
- **DSLR-Kamera**: Canon EOS 450D mit mindestens 1GB SD-Karte. Bei Verwendung einer anderen Kamera [stellen Sie die Kompatibilität mit gphoto2 auf der offiziellen Website sicher](http://www.gphoto.org/proj/libgphoto2/support.php)
- **Display**: Waveshare 10,4" QLED Quantum Dot Kapazitiver Bildschirm (1600 x 720)
- **Drucker**: Xiaomi-Instant-Photo-Printer-1S, unterstützt das CUPS-Drucksystem, 6" Fotopapier
- **LED**: 4-Kanal-RGB-LED-Streifen zusammen mit einem Steckbrett, Verbindungskabeln und 4 Mosfets zur Steuerung.
- **Baumaterial**: Drei Platten aus 80x80cm Sperrholz; Zugang zu einem Laserschneider könnte von Vorteil sein.
- **Montagematerial**: 20 Eckmagnete (je 2 Stück pro Ecke), 40 Schrauben mit 4mm Durchmesser und 120 Muttern mit 4mm Durchmesser zur Befestigung der Komponenten.
- **Sprühfarbe**: 1 Dose Grundierung, 4 Dosen der eigentlichen Farbe


  <img src="https://github.com/j0sh21/DoxBox/assets/63317640/384280e0-cc6e-4bd0-9953-c318b5e12f15" height="200">

  <img src="https://github.com/j0sh21/DoxBox/assets/63317640/e446af16-d840-4cbc-87f9-3d5f67b3a15d" height="200">
  <img src="docs/images/poc.gif" height="200">

## Beispiel Programmablauf:
<img src="docs/images/flowchart.JPG" height="1100">

## Einrichtungsanleitung

1. **Repository klonen**: Beginnen Sie damit, dieses Repository auf Ihren lokalen Rechner zu klonen.

```sh
git clone https://github.com/j0sh21/DoxBox.git
```

2. **Abhängigkeiten installieren**: Stellen Sie sicher, dass Python auf Ihrem System installiert ist, und installieren Sie dann die erforderlichen Python-Pakete.



```sh
pip install -r requirements.txt
```
   **Hinweis**: Einige Komponenten können zusätzliche systemweite Abhängigkeiten erfordern (z.B. gphoto2, CUPS).

   - Wenn Sie zusätzliche systemweite Abhängigkeiten automatisch installieren möchten, führen Sie stattdessen install.sh aus:

      ```sh
      cd DoxBox/install
      chmod u+x install.sh
      ./install.sh
      ```

3. **Konfigurieren**: Überprüfen und aktualisieren Sie `config/cfg.ini` mit Ihren spezifischen Einstellungen, wie Gerätenamen, API-Schlüsseln und Dateipfaden.

## Nutzung

Um die Anwendung auszuführen, navigieren Sie zum Projektverzeichnis und führen Sie `main.py` aus:
 ```sh
python3 main.py
 ```
Für spezifische Funktionen, wie das Aufnehmen eines Bildes oder **Drucken**, können Sie die jeweiligen Skripte ausführen.
```sh
python3 img_capture.py
```
für die Bildaufnahme 

**Drucke ein Bild**: Aktualisiere print.py mit dem Namen dines Druckers und dem Pfad zum Bild, dann führe folgendes aus:
```sh
python3 print.py
```


# Changelog für das DoxBox Projekt
## Version 0.1 veröffentlich am 25. Feb 2024

### Funktionen
- `app.py` aktualisiert, um neue Rahmen und neue GIFs zu verwenden.
- Neue GIFs von @arbadacarbaYK integriert, ohne leere Hintergrundrahmen und Wasserzeichen. Countdown-GIFs haben jetzt eine gleichmäßige Zeit zwischen den Zahlen.
- `self.isreplay` hinzugefügt, um die GIF-Schleifenzählung nur einmal zurückzusetzen.
- Neue Fehlercodes aus `switch.py` in die Dokumentation in Deutsch, Englisch und Portugiesisch aufgenommen.
- Neuer Zustand 3.5 implementiert: Übergang zu `img_capture.py` nach dem ersten Lächeln-GIF.
- Neuer Zustand 3.9 implementiert: Foto erfolgreich von der Kamera übertragen, Vorbereitung des Druckvorgangs eingeleitet.
- Zustand 4 vorgezogen: Wird früher ausgelöst, um den Druckvorgang zu starten, bevor das Foto von der Kamera gelöscht wird.
- Kamera-spezifische Fehlerbehandlung in `img_capture.py` überarbeitet.
- Maximale Wiederholungsversuche und variable Wartezeiten für kamerabezogene Fehler eingeführt.

### Verbesserungen
- Netzwerkverbindung wird überprüft, bevor die LNbits-API abgefragt wird.
- Konsolenausgabe in Stil und Übersichtlichkeit verbessert.
- Mauszeiger für eine sauberere Benutzeroberfläche ausgeblendet.
- Log-Nachrichten in Klarheit und Detail verbessert.
- Beschädigte Dateien entfernt und allgemeine Aufräumarbeiten durchgeführt.
- LED-Effekte für besseres visuelles Feedback angepasst.

### Korrekturen
- `def kill_process()` korrigiert, um sicherzustellen, dass Prozesse ordnungsgemäß beendet werden.
- Problem behoben, bei dem mehrere Lächeln-GIFs gleichzeitig angezeigt werden konnten.
- Ein Fehler behoben, bei dem Zustand 204 unendlich lange bei der Überprüfung von Druckauftragsfehlern hängen bleiben konnte.

### Infrastruktur
- Ein Ausgabeordner für Druckaufträge erstellt. **TODO:** Ordnererstellung automatisieren mit `os.mkdir`, statt einen leeren Ordner im Repository zu inkludieren.
- **TODO:** Funktionalität von `check_print_job_status` feinjustieren.

## Mitwirken

Beiträge zum Projekt sind willkommen! Bitte beachten Sie die Richtlinien für Beiträge, um Informationen darüber zu erhalten, wie Sie Pull Requests einreichen, Probleme melden oder Verbesserungen vorschlagen können.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe die Datei LICENSE für Details.

## Danksagungen

Ein besonderer Dank gilt allen Mitwirkenden und Betreuern der externen Bibliotheken und Werkzeuge, die in diesem Projekt verwendet werden.
