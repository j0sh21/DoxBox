# Dokumentation für main.py

## Übersicht

Das Skript `main.py` dient als zentraler Einstiegspunkt für die Anwendung und orchestriert verschiedene Komponenten sowie deren Ausführung basierend auf Betriebsmodi. Es verwendet Thread und Unterprozesse, um verschiedene Teile der Anwendung gleichzeitig auszuführen und bietet Flexibilität bei der Fehlerbehebung und Funktionsprüfung.

## Abhängigkeiten

- **Standardbibliotheken**: threading, subprocess
- **Projektmodule**: config, app.py, switch.py (bedingt `./dev/process_mock.py` und `./dev/debug_client.py` zum Debuggen)

## Konfiguration

Das Skript verwendet Konfigurationseinstellungen aus dem `config`-Modul, insbesondere das Flag `DEBUG_MODE`, um den Betriebsmodus (Debug oder Standard) zu bestimmen.

## Funktionen

- **Parallel Ausführung**: Verwendet Threads, um `app.py` und gegebenenfalls einen Mock-Prozess parallel auszuführen.
- **Bedingtes Debugging**: Abhängig vom `DEBUG_MODE` können zusätzliche Debugging-Prozesse zur Unterstützung bei Entwicklung und Tests ausgeführt werden.
- **Unterprozessverwaltung**: Führt Schlüsselkomponenten (`app.py`, `switch.py` oder Debug-Prozesse) als Unterprozesse aus, um isolierte und kontrollierte Ausführungsumgebungen sicherzustellen.

### `run_app()`

Führt `app.py` als Unterprozess aus. Dieses Skript enthält die Kernfunktionalität der Anwendung und wird unabhängig vom Debug-Modus immer ausgeführt.

### `run_app2()`

Führt einen Mock-Prozess (`./dev/process_mock.py`) als Unterprozess aus, der für den Debug-Modus für Entwicklungs- oder Testzwecke vorgesehen ist.

### `run_switch_or_debug_as_subprocess()`

Bestimmt, ob `switch.py` oder der Debug-Client (`./dev/debug_client.py`) basierend auf der `DEBUG`-Flag aus der Konfiguration ausgeführt werden soll. Im Standardmodus wird `switch.py` ausgeführt, das für die Steuerung von Hardware- oder Netzwerkswitches oder anderen wichtigen Anwendungsfunktionen verantwortlich sein kann. Im Debug-Modus wird der Debug-Client ausgeführt, um Debugging und Entwicklung zu erleichtern.

## Ablauf der Ausführung

1. **Initialisierung**: Das Skript startet, indem es `app.py` in einem separaten Thread startet, um sicherzustellen, dass seine Kernfunktionalität gleichzeitig mit anderen Komponenten ausgeführt wird.
2. **Debug-Modusprüfung**: Wenn sich die Anwendung im Debug-Modus befindet, startet sie zusätzlich in einem anderen Thread einen Mock-Prozess für Entwicklung oder Tests.
3. **Komponentenausführung**: Abhängig vom Betriebsmodus führt `main.py` entweder `switch.py` für Standardbetrieb oder einen Debug-Client für Debugging-Zwecke aus.

## Ausführen des Skripts

Um die Anwendung auszuführen, geben Sie den folgenden Befehl in der Konsole ein:

```bash
python main.py
