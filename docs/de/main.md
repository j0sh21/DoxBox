
# Dokumentation für main.py

## Übersicht
Dieses Modul dient als Einstiegspunkt für die DoxBox, koordiniert den Start und die Verwaltung verschiedener Komponenten, einschließlich eines Anwendungsservers, LED-Servers und zusätzlicher Hilfsmittel für Debugging und Gerätesteuerung.

## Abhängigkeiten
- Python 3
- `subprocess`-Modul zum Ausführen von Skripten.
- `threading`-Modul für die gleichzeitige Ausführung.
- `pigpiod` für die LED-Steuerung (separat installiert und ausgeführt).
- **Projektmodule**: `led.py`, `app.py`, `switch.py` (bedingt `./dev/process_mock.py` und `./dev/debug_client.py` für Debugging)

## Schlüsselkomponenten

### 1. Anwendungsserver
- **Funktionalität**: Verwaltet die Hauptanwendungslogik.
- **Skript**: `app.py`

### 2. LED-Server
- **Funktionalität**: Steuert LED-Operationen.
- **Skript**: `led.py`
- **Abhängigkeiten**: Erfordert den `pigpiod`-Daemon für die GPIO-Pin-Steuerung.

### 3. Debugging-Tools
- **Funktionalität**: Bietet Debugging-Fähigkeiten.
- **Skripte**: `debug_client.py` und `process_mock.py`
- **Modi**: Gesteuert durch die `DEBUG`-Variable in `config.py`.

### 4. Gerätesteuerung
- **Funktionalität**: Verwaltet gerätespezifische Operationen wie Zahlung und Druck.
- **Skript**: `switch.py`

## Konfiguration
Konfigurationseinstellungen, einschließlich des Debug-Modus, werden über `config.py` verwaltet. Passen Sie die Einstellungen in dieser Datei an, um das Verhalten der Anwendung zu steuern.

## Anwendung ausführen
- Starten Sie die Anwendung, indem Sie `main.py` ausführen.
- Das Skript initialisiert den Anwendungs- und LED-Server in separaten Threads.
- Abhängig vom Debug-Modus, der in `config.py` eingestellt ist, startet es entweder Debugging-Tools oder das Gerätesteuerungsskript.

## Debug-Modus
- **Level 0**: Normalbetrieb, `switch.py` wird ausgeführt.
- **Level 1**: Grundlegendes Debugging, `debug_client.py` wird ausgeführt.
- **Level 2**: Erweitertes Debugging, sowohl `debug_client.py` als auch `process_mock.py` werden ausgeführt.

## Anwendung erweitern
Um neue Funktionalitäten hinzuzufügen:
1. Erstellen Sie ein neues Skript für die Komponente.
2. Definieren Sie eine Funktion in `main.py`, um das Skript auszuführen, ähnlich wie `run_app()` oder `start_led()`.
3. Fügen Sie in `main()` einen Thread oder Subprozess-Aufruf hinzu, um die neue Funktion auszuführen.

## Fehlerbehebung
- Stellen Sie sicher, dass `pigpiod` installiert ist und vom Skript gestartet werden kann.
- Überprüfen Sie, ob alle referenzierten Skripte (`app.py`, `led.py`, `switch.py` usw.) in den erwarteten Verzeichnissen vorhanden sind.
- Überprüfen Sie `config.py` auf korrekte Debug-Modus-Einstellungen.

## Merkmale
- **Gleichzeitige Ausführung**: Nutzt Threads, um `app.py` und möglicherweise einen Mock-Prozess parallel auszuführen.
- **Bedingtes Debugging**: Abhängig vom `DEBUG_MODE` können zusätzliche Debugging-Prozesse ausgeführt werden, um bei der Entwicklung und beim Testen zu helfen.
- **Subprozess-Management**: Führt Schlüsselkomponenten (`app.py`, `switch.py` oder Debug-Prozesse) als Subprozesse aus, was eine isolierte und kontrollierte Ausführungsumgebung gewährleistet.

## Die DoxBox starten

Um die Anwendung auszuführen, geben Sie den folgenden Befehl im Terminal ein:

```bash
python3 main.py
```

Stellen Sie sicher, dass alle Abhängigkeiten korrekt installiert und konfiguriert sind, bevor Sie das Skript ausführen.
