---
title: "Neuer Open-Source Servo-Controller"
date: 2025-02-06
permalink: /2025/02/neuer-open-source-servo-controller/
categories: [team-news]
image: /assets/2025/02/sc-klein-scaled-1360x480.jpg
excerpt: "In unserem großen Prototypen, roBOOTer, übernehmen vernetzte Controller verschiedene Aufgaben wie die Steuerung des Ruders oder die Fernsteuerung. Aber was, wenn der Platz im Boot ein knappes Gut ist? Dann braucht man eine kompakte All-in-one-Lösung!"
---

In unserem großen Prototypen, roBOOTer, übernehmen vernetzte Controller verschiedene Aufgaben wie die Steuerung des Ruders oder die Fernsteuerung. Aber was, wenn der Platz im Boot ein knappes Gut ist? Dann braucht man eine kompakte All-in-one-Lösung!

Das ist zum Beispiel in unserem Test- und Wettkampf-Boot [Marlin]({{ site.baseurl }}/ueber-uns/boote/prototyp-iii/) der Fall. Hier ist es schon eine Herausforderung, die Sensoren, die Stromversorgung und die Kommunikation halbwegs störungsarm im Rumpf unterzubringen. Und ach ja, dann brauchen wir noch eine Schnittstelle zwischen Computer und Boot. Schnell war klar: Wir brauchen eine Neuentwicklung.

![]({{ site.baseurl }}/assets/2025/02/39b96f1e-2de7-4046-8b3c-7f0562fccbdd-1536x808.jpg)

## Die Servo-Controller-Hardware

Das Ergebnis ist unser Servo-Controller: Ein STM32-Mikrocontroller im [Adafruit-Feather-Format](https://learn.adafruit.com/adafruit-feather), mit einem Addon-Board als kompatibler FeatherWing. Die Highlights:

- STM32L452 – unser Standard-Mikrocontroller
- Mechanisch und elektrisch kompatibel mit Feather/FeatherWing
- Voll funktionaler USB-C, fast alle IOs sind erreichbar
- Zusatz-Features wie Debugging-Anschluss und MicroSD-Kartenslot
- Addon-Board mit CAN-Bus, PWM-Input für RC und Output für Servos
- Sehr flexible Stromversorgung per Löt-Brücken

Dieser Controller übernimmt nun die Aufgabe, die in roBOOTer die dedizierten Motorcontrollerplatinen übernehmen und erlaubt unserem Bord-PC die Motoren so zu steuern als wäre er noch in roBOOTer.

## Firmware für Marlin

Ein Controller braucht natürlich eine Firmware. Als Software-Testbed ist eine Aufgabe von Marlin, unseren Software-Stack auf dem Bootscomputer zu überprüfen. Deshalb kommuniziert der Servo-Controller mit dem Bootscomputer über CAN-Bus und simuliert so das modulare System von roBooter. Aktuell sind die folgenden Features implementiert:

- Plug-und-Play durch CAN-Bus-Kommunikation exakt wie in roBooter
- Servo-Skalierung/Kalibrierung
- Einfaches Hinzufügen/Ändern von Bootsparameters
- Überbrückung der Steuerung mit Fernbedienung z.B. im Fehlerfall
- Optionale USB-Konsole zur Fehlersuche

Gerade das zuverlässige Überbrücken des Bordcomputers durch Fernbedienung war während des SailBot-Wettbewerbs und in Testfahrten extrem hilfreich.

## Open Source!

Neben Marlin hat der flexible Controller seitdem testweise ein Motorboot gesteuert und wird auch im nächsten Prototyp, Toelpel, eingesetzt werden. Das Konzept mit FeatherWing-Addon-Board erlaubt es uns, den Controller in der Zukunft in komplett neuen Positionen einzusetzen, beispielsweise als Blackbox-Datenlogger oder Sensor-Board.

Und das Beste ist am Schluss: sowohl die [Hardware](https://github.com/SailingTeamDarmstadt/Featherboard_STM32L452) als auch die [Software](https://github.com/SailingTeamDarmstadt/sidewinder-servo-controller) sind open source! Wir freuen uns auf Inspirationen, Nachbauten und Erweiterungen.
