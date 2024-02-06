# Dokumentation für app.py
# Übersicht

`app.py` dient als zentrales Modul in der Anwendung, das die Benutzeroberfläche orchestriert und Benutzerinteraktionen erleichtert. Dieses Modul nutzt das leistungsstarke PyQt5-Framework, um eine robuste und reaktionsschnelle grafische Benutzeroberfläche (GUI) aufzubauen, was es zu einem zentralen Element für Anwendungen macht, die Benutzerinteraktion über eine visuelle Schnittstelle erfordern.

## Zweck

Der Hauptzweck von `app.py` ist es, die Struktur und das Verhalten der GUI der Anwendung zu definieren. Es kapselt das Design und die Funktionalität verschiedener UI-Komponenten ein, einschließlich Fenstern, Widgets, Layouts und Ereignisbehandlern, um eine nahtlose und intuitive Benutzererfahrung zu gewährleisten.

## Umfang

Innerhalb von `app.py` finden Sie Definitionen für Schlüsselklassen und -funktionen, die gemeinsam die Frontend der Anwendung aufbauen. Dazu gehören:

- **AppState**: Eine Klasse, die für die Verwaltung des Zustands der Anwendung konzipiert ist, was dynamische Aktualisierungen und Interaktionen innerhalb der GUI ermöglicht.
- **VendingMachineDisplay**: Eine benutzerdefinierte Unterklasse von `QWidget`, die als Hauptcontainer für die UI-Elemente der Anwendung dient und diese in einem kohärenten und funktionalen Layout organisiert.

## Schlüsselfunktionen

- **Modulares Design**: `app.py` folgt einem modularen Ansatz, der Zustandsmanagement und UI-Präsentation trennt, was Wartbarkeit und Skalierbarkeit erleichtert.
- **Zustandsgesteuerte UI**: Die UI der Anwendung reagiert dynamisch auf Änderungen im Anwendungszustand und bietet eine reaktive Benutzererfahrung, die in Echtzeit aktualisiert wird, um den aktuellen Kontext und die Daten widerzuspiegeln.
- **Integration mit PyQt5**: Durch die Nutzung von PyQt5 nutzt `app.py` einen umfassenden Satz von Tools und Widgets für die Erstellung professioneller GUIs, einschließlich Unterstützung für Multimedia-Komponenten, Ereignisbehandlung und benutzerdefinierte Widget-Styling.

## Nutzung

Entwickler, die mit `app.py` arbeiten, können mit hochrangigen Abstraktionen für UI-Komponenten, unkomplizierten Mechanismen für das Zustandsmanagement und ereignisgesteuerten Programmiermustern rechnen. Dieses Modul wird in der Regel als Teil des Startprozesses der Anwendung aufgerufen, initialisiert die GUI und bindet sie an die zugrunde liegende Logik und Datenmodelle.

## Stati

Eine Übersicht über die verwendeten Stati:

```python
    subfolder_map = {
            "0": "0_welcome",
            "1": "1_payment",
            "2": "2_countdown",
            "3": "3_smile",
            "4": "4_print",
            "5": "5_thx",
            "100": "100_error"
        }
```

# AppState Klassendokumentation

## Übersicht

Die `AppState`-Klasse, definiert innerhalb von `app.py`, ist eine fundamentale Komponente, die für die Verwaltung des Zustands der Anwendung konzipiert ist und die interkomponenten Kommunikation in einer auf Qt basierenden GUI-Anwendung ermöglicht. Sie erbt von `QObject`, um den Signal-Slot-Mechanismus von Qt zu nutzen, was sie für Anwendungen geeignet macht, die dynamische Reaktionen auf Zustandsänderungen erfordern.

## Abhängigkeiten

- **Qt-Module**: `QObject`, `pyqtSignal` aus PyQt5.QtCore

## Funktionen

- **Zustandsmanagement**: Zentralisiert die Verwaltung des Zustands der Anwendung und bietet eine einzige Quelle der Wahrheit für die zustandsbezogene Logik.
- **Signalausgabe**: Verwendet den Signalmechanismus von Qt (`pyqtSignal`), um Ereignisse auszugeben, wenn sich der Zustand der Anwendung ändert, sodass andere Komponenten auf diese Änderungen in einer entkoppelten Weise reagieren können.

## Klassendefinition

### Eigenschaften

- `state`: Eine Eigenschaft, die den aktuellen Zustand der Anwendung kapselt. Der Zugriff auf diese Eigenschaft wird durch einen Getter und einen Setter kontrolliert, um sicherzustellen, dass Zustandsänderungen konsistent verwaltet werden.

### Signale

- `stateChanged(str)`: Ein Signal, das immer dann ausgesendet wird, wenn sich der Zustand ändert, und den neuen Zustandswert als Zeichenkette mitführt. Dieses Signal kann mit Slots oder Funktionen innerhalb anderer Komponenten verbunden werden, um ihnen zu ermöglichen, auf Zustandsänderungen zu reagieren.

## Nutzung

Die `AppState`-Klasse wird in der Regel einmal instanziiert und im gesamten Verlauf der Anwendung verwendet, um den Zustand der Anwendung zu verwalten und zu beobachten. Komponenten, die auf Zustandsänderungen reagieren müssen, können ihre Slots oder Funktionen mit dem `stateChanged`-Signal verbinden.

### Beispiel

```python
# Instanziierung
app_state = AppState()

# Eine Funktion mit dem stateChanged-Signal verbinden
def on_state_changed(new_state):
    print(f"Der Anwendungszustand hat sich geändert zu: {new_state}")

app_state.stateChanged.connect(on_state_changed)

# Den Zustand aktualisieren
app_state.state = "1"  # Dies wird das stateChanged-Signal auslösen und on_state_changed aufrufen
```
## Überlegungen

Die AppState-Klasse ist darauf ausgelegt, in eine auf Qt basierende Anwendung integriert zu werden. Stellen Sie sicher, dass die Qt-Ereignisschleife läuft, um die Signal-Slot-Kommunikation zu ermöglichen.
Die Klasse verwaltet derzeit einen einfachen zeichenkettenbasierten Zustand. Abhängig von der Komplexität der Anwendung könnten Sie in Erwägung ziehen, diese Klasse zu erweitern oder ausgefeiltere Techniken für das Zustandsmanagement zu verwenden.
# VendingMachineDisplay Klassendokumentation
## Übersicht

Die `VendingMachineDisplay`-Klasse, definiert innerhalb von `app.py`, ist ein entscheidendes Element der grafischen Benutzeroberfläche (GUI) der Anwendung. Sie erbt von QWidget und ist somit ein vielseitiger Container für verschiedene UI-Elemente. Diese Klasse ist hauptsächlich dafür verantwortlich, das Layout, die Steuerelemente und andere visuelle Elemente zu konstruieren und zu verwalten, die die Benutzeroberfläche der Anwendung ausmachen.
Abhängigkeiten

- `Qt-Widgets`: Erbt von `QWidget` und kann andere Widgets wie QLabel, QVBoxLayout, QHBoxLayout aus PyQt5.QtWidgets verwenden.
- `Qt-Multimedia`: Kann QCamera, QCameraViewfinder aus PyQt5.QtMultimedia und QCameraViewfinder aus PyQt5.QtMultimediaWidgets für die Kameraintegration verwenden.
- `Qt-Core`: Nutzt Klassen wie QPixmap, QMovie aus PyQt5.QtGui und Qt, QSize, QRect, QPoint aus PyQt5.QtCore für grundlegende GUI-Funktionalitäten.

Funktionen

1. Layoutmanagement: Verwaltet die Anordnung von UI-Elementen mithilfe von Layouts (z.B. QVBoxLayout, QHBoxLayout), um eine reaktionsfähige und organisierte Anzeige zu gewährleisten.
2. Zustandsintegration: Integriert sich mit der AppState-Klasse, um den Zustand der Anwendung auf der Grundlage von Benutzerinteraktionen oder anderen Ereignissen widerzuspiegeln und möglicherweise zu ändern.
3. Multimediaunterstützung: Falls Kamerafunktionalität verwendet wird, kann sie Funktionen wie die Anzeige eines Live-Kamera-Feeds umfassen und QCamera und QCameraViewfinder nutzen.

## Klassendefinition
### Konstruktor`__init__(self, appState)`: 
 Initialisiert eine neue Instanz der VendingMachineDisplay-Klasse und nimmt ein AppState-Objekt als Argument, um das Zustandsmanagement und die Interaktion zu erleichtern.

## Wichtige Methoden

Die Klasse umfasst Methoden zum Initialisieren von UI-Komponenten, Einrichten von Layouts und Verbinden von Signalen mit Slots für die Ereignisbehandlung (z.B. Klicks auf Schaltflächen, Zustandsänderungen).

# Nutzung

Die VendingMachineDisplay-Klasse wird als Teil des GUI-Einrichtungsprozesses der Anwendung instanziiert, oft im Hauptskript oder einem dedizierten GUI-Modul. Sie erfordert eine AppState-Instanz, um zustandsbasierte UI-Updates und -Interaktionen zu ermöglichen.
Beispiel

```python

app = QApplication(sys.argv)
app_state = AppState()
vending_machine_display = VendingMachineDisplay(app_state)
vending_machine_display.show()
sys.exit(app.exec_())
```
# Überlegungen

Stellen Sie sicher, dass das AppState-Objekt ordnungsgemäß initialisiert und an den VendingMachineDisplay-Konstruktor übergeben wird, um zustandsbasierte Funktionalität zu ermöglichen.
