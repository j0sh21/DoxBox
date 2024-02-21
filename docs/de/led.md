
# Dokumentation für led.py

Willkommen beim DoxBox LED-Controller-Modul! Dieses Dokument soll Ihnen helfen, die LED-Lichteffekte in Ihre DoxBox-Fotokabine zu integrieren und das Benutzererlebnis während der Bezahlung, Fotografie und anderer Interaktionen zu verbessern.

## Erste Schritte

Die Klasse `RGBLEDController` in diesem Modul steuert RGB-LEDs, um ansprechende visuelle Effekte zu erzeugen. Egal, ob Sie während des Fotografierens eine Atmosphäre schaffen oder visuelle Hinweise während der Bezahlung geben möchten, dieses Modul bietet eine Vielzahl von Animationen wie Atmen, Blinken und Überblenden.

### Voraussetzungen

Stellen Sie sicher, dass Sie Folgendes haben:
- Ein Raspberry Pi-Setup mit angeschlossenen RGB-LEDs an den angegebenen GPIO-Pins.
- Grundkenntnisse in Python-Programmierung und GPIO-Pin-Konfiguration.

## Kernkomponenten

### RGBLEDController

Dies ist das Herzstück des LED-Steuerungssystems. Es verwaltet die Farben und Animationen der LEDs, die an Ihrem Raspberry Pi angeschlossen sind.

#### Initialisierung

Initialisiert den Controller mit den GPIO-Pins, die an Ihre RGB-LEDs angeschlossen sind. `steps` und `brightness_steps` ermöglichen es Ihnen, die Feinheit der Animationen zu steuern.

#### Animationen konfigurieren

- `set_fade_speed(self, speed)`: Passt an, wie schnell die LEDs zwischen Farben überblenden.
- `set_breath_speed(self, speed)`: Legt das Tempo des Atemeffekts fest, bei dem LEDs allmählich heller und dunkler werden.
- `set_blink_times(self, on_time, off_time)`: Konfiguriert die Dauer der Blinkanimation für das Ein- und Ausschalten der LEDs.

#### Animationen verwalten

- `set_loop(self, animation_type)`: Wählt den Typ der Animation aus (z.B. "atmen", "blinken", "überblenden").
- `activate_loop()`: Startet die ausgewählte Animationssequenz. Achtung: Diese Funktion wird bereits in set_loop() aufgerufen.
- `interrupt_current_animation(self)`: Stoppt jede laufende Animation, nützlich für sofortiges Benutzerfeedback.

#### Direkte LED-Steuerung

- `set_color(self, r, g, b)`: Stellt die LEDs direkt auf die angegebene RGB-Farbe ein.
- `update_leds(self)`: Aktualisiert die LEDs basierend auf den aktuellen Einstellungen oder Animationen.

### ServerThread

Für fortgeschrittene Setups ermöglicht die Klasse `ServerThread`, dass der DoxBox LED-Controller externe Befehle (z.B. von `app.py`) empfängt, um LED-Effekte dynamisch zu ändern.

#### Server einrichten

- `__init__(self, host, port, led_controller)`: Bereitet den Server mit Netzwerkdetails vor und verbindet ihn mit dem RGBLEDController.
- `run(self)`: Startet den Server und macht den DoxBox für externe LED-Steuerungsbefehle empfänglich.


## Nachrichtenverarbeitung

**`led.py` führt spezifische Aktionen durch, wenn ein Befehl per Nachricht gesendet wird:**


| Befehl                           | Aktion                                                                            |
|-----------------------------------|-----------------------------------------------------------------------------------|
| "color 0 255 0"                   | stellt Farbe auf Blau ein                                                         |
| "brightness 200"                  | stellt Helligkeit auf 200 ein. Bereich 0 - 255                                    |
| "fadespeed 0.8"                   | stellt Überblendgeschwindigkeit auf 0.8 ein                                       |
| "fade 1"                          | startet Überblenden                                                               |
| "blinkspeed 0.5 0.5"              | Einstellung der Ein- und Ausschaltzeit in Sekunden für den Blinkeffekt            |
| "blink 1"                         | startet Blinken unbegrenzte Male                                                  |
| "blink 10"                        | startet Blinken 10 Mal                                                            |
| "breathbrightness 0.2 0.8"        | Einstellung des Helligkeitsbereichs für den Atemeffekt auf 20% bis 80% Helligkeit |
| "breathspeed 0.5"                 | Einstellung der breath Geschwindigkeit auf 0.5                 |
| "breath 1"                        | startet Atmen unbegrenzt                                                          |
| "breath 5"                        | startet Atmen 5 Mal                                                               |
| "interrupt"                       | unterbricht die aktuelle Animationssequenz                                        |
| "fade 0", "breath 0" oder "blink 0" | stoppt die gegebene Animationssequenz                                             |

## Beispiel zur Integration

Hier ist ein einfaches Beispiel, um LED-Effekte in Ihre DoxBox zu integrieren:

```python
from led_controller import RGBLEDController, ServerThread

# Initialisieren des LED-Controllers mit GPIO-Pins
led_controller = RGBLEDController(red_pin=17, green_pin=27, blue_pin=22)

# Optional: Starten eines Servers für externe Befehle
server = ServerThread(host='0.0.0.0', port=12345, led_controller=led_controller)
server.run()

# Einrichten eines Atemeffekts für den Fotografieprozess
led_controller.set_loop('breath')
led_controller.activate_loop()
```

## Tipps für ein großartiges Benutzererlebnis

- Verwenden Sie sanfte, langsame Atemeffekte in Ruhezeiten, um eine einladende Atmosphäre zu schaffen.
- Helle, schnelle Blitze können den Beginn der Fotoaufnahme oder eine erfolgreiche Bezahlung signalisieren.
- Berücksichtigen Sie Farbthemen, die zu Ihrer DoxBox-Marke oder dem Event-Thema passen.

## Fehlerbehebung

- LEDs reagieren nicht: Überprüfen Sie Ihre GPIO-Verbindungen und stellen Sie sicher, dass Ihr Raspberry Pi die richtige Pin-Konfiguration hat.
- Animationen ändern sich nicht: Stellen Sie sicher, dass `interrupt_current_animation` aufgerufen wird, bevor Sie die Animationen wechseln.
