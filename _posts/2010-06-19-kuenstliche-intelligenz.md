---
title: "Künstliche Intelligenz"
date: 2010-06-19
permalink: /2010/06/kuenstliche-intelligenz/
excerpt: "Um unseren Segelroboter in die Lage zu versetzen autonom fahren zu können, müssen nicht nur die mechanischen Abläufe an Bord automatisiert werden, sondern auch alle wichtigen Entscheidungen über die Planung der Route und den Kurs müssen vom Boot selbst getroffen werden. Diese Aufgabe wird von Softwa"
---

Um unseren Segelroboter in die Lage zu versetzen autonom fahren zu können, müssen nicht nur die mechanischen Abläufe an Bord automatisiert werden, sondern auch alle wichtigen Entscheidungen über die Planung der Route und den Kurs müssen vom Boot selbst getroffen werden. Diese Aufgabe wird von Software übernommen.

Dazu haben wir nun ein Programm entwickelt, dass den besten Kurs bei gegebenem Wind berechnet. Es werden der gewünschte Start- und Endpunkt der zu fahrenden Strecke festgelegt und die Windverhältnisse als Vektorfeld dem Programm übergeben. Unter Berücksichtigung der Fahreigenschaften des Bootes, also wie schnell es unter welchem Winkel zum Wind fahren kann, wird daraus der schnellste Kurs berechnet. So ergibt sich beispielsweise bei einer Fahrt gegen den Wind der typische Zickzack-Kurs.

Die Berechnung des Kurses geschieht über Methoden der Variationsrechnung. Um die optimale Trajektorie zu finden, auf welcher man in kürzester Zeit von A nach B gelangt, wird zunächst ein Funktional formuliert, welches eine Aussage über die Durchlaufzeit der Trajektorie enthält. Nach Minimierung des Funktionals erhalten wir ein Randwertproblem, welches aus den Eulerschen Differentialgleichungen und der Randbedingung des Anfangs- und Endpunktes besteht.
