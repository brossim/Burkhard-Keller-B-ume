# Burkhard-Keller-Bäume zur approximativen Suche



## Modulprojekt Programmierung II

Das vorliegende Projekt implementiert die Burkhard-Keller-Bäume Datenstruktur anhand einer Model-View-Controller Klassenarchitektur. Aufgrund ihrer inhärenten Eigenschaften eignen sich BK-Bäume, gegeben ein Suchelement als Wort und einer maximalen String Distanz, zur effizenten Suche von ähnlichen Wörtern. Sie findet hauptsächlich Anwendung in der Rechtschreibprüfung sowie in der Generierung von Wortvorschlägen.

## 1. Struktur & Bestandteile

```
modulprojekt_pro2.
+---src
|   +---controller
|   |   \---__init__.py
|   |   \---bk_controller.py
|   +---model
|   |   \---__init__.py
|   |   \---bk_tree.py
|   |   +---metrics
|   |   |   \---metrics.py
|   |   |   \---test_metrics.py
|   +---view
|   |   \---__init__.py
|   |   \---bk_view.py
\---main.py 
\---demo_list.txt
\---README.md
\---requirements.txt
```

### 1.1 Ordner 'src'

Enthält das dreiteilige Architekturmuster: Model View, Controller (MVC)

|  Unterordner | Kurzbeschreibung  |
|---|---|
| model  |  Stellt die zentrale Logik des Burkhard-Keller-Baumes dar und beinhaltet die Metriken Levensthein und LSC-Distanz zur Abstandsberechnung (im Ordner 'metrics') sowie deren Unittests (ebd.).    |
| controller  |  Fungiert als Mittler zwischen Model und View, um die Datenverarbeitung des Models von den Benutzer Aus- und Eingaben in der View zu trennen.  |
|  view |  Dient zur Darstellung der Ergebnisse, die das Model ausgibt, und nimmt den User-Input entgegen.|

### 1.2 main.py

Das Hauptprogramm stellt die Kommandozeilenschnittstelle bereit (siehe 2.3) und steuert den Programmablauf. In ihm bündeln sich die einzelnen MVC-Komponenten.

### 1.3 demo_list.txt

Siehe 2.4

### 1.4 requirements.txt

Siehe 2.2

## 2. Installation & Anwendung

### 2.1 Download

Das Projekt kann entweder als lokale Kopie des Repositories geclont oder als komprimierter Ordner (.zip o.ä) über den Download-Button heruntergeladen werden. 

Zum Clonen wird folgender Befehl benutzt: 

```
$ git clone https://gitup.uni-potsdam.de/bross/modulprojekt_pro2.git
```

Es ist zu beachten, dass die ursprüngliche Ordner- und Dateistruktur beibehalten werden muss, um einen fehlerfreien Programmablauf zu gewährleisten.

### 2.2 Installation notwendiger Packages

Alle benötigten packages sind in 'requirements.txt' gelistet und können mithilfe des package installers 'pip' ausgehend vom Projektstammverzeichnis in eine Conda-Umgebung installiert werden:

```
$ pip install -r requirements.txt
```

Falls es während der grafischen Visualisierung der Baumstruktur durch die view zu einer Fehlermeldung bezüglich 'dot' kommen sollte ("dot" not found in path), muss zusätzlich folgender Befehl in der Conda-Umgebung ausgeführt werden: 

```
$ conda install -c anaconda graphviz
```

### 2.3 Programmaufruf mithilfe der Kommandozeilenschnittstelle 

Die Kommandozeilenschnittstelle verfügt über vier Optionen:

```
$ python main.py -pkl "path_to_.pkl_file" -p "path_to_txt_file" -m "string_metric" --vis/-no-vis 
```

**1. Option -pkl/--pickle**: Mit dieser Option lässt sich eine als .pkl abgespeicherte BKTree-Instanz deserialisieren, um sie grafisch darzustellen und im interaktiven Modus Suchen im Baum durchzuführen. Es muss ein valider Pfad zu einer .pkl-Datei übergeben werden. Falls diese Option ausgewählt ist, werden jedwede Eingaben bei den Optionen '-p/--path' und '-m/--metric' ignoriert. 

**2. Option -p/--path**: 'path' muss einen validen Dateipfad zu einer Textdatei bereitstellen, aus der ein neuer Baum erzeugt wird. In der Datei darf jede Zeile nur aus einem Wort bestehen. 

**3. Option -m/--metric**: Die Angabe von 'metric' ist optional bei der Erstellung eines neuen Baumes aus einer txt-Datei, weil standardmäßig mit der Levenshtein-Distanz gerechnet wird. Mögliche Argumente sind hier "levenshtein" und "lsc_distance". 

**4. Option --vis/-no-vis**: Dieser boolean Flag legt fest, ob eine grafische Visualisierung des Baumes erstellt wird (siehe Demo-Anwendung). Standardmäßig ist "--vis" eingestellt, d.h. der Flag kann ausgelassen werden, wenn eine Visualisierung erwünscht ist.  


### 2.4 Demo-Anwendung

Im Projektstammverzeichnis befindet sich eine Demowortliste ('demo_list.txt'), die zur Demonstration des Programmes genutzt werden kann. Sie beinhaltet 30 englische Wörter, die mit 'demo' beginnen. Es bietet sich an, falsch geschriebene Strings, die mit 'demo' anfangen, als Suchwort einzugeben (bpsw. 'democrazy', bzw. je nach Wort als Wurzelknoten). 

**Zur Bedienung des Matplotlib Plotting-Fensters (öffnet sich während des Programmes, wenn eine sofortige grafische Visualisierung erwünscht ist):**

1. Navigation/Zooming im Baum (v.a. wenn Knoten überlappen) ![The Pan/Zoom button](https://matplotlib.org/3.2.2/_images/move_large.png)

    "This button has two modes: pan and zoom. Click the toolbar button to activate panning and zooming, then put  your mouse somewhere over an axes. Press the left mouse button and hold it to pan the figure, dragging it to a new position. When you release it, the data under the point where you pressed will be moved to the point where you released. Press the right mouse button to zoom, dragging it to a new position. The x axis will be zoomed in proportionately to the rightward movement and zoomed out proportionately to the leftward movement."

2. Speicherung des Baums ![Save Button](https://matplotlib.org/3.2.2/_images/filesave_large.png)

    "Click this button to launch a file save dialog. You can save files with the following extensions: png, ps, eps, svg and pdf."
    
    Speichern im PDF-Format bietet die beste Qualität/Zoomeigenschaften. 

**Zur Starten einer Demo-Anwedung können folgende Befehle genutzt werden:**

```
 
1. $ python main.py -p "demo_list.txt"
    --> Baut Baum mit der Levenshtein-Distanz auf (Standardmetrik) und öffnet ein neues Fenster mit der grafischen Visualisierung. 

 2. $ python main.py -p "demo_list.txt" -m "lsc_distance"
    --> Das gleiche mit der LSC-Distanz

 3. $ python main.py -p "demo_list.txt" --no-vis
     --> Wie 1., nur ohne grafische Visualisierung in einem neuen Fenster 

 4. $ python main.py -p "demo_list.txt" -m "lsc_distance" --no-vis
     --> Wie 2., nur ohne grafische Visualisierung in einem neuen Fenster
```

### Beispiel-Output im Terminal mit grafischer Visualisierung

![BKTree_Vis](https://i.im.ge/2022/09/05/O87m0P.bk-plot.png)

### Beispiel: Interaktiver Modus 

```
(base) PS C:\Users\bross\anaconda3\envs\modulprojekt_pro2> python main.py -p ".\demo_list.txt"

The BK-Tree is being instantiated with a word list of 60 words.
It may take a few moments if a large (~200k) word list was provided.


-----------------------------------
Burkhard Keller Tree Specifications
-----------------------------------
Root Word           : demonizes
Number of Words     : 60
Maximum Tree Depth  : 4



The BK-Tree is being plotted. Depending on the tree size, this may take a few moments.

Interactive Mode has started.
Exit by entering a blank line (Press Enter without input)

Enter query word: demonizer
Enter distance as integer: 2
Search Result(s): demonizes, demonized, demonised, demonises

Enter query word:

The programm was closed.
```

### 2.5 Python-Version
Für das gesamte Projekt wurde **Python 3.9** verwendet. 

### 2.6 Daten
Als Datengrundlage für das Programm wurde die Wortliste aus dem nltk.corpus Package verwendet (235.892 Wörter nach Eliminierung von doppelten Wörtern, dies geschieht automatisch innerhalb des models).

**Datenbeschaffung in python:** 

1. Package-Import

```
from nltk.corpus import words
```

2. Wortliste definieren

```
word_list = words.words()
```

### 2.7 Unittests 

Die Unittests für die Abstandsberechnnung zwischen zwei Strings befinden sich im Ordner **src/model/metrics**, unter dem Dateinamen **'test_metrics.py'**.
Zur Ausführung im Terminal wird in den Projektunterordner  **src/model/metrics** navigiert und der Befehl ```pytest test_metrics.py``` ausgeführt (pytest Installation erforderlich, in 'requirements.txt' enthalten)

Alternativ kann 'test_metrics.py' auch in einer IDE geöffnet (bspw. PyCharm) und dort mit einer Python tests configuration ausgeführt werden. 
