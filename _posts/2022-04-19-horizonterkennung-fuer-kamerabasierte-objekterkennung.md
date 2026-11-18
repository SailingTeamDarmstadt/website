---
title: "Horizonterkennung für Kamerabasierte Objekterkennung"
date: 2022-04-19
permalink: /2022/04/horizonterkennung-fuer-kamerabasierte-objekterkennung/
image: /assets/2022/04/horizont-1360x480.png
excerpt: "Um ohne Segler in der Lage zu sein schwimmenden Hindernissen auszuweichen werden unsere autonomen Boote mit Computer Vision Methoden ausgestattet. Damit unbekannte Objekte korrekt lokalisiert werden können, also insbesondere der Abstand zum Boot geschätzt werden kann, ist der Verlauf des Horizonts i"
---

Um ohne Segler in der Lage zu sein schwimmenden Hindernissen auszuweichen werden unsere autonomen Boote mit Computer Vision Methoden ausgestattet. Damit unbekannte Objekte korrekt lokalisiert werden können, also insbesondere der Abstand zum Boot geschätzt werden kann, ist der Verlauf des Horizonts im Bild ein wichtiger geometrischer Hinweis. Dafür haben wir in den letzten Monaten ein neues Softwarepaket erarbeitet, welches den Horizont in Echtzeit erkennt und für die anstehende Hinderniserkennung bereitstellt. Als Grundlage für die Entwicklung verwenden wir Daten aus dem Marine Obstacle Detection Dataset (MODD) [1, 2].

*[1] M. Kristan, V. Sulic Kenk, S. Kovacic and J. Pers, „Fast Image-Based Obstacle Detection From Unmanned Surface Vehicles,“ in IEEE Transactions on Cybernetics, vol. 46, no. 3, pp. 641-654, March 2016. doi: 10.1109/TCYB.2015.2412251*

[2] Matej Kristan, Janez Pers, Vildana Sulic, Stanislav Kovacic. A Graphical Model for Rapid Obstacle Image-map Estimation from Unmanned Surface Vehicles, ACCV 2014, Singapore, November 2014.
