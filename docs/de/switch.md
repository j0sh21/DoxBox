# Dokumentation für switch.py

## Übersicht

Das `switch.py`-Modul ist eine wichtige Komponente der Anwendung, die für die Überwachung von Daten externer APIs, die Erkennung signifikanter Änderungen und die Kommunikation mit anderen Teilen der Anwendung verantwortlich ist, um spezifische Aktionen aufgrund dieser Änderungen auszulösen. Es verwendet Netzwerkanfragen, Thread-Verarbeitung und Socket-Programmierung, um seine Ziele zu erreichen.

## Abhängigkeiten

- **Standardbibliotheken**: requests, time, threading, socket
- **Projektmodule**: config

## Konfiguration

Das Modul stützt sich auf verschiedene Einstellungen, die im Modul `config` definiert sind, einschließlich:

- `API_URL`: Die URL der externen API, die überwacht werden soll.
- `API_KEY`: Der zur API-Authentifizierung erforderliche Schlüssel.
- `HOST, PORT`: Netzwerkeinstellungen für die Kommunikation über Sockets.
- `AMOUNT_THRESHOLD`: Ein bestimmter Schwellenwert, der eine Aktion auslöst, wenn er erreicht wird.
- `CHECK_INTERVAL`, `POST_PAYMENT_DELAY`: Zeitintervalle für die operationelle Geschwindigkeit.

## Schlüsselfunktionen

### `send_message_to_app(message)`

Sendet eine Nachricht an eine andere Anwendungskomponente (möglicherweise `app.py`) unter Verwendung der Socket-Programmierung. Diese Funktion umfasst die Netzwerkkommunikationslogik einschließlich Fehlerbehandlung.

### `main_loop()`

Die Kernfunktion, die in einer kontinuierlichen Schleife ausgeführt wird und die folgenden Aktionen ausführt:

1. Ruft Daten von einer externen API mit der `requests`-Bibliothek ab.
2. Überwacht Änderungen an den Daten, insbesondere nach Änderungen an einem `payment_hash`-Wert.
3. Wenn eine Änderung erkannt wird und bestimmte Bedingungen erfüllt sind (z. B. ein Betragsschwellenwert), löst sie eine Aktion aus, indem sie eine Nachricht an eine andere Komponente sendet.
4. Integriert Verzögerungsmechanismen zur Steuerung der Häufigkeit von API-Anfragen und nachfolgenden Aktionen.

## Ausführungsfluss

1. Initialisiert und startet die Hauptschleife in einem separaten Thread, um eine blockierende Ausführung sicherzustellen.
2. Überwacht kontinuierlich eine externe API auf Änderungen, wobei ein Hash-Wert als Indikator verwendet wird.
3. Kommuniziert über Sockets mit anderen Anwendungskomponenten, um Aktionen aufgrund erkannter Änderungen zu koordinieren.

## Ausführen des Moduls

Um `switch.py` auszuführen, geben Sie den folgenden Befehl in einem Terminal ein:

```bash
python switch.py
