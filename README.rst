
.. image:: logo.png


Python Project *GeolocationUpdate*
-----------------------------------------------------------------------


Introduction
------------

To import the project simply type

.. code-block:: python

    >>> import GeolocationUpdate

after installation.


Install
-------

The latest stable version can always be installed or updated via pip:

.. code-block:: bash

    $ pip install GeolocationUpdate

Einleitung
----------
Mit Hilfe dieses Packages soll es einem User möglich sein, auf Grund seiner aktuellen Position und speziellen weiteren Angaben
den exakten Weg auf welchem sich der User befindet und die dazugehörige Geschwindigkeit des Weges zurückzugeben. Dafür sollte zunächst an einer Idee
für einen Algorithmus geschrieben werden, welcher ein mathematisches Modell beschreibt. Dieser Algorithmus sollte
als Input Argumente folgende Angaben zur Position des Users bekommmen:

- $latitude$
- $longitude$
- $speed$ 
- $direction$

Als Output Argumente dieser Funktion sollten ein Tupel zurückgegeben werden, welches aus folgenden Komponenten bestehen soll:

- $speed$ in km/h
- ein Tupel bestehend aus $way$ Objekten, wobei das erste Objekt dieses Tupels den Weg darstellen soll, auf welchem sich der User befindet

Im Nachhinein sollte dieser Algorithmus in der Funktion $get\_limit()$ implementiert werden. Dieser Algorithmus wurde dann ausgiebig getestet
und weiter angepasst. Diesen Prozess halten wir weiter in dieser Ausarbeitung fest.

.. figure:: statics/blackbox.png
    :width: 600px
    :align: center
    :alt: Straight way
    :figclass: align-center

    Darstellung des Workflows

Mathematisches Grundmodell
--------------------------

In diesem mathematischem Modell betrachten wir 2 wichtige Komponenten, einerseits $location$ Objekte und andererseits
$way$ Objekte. Diese beiden Komponenten möchten wir zunächst näher beschreiben und diesen Objekten eine Rolle in unserem
Algorithmus zuweisen. 

- Das eine $location$ Objekt, welches für uns von besonderer Bedeutung ist, ist die Location $pointSelf$ des Users der Anwendung. Dieses Objekt ist als schwarzer Punkt in folgender Abbildung vermerkt. Dieses Location Objekt $pointSelf$, welches den aktuellen Standpunkt des Users beschreiben soll, beinhaltet dabei die Input Argumente $latitude, longitude, speed$ und $direction$ der Funktion $get\_limit()$. 
- Das andere ausschlaggebende Objekt ist ein $way$ Objekt, welches die Straßen und Wege darstellen sollen, auf welchen sich der User fortbewegt. In unserer Abbildung sind die Wege und Straßen durch graue Striche abgebildet. In unserem Algorithmus vergleichen wir jedes mögliche $way$ Objekt in einem bestimmten Radius um das $location$ Objekt $pointSelf$
  mit dem Standpunkt $pointSelf$ des Users und bestimmen spezielle Parameter, die uns später entscheiden lassen, welches $way$ Objekt am wahrscheinlichsten zu der aktuellen Position des Users passt.

Weiterhin gilt zu vermerken, dass wir nur die Wege und Straßen betrachten, welche sich in einem bestimmten Suchradius $r$, angegeben in Metern, um den User befinden. Diesen Suchradius fragen wir 
im besten Fall exakt ein Mal ab, jedoch ist es auch möglich den Suchradius $r$ maximal 2 Mal 
zu erweitern, so dass wir mindestens ein Rückgabe $way$ Objekt erhalten. Dabei sind die möglichen Wert, welcher der Suchradius $r$ annehmen kann entweder 80, 150 und 300 Meter.
In folgender Abbildung ist der Suchradius $r$ um den Punkt $pointSelf$ durch einen roten Kreis vermerkt.

.. figure:: statics/mathematischesModell.png
    :width: 600px
    :align: center
    :alt: Straight way
    :figclass: align-center

    Darstellung der wichtigsten Komponenten

Für jedes $way$ Objekt in einem Radius $r$ der aktuellen Position des Users $pointSelf$ bestimmen wir
einen Paramter $qL$, welcher die Güte dieses $way$ Objektes beurteilt. Wir beurteilen die Güte $qL$ eines $way$ Objektes nach
verschiedenen Kriterien, die wir in den nachfolgenden Stichpunkten besprechen:

- Das Ausgangsmodell berücksichtigt zum einen den minimalen Abstand $distance$ zwischen der aktuellen Position 
  $pointSelf$ des Users zu einem gegebenen $way$ Objekt. 

  .. figure:: statics/image.png
    :width: 600px
    :align: center
    :alt: Straight way
    :figclass: align-center

    Ermittlung des minimalen Abstandes der momentanen Position des Users $pointSelf$ zu einem $way$ Objekt

  Den minimalen Abstand berechnen wir mithilfe der Funktion $getNearestPointToWay()$. Diese 
  Funktion nimmt als Eingabeargumente einerseits das $way$ Objekt und andererseits die aktuelle Position des Users $pointSelf$.
  Als Rückgabewert erhält man ein Tupel $(latitude, longitude)$, welches denjenigen Punkt auf dem $way$ Objekt darstellt,
  welcher am kürzesten von $pointSelf$ entfernt ist.

  .. figure:: statics/getNearestPointToWay.png
    :width: 600px
    :align: center
    :alt: Straight way
    :figclass: align-center

    getNearestPointToWay() Funktion 
  
  Die Funktion berechnet diese Daten, indem wir das $location$ Objekt $pointSelf$
  als Punkt in einem Koordinatensystem begreifen, wobei $latitude$ und $longitude$ $x$- und $y$-Koordinaten darstellen.
  Das $way$ Objekt interpretieren wir als 2-dimensionale Gerade. Wir können diese Darstellungsweise wählen, da ein
  $way$ Objekt durch 2 $location$ Objekte markiert wird, die in den meisten Fällen als Beginn und Anfang des $way$ Objektes
  verstanden werden können. Die Vektoren, welche nur die $latitude$ und $longitude$ der beiden $location$ Objekte beinhalten, benennen wir mit $pointWay_{1}$ und $pointWay_{2}$.
  Die Gerade $g$, die durch die beiden Punkte $pointWay_{1}$ und $pointWay_{2}$ geht, hat somit folgende Form:

  .. math:: 
    g: \left(\begin{array}{c} latitude_{way} \\ longitude_{way} \end{array} \right) = pointWay_{1} + r * (pointWay_{2} - pointWay_{1}), r \in \mathbb{R}

  Nachdem wir die Gerade $g$ definiert haben, bestimmen wir eine Hilfsgerade $h$, für die gilt, dass der Normalenvektor der Geraden $h$ gerade der Richtungsvektor
  der Geraden $g$ ist. Weiterhin soll gelten, dass der Punkt $pointSelf$ auch auf dieser Geraden liegt. Damit erhalten wir folgende Gerade $h$,
  wobei $point$ ein beliebiger 2-dimensionaler Punkt ist und gilt $a \in \mathbb{R}$.

  .. math:: 
    h: (pointWay_{2} - pointWay_{1}) \cdot point = a

  Im Anschluss bestimmen wir den Lotfußpunkt von $g$ und $h$, indem wir $g$ in $h$ einsetzen und nach $r$ umstellen.

  .. math:: 
    (pointWay_{2} - pointWay_{1}) \cdot (pointWay_{1} + r * (pointWay_{2} - pointWay_{1})) = a
    

  Setzen wir zuletzt den errechneten Wert $r$ in $g$ ein, so erhalten wir die Rückgabewerte unserer Funktion, also
  ein Wertepaar $(latitude, longitude)$
- Zum anderen berücksichtigt das Ausgangsmodell die Winkeldifferenz $diffDegree$ der $direction$ des $way$ Objektes und der $direction$ von $pointSelf$.
  
  .. figure:: statics/direction.png
    :width: 600px
    :align: center
    :alt: Straight way
    :figclass: align-center

    Vergleich der $direction$ Werte von $pointSelf$ und dem $way$ Objekt

  Die Differenz $diffDegree$ entspricht somit der maximalen Winkeldifferenz zwischen $direction$ des Weges und $direction$ des Users, wobei gilt,
  dass $0 \leq diffDegree \leq 90$.

  .. figure:: statics/diffDegree.png
    :width: 300px
    :align: center
    :alt: Straight way
    :figclass: align-center

    Darstellung der Winkeldifferenz $diffDegree$
  
  Diese Winkeldifferenz $diffDegree$ errechnen wir mithilfe der Funktion $getDegreeDifference()$, die als Eingbewerte
  einerseits die $direction$ des $way$ Objektes in Bezug auf Norden und andererseits die $direction$ des $location$ Objektes
  $pointSelf$, ebenfalls in Bezug auf Norden, erhält. Als Rückgabewert erhält man hier den Winkel $diffDegree$.

  .. figure:: statics/getDegree.png
    :width: 600px
    :align: center
    :alt: Straight way
    :figclass: align-center

    Funktion getDegreeDifference()
  
Im Ausgangsmodell führen wir den minimalen Abstand zwischen dem $location$ Objekt $pointSelf$ und dem $way$ Objekt
und der Winkeldifferenz $diffDegree$ nun in ein Gütemaß $qL \in \mathbb{R}_{+}$ über, wobei gelten soll, dass ein
Wert nahe 0 einer hohen Trefferwahrscheinlichkeit entsprechen soll. Andererseits soll ein hoher Zahlenwert $qL$
bedeuten, dass das $way$ Objekt nicht als möglicher Weg infrage kommt, wenn sich der User bei $pointSelf$ befindet.
Die Leitidee, die hinter dem folgenden Mechanismus steckt, bezieht sich stark auf die Idee einer Standardabweichung:
Kleine Abstände $diffLocation$ zwischen dem momentanen Standpunkt des Users und des $way$ Objektes und auch kleine 
Winkeldifferenzen $diffDegree$ sollen betragsmäßig wenig auf das Gütemaß $qL$ aufaddieren. Hingegen sollen betragsmäßig große Zahlenwerte 
$diffLocation$ und $diffDegree$ besonders viel auf das Gütemaß $qL$ aufaddieren. Damit arbeiten wir mit folgender
Gleichung, die das Gütemaß $qL$ bestimmt.

.. math::
  qL = \frac{\sqrt{diffLocation^{2} + diffDegree^{2}}}{2}

All diese Schritte werden nun für alle möglichen $way$ Objekte berechnet. Im Anschluss werden die verschiedenen Gütemaße betrachtet.
Jener Weg mit dem niedrigsten Gütemaß $qL$ wird als Weg ausgewählt, auf welchem sich der User am wahrscheinlichsten befindet.

Beurteilen wir nun dieses Modell nach 2 Kriterien: 

1) Wie verhält sich dieses Modell mit gesäuberten Daten, welche per Hand generiert wurden?
2) Wie verhält sich dieses Modell mit real gesammelten Daten?

Genauigkeit bei gesäuberten Daten bei mathematischem Grundmodell
----------------------------------------------------------------

Die folgenden Beispiele wurden am Rechner erstellt, um möglichst gut nachvollziehbare Datensätze benutzen zu können. Dies ist notwendig, da wir
in der Realität teilweise starken Messfehlern unterliegen. Damit wir zunächst die Grundfunktionen des Algortihmus nachvollziehen können,
arbeiten wir mit künstlich erstellten Daten.

1) Gerade Straße

  .. figure:: statics/bleichstraße_bild.png
    :width: 600px
    :align: center
    :alt: Straight way
    :figclass: align-center

    Gerade Straße

  Das oben gezeigte Beispiel lässt sich in 17 Wegstücke aufteilen (diese entsprechen nicht den gezeigten Punkten).
  Der Algorithmus ist in der Lage 8 der 17 Wegstücke richtig zuzuordnen.

2) Straße mit Ecken

  .. image:: statics/imFiedlersee.png
    :width: 400
    :alt: Straße mit Ecken

  Bei diesem Beispiel werden 7 der 8 Wegpunkte korrekt zugeordnet. 

Wir sehen, dass der Algorithmus noch große Schwierigkeiten damit hat, das richtige $way$ Objekt auszuwählen, wenn die
Dichte der $way$ Objekte auf dem betrachteten Gebiet sehr hoch ist. Dies möchten wir mit einer überarbeiteten Version des Algorithmus
verringern.

Genauigkeit bei ungesäuberten Daten bei mathematischem Grundmodell
------------------------------------------------------------------

1) Gerader Weg

  .. image:: statics/unsauber.png
    :width: 400
    :alt: Street with corners

  Bei diesem Beispiel werden 3 der 34 Wegpunkte falsch zugeordnet. Schnell erkennen wir auch warum: Die Messgenauigkeit
  der Testdaten ist nicht sehr genau, da die Abweichung des zu bestimmenden Wegpunktes $pointSelf$ um 35 Meter abweichen kann. Vor
  allem bei kleinen Geschwindigkeiten, mit denen sich der User bewegt, entstehen so hohe Messungenauigkeiten. Deshalb erweitern wir unser mathematischen Modell
  im nächsten Abschnitt, um so Messfehlern vorzubeugen.

Erweiterung des mathematischen Grundmodells
-------------------------------------------

Wir haben erkannt, dass weitere Maßnahmen ergriffen werden sollten, sodass der Algorithmus eine höhere
Trefferwahrscheinlichkeit generiert. Dazu betrachten wir folgende Stichpunkte:

- Wir erweitern das Modell von oben weiterhin, indem wir nicht nur das $location$ Objekt $pointSelf$ betrachten,
  sondern auch 6 weitere $location$ Objekte generieren. 
  
  .. figure:: statics/multiple.png
    :width: 600px
    :align: center
    :alt: Straight way
    :figclass: align-center

    Erstellung weiterer $location$ Objekte aus $pointSelf$

  Dabei befinden sich 3 $location$ Objekte for dem User,
  welche mit $pSelfF, pSelfFF, pSelfFFF$ benannt werden. Die anderen 3 $location$ Objekte befinden sich gerade hinter dem User,
  und werden $pSelfP, pSelfPP, pSelfPPP$ genannt. Alle Punkte sind exakt 5 Meter voneinander entfernt. Die Gemeinsamkeit
  dieser $location$ Objekte ist, dass sie alle dieselbe $direction$ teilen. Dabei handelt es sich um die $direction$,
  welche aus den Eigabewerte der $get\_limit()$ Funktion hervorgeht.

- Für jedes dieser 7 $location$ Objekte errechnen wir ein Gütemaß $qL_{way, singleLocation} \in \mathbb{R}_{+}$ für alle $way$ Objekte.
  Dieses errechnet sich ähnlich zu dem Gütemaß $qL$ aus unserem Grundmodell. Dabei gilt ebenfalls wieder, dass ein niedriger Zahlenwert dieses Gütemaßes 
  eine hohe Sicherheit bedeutet und umgekehrt ein hoher Zahlenwert eine niedirge Sicherheit bedeutet.

  .. math::
    qL_{way, singleLocation} = \frac{\sqrt{0.75 * diffLocation^{2} + 0.25 * diffDegree^{2}}}{2}

  Die Faktoren 0.75 und 0.25 ergeben sich aus Erfahrungswerten, da die Abweichung der real gemessenen $direction$ des Users sehr schwankt und somit wenig
  Aussagekraft hat. Somit berücksichtigen wir diesen Wert weniger.
- Im Anschluss berechnen wir ein geteiltes Gütemaß $qL_{way, multipleLocations} \in \mathbb{R}_{+}$. Dieses Gütemaß bezieht sich 
  auf alle 7 $location$ Objekte, die aus einem $location$ Objekt generiert wurden. Das geteilte Gütemaß $qL_{way, multipleLocations}$
  errechnet sich wie folgt:

  .. math::
    qL_{way,  multipleLocations} = \frac{\sqrt{\sum_{i=1}^{7}qL_{way, singleLocation,i}^{2}}}{7}

  Auch hier ist es wieder so, dass ein niedirger Zahlenwert dieses Gütemaßes 
  eine hohe Sicherheit bedeutet und umgekehrt ein hoher Zahlenwert eine niedrige Sicherheit bedeutet.

- Zuletzt bauen wir einen weiteren Sicherheitsmechanismus ein: Hat unser Algorithmus das betrachtete $way$ Objekt
  bereits im vorigen Durchlauf der $get\_limit()$ Funktion als den wahrscheinlichsten Kandidaten unter allen $way$ Objekten
  ausgesucht, so verringern wir das errechnete Gütemaß $qL_{way,  multipleLocations}$ dieses $way$ Objektes in diesem Aufruf der $get\_limit()$ Funktion
  um die Hälfte, da es sehr wahrscheinlich ist, dass wir uns wieder auf demselben Weg befinden, wenn wir uns davor schon af diesem 
  Weg befunden haben.

Beurteilen wir nun die Erweiterung des mathematischen  Grundmodells nach den 2 bekannten Kriterien: 

1) Wie verhält sich dieses Modell mit gesäuberten Daten, welche per Hand generiert wurden?
2) Wie verhält sich dieses Modell mit real gesammelten Daten?

Genauigkeit bei gesäuberten Daten
---------------------------------

Um wirklich fetstellen zu können, ob die vorangegangenen Veränderungen den Algorithmus verbessert haben, verwenden wir wieder dieselben 
Datensätze.

1) Gerade Straße

  .. figure:: statics/bleichstraße_bild.png
    :width: 600px
    :align: center
    :alt: Straight way
    :figclass: align-center

    Gerade Straße

  Der Algorithmus hat 16 der 17 Wegstücke richtig zugeordnet. Die Genauigkeit des Algorithmus
  liegt hier bei ungefähr 0.94 Prozent. 
  Wir erkennen somit eine deutliche Steigerung der Genauigkeit des Algorithmus.

2) Straße mit Ecken

  .. image:: statics/imFiedlersee.png
    :width: 400
    :alt: Street with corners

  Bei diesem Beispiel werden alle 8 Wegpunkte korrekt zugeordnet.

Genauigkeit bei ungesäuberten Daten
-----------------------------------

1) Gerader Weg

  .. image:: statics/unsauber.png
    :width: 400
    :alt: Street with corners

  Bei diesem Beispiel werden nur 2 der 34 Wegpunkte falsch zugeordnet. Somit haben wir auch hier die Genauigkeit
  des Algorithmus erhöht.

Fazit
-----

Es lässt sich zusammenfassen, dass es bereits mit einfachen Mitteln möglich ist, eine meist zuverlässige Lösung für
das von uns gestellte Problem zu finden. Die von uns erarbeite Lösungsmethode baut auf einfachen mathematischen 
Konzepten auf und erlaubt so die interdisziplinäre Verbindung zwischen der Mathematik und der Informatik. Ebenfalls ist
es interessant, ein mathematisches Modell zu entwickeln, welches sehr praktisch orientiert arbeitet. Selten hat man
so schnell einen Bezug zur Realität aufbauen können, wenn man mathematische Modelle entwickelt und anwendet. 

Beim Prozess des Entwickelns dieser Anwendung habe ich jedoch festgestellt,
dass es einen großen Unterschied macht, in der Theorie zu arbeiten und sich danach mit realen Beispielen zu beschäftigen.
Es gab viele weitere Ideen, welche auch umgesetzt wurden und in der Theorie auch vielversprechend waren. 
Jedoch hat sich mit dem Bezug zur Realität meistens schnell herausgestellt, dass diese Überlegungen doch zu kompliziert waren
oder schlichtweg nicht gewinnbringend waren. 

Im Endeffekt war es sehr spannend, reale Erfahrungen sammeln zu können und an einem Projekt mitarbeiten zu dürfen, 
welches so vielschichtig und komplex war wie dieses.

License
-------

Code and documentation are available according to the license
(see LICENSE file in repository).
