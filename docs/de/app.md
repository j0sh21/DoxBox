
# Dokumentation für app.py
## Übersicht

`app.py` dient als zentrales Modul in der Anwendung, das die Benutzeroberfläche orchestriert und Benutzerinteraktionen erleichtert. Dieses Modul nutzt das leistungsstarke PyQt5-Framework, um eine robuste und reaktionsfähige grafische Benutzeroberfläche (GUI) zu erstellen, was es zu einem zentralen Element für Anwendungen macht, die Benutzerinteraktion über eine visuelle Schnittstelle erfordern.

## Zweck

Der Hauptzweck von `app.py` besteht darin, die Struktur und das Verhalten der GUI der Anwendung zu definieren. Es kapselt das Design und die Funktionalität verschiedener UI-Komponenten ein, einschließlich Fenster, Widgets, Layouts und Ereignisbehandlungen, und gewährleistet so eine nahtlose und intuitive Benutzererfahrung.

## Umfang

In `app.py` finden Sie Definitionen für Schlüsselklassen und -funktionen, die zusammen die Frontend der Anwendung aufbauen. Dazu gehören:

- **AppState**: Eine Klasse, die für die Verwaltung des Zustands der Anwendung konzipiert ist und dynamische Aktualisierungen und Interaktionen innerhalb der GUI ermöglicht. Sie verwendet ein `stateChanged`-Signal, um andere Teile der Anwendung zu benachrichtigen, wenn sich der Zustand ändert, was ein reaktives Design fördert, bei dem sich die UI basierend auf dem aktuellen Anwendungszustand anpassen kann.
- **VendingMachineDisplay**: Eine benutzerdefinierte `QWidget`-Unterklasse, die als Hauptcontainer für die UI-Elemente der Anwendung dient und diese in ein kohärentes und funktionales Layout organisiert.

## Zustandsverwaltung

Die `AppState`-Klasse steht im Zentrum der Zustandsverwaltung der Anwendung. Sie hält eine `state`-Variable, die den aktuellen Zustand oder Modus der Anwendung widerspiegelt. Änderungen an diesem Zustand werden über das `stateChanged`-Signal verbreitet, was es anderen Komponenten, insbesondere der UI, ermöglicht, entsprechend zu reagieren und sich zu aktualisieren. Dieser Ansatz entkoppelt die Zustandsverwaltung von der UI-Logik, was die Modularität und Wartbarkeit verbessert.

## Socket-Programmierung und Server-Client-Kommunikation

Die Anwendung verfügt über eine Serverkomponente, die auf eingehende Verbindungen hört, die mit Pythons `socket`-Bibliothek verwendet werden. Die Funktion `start_server` initialisiert diesen Server, der auf Nachrichten von Clients wartet. Nach Erhalt einer Nachricht verarbeitet die Funktion `handle_client_connection` diese und aktualisiert den `AppState`, indem sie das Zustandsverwaltungssystem nutzt, um Änderungen in der UI dynamisch widerzuspiegeln. Diese Server-Client-Konfiguration ermöglicht eine Fernsteuerung oder automatisierte Steuerung über die Anwendung, ideal für Kiosk- oder Verkaufsautomatenszenarien.

## Socket-Programmierung und Server-Client-Kommunikation

Die Anwendung verfügt über eine Serverkomponente, die auf eingehende Verbindungen mit Pythons `socket`-Bibliothek hört. Die Funktion `start_server` initialisiert diesen Server, der auf Nachrichten von Clients wartet. Bei Erhalt einer Nachricht verarbeitet die Funktion `handle_client_connection` diese und aktualisiert den `AppState`, wobei das Zustandsverwaltungssystem genutzt wird, um Änderungen in der Benutzeroberfläche dynamisch widerzuspiegeln. Diese Server-Client-Konfiguration ermöglicht eine Fern- o...

## Schlüsselmerkmale

- **Modulares Design**: `app.py` verfolgt einen modularen Ansatz, der die Zustandsverwaltung und die Darstellung der Benutzeroberfläche trennt, was die Wartbarkeit und Skalierbarkeit erleichtert.
- **Zustandsgesteuerte Benutzeroberfläche**: Die Benutzeroberfläche der Anwendung reagiert dynamisch auf Änderungen des Anwendungszustands und bietet ein reaktives Benutzererlebnis, das sich in Echtzeit aktualisiert, um den aktuellen Kontext und die Daten widerzuspiegeln.
- **Integration mit PyQt5**: Durch die Nutzung von PyQt5 nutzt `app.py` einen umfassenden Satz von Werkzeugen und Widgets zur Erstellung professioneller GUIs, einschließlich Unterstützung für Multimedia-Komponenten, Ereignisbehandlung und benutzerdefiniertes Widget-Styling.

## Abhängigkeiten

- **Qt Widgets**: Erbt von `QWidget` und kann andere Widgets wie `QLabel`, `QVBoxLayout`, `QHBoxLayout` von PyQt5.QtWidgets verwenden.
- **Qt Multimedia**: Kann möglicherweise `QCamera`, `QCameraViewfinder` von PyQt5.QtMultimedia und `QCameraViewfinder` von PyQt5.QtMultimediaWidgets für die Kameraintegration verwenden.
- **Qt Core**: Nutzt Klassen wie `QPixmap`, `QMovie` von PyQt5.QtGui und `Qt`, `QSize`, `QRect`, `QPoint` von PyQt5.QtCore für Kernfunktionalitäten der GUI.

## Multimedia-Verarbeitung und GIF-Animationen

Die Klasse `VendingMachineDisplay` beinhaltet fortgeschrittene Multimedia-Verarbeitungsfunktionen, insbesondere für das Abspielen und Verwalten von GIF-Animationen. Diese Funktionalität erhöht die visuelle Attraktivität der Anwendung und das Benutzerengagement, insbesondere bei interaktiven Kiosken oder Verkaufsautomaten-Schnittstellen.

### Abspielen von GIF-Animationen

Die Anwendung kann GIF-Animationen als Teil ihrer Benutzeroberfläche anzeigen und bietet damit dynamischen visuellen Inhalt. Dies wird durch die `QMovie`-Klasse von PyQt5 erreicht, die zum Laden und Abspielen von GIF-Dateien verwendet wird. Die Klasse `VendingMachineDisplay` beinhaltet Methoden, um ein GIF abzuspielen, dessen Dauer zu berechnen und sicherzustellen, dass es in die vorgesehenen Benutzeroberflächenelemente passt, was ein nahtloses Multimedia-Erlebnis bietet.

### Schlüsselmethoden

- **send_msg_to_LED(host, port, command)**: Diese Methode ermöglicht es der Anwendung, mit externen Geräten wie einem angeschlossenen LED-Streifen über ein Netzwerk zu kommunizieren. Es wird eine Socket-Verbindung zum angegebenen Host und Port hergestellt und dann ein Befehl gesendet, der verwendet werden könnte, um Nachrichten anzuzeigen oder den LED-Streifen zu steuern.
- **calculateDuration()**: Berechnet die Gesamtdauer einer GIF-Animation, indem sie durch ihre Frames iteriert. Diese Informationen können verwendet werden, um die Wiedergabe des GIFs mit anderen Ereignissen in der Anwendung zu synchronisieren und so ein kohärentes Benutzererlebnis zu gewährleisten.
- **handle_client_connection(client_socket, appState)**: Verarbeitet eingehende Verbindungen von Clients. Diese Funktion ist ein wesentlicher Teil der Server-Client-Architektur, liest Nachrichten, die von Clients gesendet wurden, aktualisiert den Anwendungszustand basierend auf diesen Nachrichten und stellt sicher, dass die Benutzeroberfläche diese Änderungen widerspiegelt.
- **start_server(appState)**: Initialisiert und startet den Server, der auf eingehende Verbindungen hört. Er bindet an einen bestimmten Port und wartet auf die Verbindung von Clients, wobei für jede Verbindung ein neuer Thread erstellt wird, sodass die Anwendung reibungslos weiterlaufen kann, während sie Clientanfragen verwaltet.


### GIF-Wiederholungslogik

Die GIF-Wiederholungslogik in der DoxBox ist darauf ausgelegt, die Wiedergabe von GIF-Animationen basierend auf dem aktuellen Zustand der Anwendung und der Dauer der GIFs zu verwalten. Diese Logik stellt sicher, dass kürzere GIFs eine festgelegte Anzahl von Malen wiederholt werden, um das Engagement der Benutzer aufrechtzuerhalten, während längere GIFs reibungslos zum nächsten Zustand oder GIF übergehen, wenn sie abgeschlossen sind. Im Folgenden finden Sie einen Überblick über die wichtigsten Komponenten und Funktionen der GIF-Wiederholungslogik.

#### Komponenten:

- Filmobjekt: Repräsentiert die abzuspielende GIF-Animation. Es ist verantwortlich für die Verwaltung der GIF-Wiedergabe.
- GIF-Label: Eine grafische UI-Komponente (Label), die die GIF-Animation anzeigt.
- Zustandsverwaltung: Die Anwendung behält einen Zustand bei, der den Kontext oder die Phase bestimmt, in der sie sich gerade befindet (z.B. Zahlung, Countdown, Lächeln).

#### Schlüsselattribute:

- `loopCount`: Verfolgt die Anzahl der Wiederholungen des aktuellen GIFs.
- `desiredLoops`: Die gewünschte Anzahl von Wiederholungen des GIFs, die je nach Dauer des GIFs variiert.
- `isreplay`: Ein Flag, das anzeigt, ob die aktuelle GIF-Wiedergabe eine Originalwiedergabe (0) oder eine Wiederholung (1) ist.
- `total_duration`: Die Gesamtdauer des aktuellen GIFs. Wird verwendet, um die Anzahl der gewünschten Schleifen für kürzere GIFs zu bestimmen.
- `gif_path`: Der Dateipfad des aktuell abzuspielenden GIFs.

#### Funktionen:

- `playGIF()`: Initiiert die Wiedergabe eines GIFs. Wenn `isreplay` 0 ist, setzt es `loopCount` und `desiredLoops` für ein neues GIF zurück. Wenn `isreplay` 1 ist, wird das aktuelle GIF ohne Zurücksetzen der Schleifenzählung erneut abgespielt.
- `updateGIF(state)`: Aktualisiert das aktuelle GIF basierend auf dem Zustand der Anwendung. Es wählt ein zufälliges GIF aus einem bestimmten Unterordner aus, der dem aktuellen Zustand entspricht, und richtet es für die Wiedergabe ein.
- `onGIFFinished()`: Wird ausgelöst, wenn ein GIF fertig abgespielt ist. Es verwaltet die Logik für das Wiederholen oder Übergehen von GIFs basierend auf ihrer Dauer und dem Zustand der Anwendung.

#### GIF-Dauer und Wiederholungszeiten:

- Dauer < 0,6 Sekunden: Für GIFs, die kürzer als 0,6 Sekunden sind, wird die gewünschte Anzahl von Wiederholungen (`desiredLoops`) auf 6 Mal festgelegt. Dies stellt sicher, dass sehr kurze GIFs ausreichend oft abgespielt werden, um für den Benutzer erkennbar und ansprechend zu sein.
- Dauer zwischen 0,6 und 1,6 Sekunden: Für GIFs mit einer Dauer zwischen 0,6 Sekunden und 1,6 Sekunden wird das GIF 3 Mal wiederholt. Dieser Dauerbereich umfasst mäßig kurze GIFs, die weniger Wiederholungen benötigen, um das Engagement der Benutzer aufrechtzuerhalten.
- Dauer zwischen 1,6 und 3,3 Sekunden: GIFs, die in diesen Dauerbereich fallen, werden 2 Mal wiederholt. Diese werden als kurz, aber nicht so kurz angesehen, dass sie viele Wiederholungen benötigen, um wirksam zu sein.

#### Logikablauf mit spezifischen Dauern:

- Erstmalige Wiedergabe: Bei der Auswahl eines neuen GIFs wird `playGIF()` mit `isreplay` auf 0 aufgerufen. Dies initialisiert die Wiedergabe, indem `loopCount` auf 0 und `desiredLoops` auf 1 gesetzt wird.
- Bestimmung des Wiederholungsbedarfs: Wenn ein GIF abgeschlossen ist (`onGIFFinished()`), überprüft die Logik die Gesamtdauer (`total_duration`) des GIFs und den aktuellen Anwendungszustand. Wenn der Zustand nicht "2" oder "3" ist und die Dauer des GIFs weniger als 3,3 Sekunden beträgt, wird die Anzahl der Wiederholungen basierend auf den oben genannten spezifischen Dauerbereichen bestimmt.
- Ausführung der Wiederholung: Erfüllt das GIF die Kriterien für eine Wiederholung, wird `isreplay` auf 1 gesetzt und `playGIF()` erneut aufgerufen. Dies erhöht `loopCount` jedes Mal, wenn das GIF eine Schleife abschließt. Die Wiederholung wird fortgesetzt, bis `loopCount` `desiredLoops` erreicht.
- Übergang oder Aktualisierung: Nachdem die gewünschte Anzahl von Wiederholungen abgeschlossen ist oder wenn das GIF die Wiederholungskriterien nicht erfüllt (entweder aufgrund seiner Dauer, die länger als 3,3 Sekunden ist, oder des Anwendungszustands), wechselt die Anwendung entweder in einen neuen Zustand oder wählt basierend auf dem aktuellen Zustand ein neues GIF aus.


## Von app.py verarbeitete Nachrichten

Die Anwendung verwendet numerische Zeichenketten als Nachrichten, um verschiedene Zustände und Aktionen innerhalb der Anwendung darzustellen. Jede Nachricht löst spezifische Verhaltensweisen aus, die mit verschiedenen Funktionen oder visuellem Feedback durch die GUI korrelieren. Unten ist eine Tabelle, die die numerischen Nachrichten und ihre entsprechenden Auswirkungen innerhalb der Anwendung zusammenfasst:

**Zustandsnachrichten**:

| Nachricht | Beschreibung                                                                |
|-----------|-----------------------------------------------------------------------------|
| "0"       | stellt einen anfänglichen oder Willkommenszustand dar.                      |
| "1"       | zeigt eine abgeschlossene Zahlung oder Transaktion an.                      |
| "2"       | Startet den Countdown, Vorbereitungsphase nach einer Zahlung.               |
| "3"       | bedeutet den Abschluss eines Countdowns, Übergang zur Fotoaufnahme.         |
| "4"       | Foto erfolgreich aufgenommen, Beginn des Druckvorgangs.                     |
| "5"       | Druck abgeschlossen: "Danke" oder Abschlusszustand, Ende einer Transaktion. |
| "144"     | Unterbezahlt                                                                |
| "204"     | Bild wurde nach dem Drucken erfolgreich gelöscht.                           |


**Fehlermeldungen**:

| Nachricht | Beschreibung                                  |
|-----------|-----------------------------------------------|
| "100"     | Allgemeiner Fehler in app.py.                 |
| "101"     | Kamera hat keinen Fokus gefunden              |
| "102"     | Keine Kamera gefunden                         |
| "103"     | Datei nicht gefunden                          |
| "104"     | Zugriff verweigert                            |
| "110"     | Allgemeiner Fehler in print.py                |
| "112"     | Drucker nicht gefunden                        |
| "113"     | Datei nicht gefunden                          |
| "114"     | Zugriff verweigert                            |
| "115"     | Fehler beim Kopieren der Datei                |
| "116"     | Druckauftrag angehalten oder abgebrochen.     |
| "119"     | Fehler beim Erstellen des Druckauftrags       |
| "120"     | Allgemeiner Fehler in img_capture.py          |
| "130"     | Allgemeiner Fehler in led.py                  |
| "140"     | Unerwarteter Fehler in switch.py              |
| "141"     | LNbits API-Antwortstatuscode ist nicht 200    |
| "142"     | Verbindungsfehler mit LNbits API              |
| "143"     | Anfänglicher Verbindungsfehler mit LNbits API |


Diese Nachrichten werden von der Anwendung verarbeitet, um den `AppState` und damit auch die Benutzeroberfläche und alle externen Anzeigen, die mit der Anwendung verbunden sind, zu aktualisieren. Die spezifischen Aktionen, die als Reaktion auf jede Nachricht unternommen werden, können je nach aktuellem Anwendungskontext und beabsichtigtem Arbeitsablauf variieren.

## Nutzung

Entwickler, die mit `app.py` arbeiten, können mit hochgradigen Abstraktionen für UI-Komponenten, unkomplizierten Mechanismen für die Zustandsverwaltung und ereignisgesteuerten Programmiermustern interagieren. Dieses Modul wird üblicherweise als Teil des Anwendungsstartprozesses aufgerufen, initialisiert die GUI und bindet sie an die zugrunde liegende Logik und Datenmodelle.


# Dokumentation zur AppState-Klasse

## Übersicht

Die `AppState`-Klasse, definiert in `app.py`, ist eine grundlegende Komponente, die für die Verwaltung des Zustands der Anwendung und die Ermöglichung der Kommunikation zwischen Komponenten in einer auf Qt basierenden GUI-Anwendung konzipiert wurde. Sie erbt von `QObject`, um den Signal-Slot-Mechanismus von Qt zu nutzen, was sie für Anwendungen geeignet macht, die dynamische Reaktionen auf Zustandsänderungen erfordern.

## Merkmale

- **Zustandsverwaltung**: Zentralisiert die Verwaltung des Zustands der Anwendung und bietet eine einzige Quelle der Wahrheit für die zustandsbezogene Logik.
- **Signalübertragung**: Verwendet den Signalmechanismus von Qt (`pyqtSignal`), um Ereignisse auszusenden, wenn sich der Zustand der Anwendung ändert, sodass andere Komponenten auf diese Änderungen in entkoppelter Weise reagieren können.

## Klassendefinition

### Eigenschaften

- `state`: Eine Eigenschaft, die den aktuellen Zustand der Anwendung kapselt. Der Zugriff auf diese Eigenschaft wird durch einen Getter und einen Setter kontrolliert, um sicherzustellen, dass Zustandsänderungen konsistent verwaltet werden.

### Signale

- `stateChanged(str)`: Ein Signal, das immer dann ausgesendet wird, wenn sich der Zustand ändert, und den neuen Zustandswert als Zeichenkette trägt. Dieses Signal kann mit Slots oder Funktionen innerhalb anderer Komponenten verbunden werden, sodass sie auf Zustandsänderungen reagieren können.

## Nutzung

Die `AppState`-Klasse wird in der Regel einmal instanziiert und im gesamten Anwendungsverlauf verwendet, um den Zustand der Anwendung zu verwalten und zu beobachten. Komponenten, die auf Zustandsänderungen reagieren müssen, können ihre Slots oder Funktionen mit dem `stateChanged`-Signal verbinden.

### Beispiel

```python
# Instanziierung
app_state = AppState()

# Verbindung einer Funktion mit dem stateChanged-Signal
def on_state_changed(new_state):
    print(f"Der Zustand der Anwendung hat sich geändert zu: {new_state}")

app_state.stateChanged.connect(on_state_changed)

# Aktualisierung des Zustands
app_state.state = "1"  # Dies wird das stateChanged-Signal auslösen und on_state_changed aufrufen
```


# Dokumentation zur VendingMachineDisplay-Klasse

## Übersicht

Die `VendingMachineDisplay`-Klasse, definiert in `app.py`, ist eine entscheidende Komponente der grafischen Benutzeroberfläche (GUI) der Anwendung. Sie erbt von `QWidget`, was sie zu einem vielseitigen Behälter für verschiedene UI-Elemente macht. Diese Klasse ist hauptsächlich verantwortlich für den Aufbau und die Verwaltung des Layouts, der Steuerelemente und anderer visueller Elemente, die die Benutzeroberfläche der Anwendung ausmachen.

## Abhängigkeiten

- **Qt Widgets**: Erbt von `QWidget` und kann andere Widgets wie `QLabel`, `QVBoxLayout`, `QHBoxLayout` von PyQt5.QtWidgets verwenden.
- **Qt Multimedia**: Kann möglicherweise `QCamera`, `QCameraViewfinder` von PyQt5.QtMultimedia und `QCameraViewfinder` von PyQt5.QtMultimediaWidgets für die Kameraintegration verwenden.
- **Qt Core**: Nutzt Klassen wie `QPixmap`, `QMovie` von PyQt5.QtGui und `Qt`, `QSize`, `QRect`, `QPoint` von PyQt5.QtCore für Kernfunktionalitäten der GUI.

## Merkmale

- **Layoutverwaltung**: Verwaltet die Anordnung von UI-Elementen mit Layouts (z. B. `QVBoxLayout`, `QHBoxLayout`), um eine ansprechende und organisierte Anzeige zu gewährleisten.
- **Zustandsintegration**: Integriert sich mit der `AppState`-Klasse, um den Zustand der Anwendung basierend auf Benutzerinteraktionen oder anderen Ereignissen zu reflektieren und möglicherweise zu modifizieren.
- **Multimedia-Unterstützung**: Wenn Kamerafunktionalität verwendet wird, kann sie Funktionen wie die Anzeige eines Live-Kamerabilds umfassen, unter Verwendung von `QCamera` und `QCameraViewfinder`.

## Klassendefinition

### Konstruktor

- `__init__(self, appState)`: Initialisiert eine neue Instanz der `VendingMachineDisplay`-Klasse, wobei ein `AppState`-Objekt als Argument übergeben wird, um die Zustandsverwaltung und Interaktion zu erleichtern.

### Schlüsselmethoden

- Die Klasse beinhaltet Methoden zur Initialisierung von UI-Komponenten, zum Aufbau von Layouts und zum Verbinden von Signalen mit Slots für die Ereignisbehandlung (z. B. Tastenklicks, Zustandsänderungen).

## Nutzung

Die `VendingMachineDisplay`-Klasse wird als Teil des GUI-Einrichtungsprozesses der Anwendung instanziiert, oft im Hauptskript oder einem dedizierten GUI-Modul. Sie erfordert eine `AppState`-Instanz, um zustandsbasierte UI-Aktualisierungen und Interaktionen zu ermöglichen.

### Beispiel

```python
app = QApplication(sys.argv)
app_state = AppState()
vending_machine_display = VendingMachineDisplay(app_state)
vending_machine_display.show()
sys.exit(app.exec_())
```
