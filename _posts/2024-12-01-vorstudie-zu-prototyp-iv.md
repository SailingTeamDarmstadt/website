---
title: "Vorstudie zu Prototyp IV"
date: 2024-12-01
permalink: /2024/12/vorstudie-zu-prototyp-iv/
image: /assets/2024/12/photo_5274150497697263360_y.jpg
excerpt: "Bei letzten Sailbot, meinte die Organisatorin Sarah beim Abschlussevent, dass das Beste an der Sailbot nicht die Konkurrenz zwischen den Teams ist, sondern dass alle sich gegenseitig unterstützen ( Grüße an Cornell, wenn Ihr wieder einen spare Pi braucht, meldet euch einfach , wir stellen euch gern "
---

Bei letzten Sailbot, meinte die Organisatorin Sarah beim Abschlussevent, dass das Beste an der Sailbot nicht die Konkurrenz zwischen den Teams ist, sondern dass alle sich gegenseitig unterstützen (*Grüße an Cornell, wenn Ihr wieder einen spare Pi braucht, meldet euch einfach*, *wir stellen euch gern wieder unsern Backup zur Verfügung*) und bereits auf dem Abschlussevent Ideen fürs nächste Jahr diskutiert werden. Dem wollten wir uns nicht verweigern, und so sind schon auf dem Rückflug die Ideen für das nächste Boot entstanden.

<div class="gallery"><img alt="" loading="lazy" src="{{ site.baseurl }}/assets/2025/02/photo_5274150497697263178_y-1-rotated.jpg"/><img alt="" loading="lazy" src="{{ site.baseurl }}/assets/2025/02/photo_5274150497697263198_y.jpg"/></div>

Eines der Probleme, die wir wärend der Sailbot festgestellt haben, war durch die Wende zu kommen. Unsere Analyse ergab, das wir nicht die Trägheit der größeren Konkurenzboote haben, plus das wir starkes Schlingern beim Segeln am Wind hatten.

![]({{ site.baseurl }}/assets/2024/12/IMG_7350-1241x1536.jpeg)

Die erste Idee basiert auf dem Model eines [Sandbaggers](https://de.wikipedia.org/wiki/Sandbagger_(Bootstyp)), das wir im Museum in Salem gesehen haben. Ein kurzer Rumpf, Formstabilität, ein weit herausragender Bugspriet und Großbaum und damit riesige Segelfläche für ein kleines Boot sind die Hauptmerkmale dieser Boote. Beim genaueren Nachforschen über diese Boote sprang und aber der Punkt mit dem Beweglichen Ballast sehr schnell ins Auge. Das wäre grundsätzlich technisch umsetzbar: das Team von WPI hatte ein solches System zur Ballastverlagerung an Bord, aber aus Energiegründen nicht eingesetzt. Außerdem wollen wir doch lieber ein Boot bauen, das von selbst stabil im Wasser liegt und sich nicht bei Krängung selber versenken kann.

Beim Designen von roBOOTer hatten sich unsere Vorgänger schon tiefer mit dem Thema beschäftigt und uns zwei Bücher zu dem Thema hinterlassen. Principles of Yacht Design von Lars Larsson und Rolf Eliasson und Seetüchtigkeit von C. A. Marchaij. Insbesondere die Ausführungen im zweiten zur Seetüchtigkeit brachte uns auf eine Beobachtung, die wir bislang noch nicht gemacht hatten: Durch den Scale-Faktor von Marlin sind selbst 10 cm hohe Wellen vergleichbar mit ca. 1 m Wellen bei seinem großen Vorbild. Während der Sailbot zeigte sich eindeutig, das wir mit mindestens solchen Wellenhöhen zu rechnen haben und die Annahme treffen sollten, das wir die Designregeln für ein Blauwasserboot mehr beachten sollten als die für eine reine Schönwetter-Binnenyacht.

<div class="gallery"><img alt="" loading="lazy" src="{{ site.baseurl }}/assets/2025/02/m7304_crop169014_2000x2000_proportional_1670195685B05C-1594148057-1536x1215.jpg"/><img alt="" loading="lazy" src="{{ site.baseurl }}/assets/2025/02/2053bbc09a746158f1730a5aef61d4e6-2846939303.jpg"/><img alt="" loading="lazy" src="{{ site.baseurl }}/assets/2024/12/22er_Schaere.jpg"/></div>

Bei der Suche nach Booten, die wir als Referenz nutzen können sind wir auf die [Ranger](https://de.wikipedia.org/wiki/Ranger_(Yacht)) bzw. die dazugehörige [J-Class](https://de.wikipedia.org/wiki/J-Klasse_(Segeln)) und die Klasse der [Schärenkreuzer](https://en.wikipedia.org/wiki/Skerry_cruiser) gestoßen. Beide haben ein durchaus ähnlichen Schnittplan, wobei die J-Class seetauglich ist und die Schärenkreuzer durch ihre Segelanforderungen im Wind der Fjorde in ähnlichen Bedingungen wie wir auf einem umrandeten See segeln muss.

<div class="gallery"><img alt="" loading="lazy" src="{{ site.baseurl }}/assets/2025/02/photo_5274150497697263166_y.jpg"/><img alt="" loading="lazy" src="{{ site.baseurl }}/assets/2025/02/photo_5274150497697263211_y.jpg"/><img alt="" loading="lazy" src="{{ site.baseurl }}/assets/2025/02/photo_5274150497697263212_y.jpg"/><img alt="" loading="lazy" src="{{ site.baseurl }}/assets/2025/02/photo_5433696386576147300_y.jpg"/></div>

Mit diesen Vorlagen entstanden die ersten CAD Zeichnungen und 3D Drucke. Diese zeigen aber bereits im Bug eine Veränderung zu den oben genannten Modellen, die sich durch die gesamte Studienreihe durchzieht.

Die Aufnahmen während der Sailbot zeigten, das wir beim segeln am Wind durch das Stampfen sehr viel Geschwindigkeit verlieren. Unsere Idee war daher, den Bug so umzubauen, das er in die Welle eintaucht und das Wasser auf ihm dem Auftrieb entgegenwirkt und wir in einer möglichst gleichbleibenden Lage durch die Welle segeln. Dieser Gedanke führt auch zu dem Langkiel, der zwar so schon auch in der Ranger, und verkürzt im Schärenkreuzer, zu finden ist, wir nun aber bewusst übernehmen.

<div class="gallery"><img alt="" loading="lazy" src="{{ site.baseurl }}/assets/2025/02/photo_5267495020670344659_y.jpg"/><img alt="" loading="lazy" src="{{ site.baseurl }}/assets/2025/02/photo_5274150497697263172_y.jpg"/></div>

Das Problem das wir beim Zeichnen dieser Studien immer wieder hatten war, dass der am weitesten vorne liegende Punkt zum Schneiden in die Welle immer auf der Wasserlinie lag und wir somit auch in die kleinsten Wellen eintauchen würden. Damit würde das Boot aber auch bei Wellen, die uns kaum ins Stampfen bringen würden, Fahrt durch den erhöhten Wasserwiderstand verlieren. Die Versuche, das zu vermeiden führten uns zu diversesten Ideen, die wir nicht mal mehr druckten oder simulierten, da der innewohnende Wahnsinn der Zeichnung uns auch so schon klar wurde. Der schönste Kommentar zu diesen Entwürfen war „Das sieht aus wie eine Kaulquappe“, ein Tier das nun wirklich nicht unserem Design entsprach.

![]({{ site.baseurl }}/assets/2025/02/photo_5274150497697263686_y.jpg)

*Eine der etwas radikaleren Designideen*

Parallel zu den immer weiter angepassten CAD Zeichnungen, in die wir unsere wachsende Erfahrung einfließen ließen, wurden auch einige Prototypen in kleinerem Maßstab gedruckt und ersten Tests unterzogen.

![]({{ site.baseurl }}/assets/2025/02/photo_5274150497697263155_y-2.jpg)

*Gruppe der finaleren Studienentwürfe*

All dies zusammen, inklusive der weiteren Suche nach anderen erprobten Lösungsansätzen führte uns zu einem Design das ähnlich zum X- bzw. Axe-Bow ist. Das ist ein nach oben gezogener Keil, der ins Wasser schneidet und die Wellen zur Seite lenkt. Dabei erzeugt er aber durch eine geringere Höhe und Verkürzung der Wasserlinie am Bug einen geringeren Windfang und Strömungswiderstand bei der Wende, selbst wenn diese beim Eintauchen in die Welle auftritt. Dass unser Bug am Ende sehr ähnlich zu dem Bug einer IMOCA-Hightech-Rennyacht aussieht, lässt uns vermuten, das wir auf dem richtigen Weg sind.

![https://commons.wikimedia.org/wiki/File:Imoca_Charal_2_%282022%29_01.jpg]({{ site.baseurl }}/assets/2024/12/Imoca_Charal_2_2022_01.jpg)

Da wir angefangen haben, ein neues Boot zu designen, das gut durch die Wende kommt, ist die Manövrierfähigkeit des Designs der nächste Optimierungsschritt. Dem steht ein Langkieler deutlich im Weg, da er ja traditionell für eine bessere geradeaus Lauffähigkeit steht und bei Manövern eine riesige Fläche bzw. Flügel darstellt, dessen Kurs angepasst werden soll.

![]({{ site.baseurl }}/assets/2025/02/02920-jpg-582184864.jpg)

*Rissplan der Ranger*

Langkieler bieten jedoch, laut der Literatur, einen Vorteil gegenüber kürzeren Kielen bei langsamen Geschwindigkeiten. Die geringe Aspect Ratio des Kiels erlaubt die Generierung von Auftriebskraft schon bei geringen Geschwindigkeiten, vergleichbar mit den Klappen bei Flugzeugen, die für Start und Landung verwendet werden und den Auftrieb erhöhen. Um somit beim Beschleunigen aus der Wende nur geringen Abdrift zu haben, wollten wir den Kiel so beibehalten.

![]({{ site.baseurl }}/assets/2025/02/photo_5274150497697263149_y-rotated.jpg)

*Letzter Studienprototyp*

Unsere Lösung für dieses Problem wird vor allem bei einem der letzten Studienmodelle deutlich. Neben dem nach hinten geneigten Axe-bow sieht man die riesige Fläche im Kiel, die durch das Ruder eingenommen wird. Bei diesem Prototypen noch deutlich überdimensioniert ist unser Ansatz, die Aspect Ratio des Kieles bei Manövern, also genau dann, wenn uns eine geringe Ratio stören würde, zu verändern und, durch das wegkippen des Ruders zu erhöhen (*Zur Erinnerung: Die Aspekt Ratio ist das Verhältnis von Flügelwurzel zu Flügellänge. Ein langer, schmaler Flügel hat eine hohe Aspekt Ratio, ein kurzer Stummel eine niedrige.*) Da unsere finale Konstruktion nur 1 Meter lang ist, sind die Kräfte, die zum Stellen eines solchen Ruders relevant sind, deutlich geringer. Das obere Bild vom Rissplan der Ranger zeigt, die verhältnismäßig klein das Ruder dort zum Kiel ist. Da Sie jedoch auf Tempo optimiert ist, hat Sie nicht die Probleme von uns.

Zudem wird unser Ruder nicht am Ende des Kiels befestigt, sondern seine Drehachse ist in seinen Masseschwerpunkt verschoben. Damit soll es aus dem Kiel heraus kippen können, und eine definierte Strömungsabrisskante im Kiel bilden.

Nun, wie sieht eigentlich der neue Prototyp aus? Noch ist er nicht gefertigt, aber die CAD Designs für die 13ten und finale Iteration der Studie ist großteils fertig und werden demnächst gedruckt. Sobald der Rumpf fertig ist, schreiben wir einen Updateartikel, aber bis dahin, hier erst einmal die aktuellen Pläne:

<div class="gallery"><img alt="" loading="lazy" src="{{ site.baseurl }}/assets/2025/02/photo_5274150497697263682_y.jpg"/><img alt="" loading="lazy" src="{{ site.baseurl }}/assets/2025/02/photo_5274150497697263683_y.jpg"/><img alt="" loading="lazy" src="{{ site.baseurl }}/assets/2025/02/photo_5274150497697263684_y.jpg"/></div>

*Bildquellen*:

- <https://www.americascup.com/history/30_RANGER-THE-SUPER-J>
- *J Class Sailboat 1934 von Levick, Edwin*
- <https://commons.wikimedia.org/wiki/File:22er_Sch%C3%A4re.jpg>
- <https://commons.wikimedia.org/wiki/File:Imoca_Charal_2_%282022%29_01.jpg>
- <https://www.boatdesign.net/threads/scale-j-boat-j-class-ranger-thread-no-3.64267/>
