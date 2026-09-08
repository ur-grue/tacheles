# Stilistik: Was einen Text menschlich macht

Die Floskelliste fängt Slop. Stil ist mehr. Die deutsche Stilistik (Riesel, Fleischer/Michel, Sowinski, Eroms, Sandig) beschreibt Stil als Eigenschaft des ganzen Textes, die aus dem Zusammenwirken vieler Entscheidungen entsteht: Stilzüge. Die Forschung zu KI-Texten (Reinhart u. a. 2025, Irrgang u. a. 2024, Yang u. a. 2024) findet die Unterschiede zwischen Mensch und Modell genau dort: nicht in einzelnen Wörtern, sondern in Verteilungen, Varianz, Verkettung, Beteiligung. Ein Text kann jede Floskel vermeiden und trotzdem generisch klingen, wenn seine Sätze gereiht statt verkettet sind, alle mit dem Subjekt beginnen, gleich lang sind und keinen Standpunkt haben.

Eroms fasst die Stilanforderungen in drei Gebote: **Variation**, **Angemessenheit und Bildkraft**, **Sparsamkeit**. Sie ziehen in verschiedene Richtungen; die Spannung ist gewollt. Wo zwei Prinzipien kollidieren, entscheidet die Funktion an der Stelle, nie eine Quote.

Die vierzehn Prinzipien unten sind zugleich die Prüfreihenfolge: Textebene zuerst, Wortebene zuletzt. Alle Beispiele sind eigene Formulierungen.

## Textebene

### 1. Die Textsorte ist erkennbar und wird durchgehalten

Ein Text erzählt, beschreibt, argumentiert oder weist an (Eroms’ Vertextungsstrategien), und er benutzt die Muster seiner Sorte. Sprachmodelle schreiben alles im selben Register; Reinhart: „they don’t necessarily adapt to the writing style“. Das Einheitsschema Einleitung, drei Aspekte, Fazit ist das Kennzeichen des sortenlosen Textes.

Arbeitsanweisung: Vor dem Umschreiben die Sorte benennen (`textsorten.md`) und drei ihrer Erwartungen ausdrücklich machen. Kommentar: These im ersten Absatz, Ich erlaubt, Schluss mit Forderung. Bericht: Wer, was, wann zuerst, kein Ich, Schluss ohne Wertung. Anleitung: Imperativ, ein Schritt je Satz. Sortenfremde Muster entfernen.

### 2. Die Sätze sind verkettet, nicht gereiht

Daneš unterscheidet Arten der thematischen Progression: **linear** (das Neue des einen Satzes wird das Bekannte des nächsten), **durchlaufend** (alle Sätze haben dasselbe Thema, meist dasselbe Subjekt), **abgeleitet** (Teilthemen eines Oberthemas). Yang u. a. 2024 messen: Menschen schreiben überwiegend linear, Modelle überwiegend durchlaufend, und die durchlaufende Progression „macht den Text redundant und simpel wie eine Liste von Ideen“. Das ist der textlinguistische Grund, warum KI-Absätze aus parallelen Sätzen bestehen.

Arbeitsanweisung: Drei Sätze mit demselben Thema hintereinander sind ein Warnsignal, außer in einer bewussten Aufzählung. Mindestens jeden zweiten Übergang linear bauen: Das Ende von Satz n liefert den Anfang von Satz n+1.

> Vorher: Die Plattform bietet Analysen. Die Plattform ermöglicht Exporte. Die Plattform unterstützt mehrere Sprachen.
> Nachher: Die Plattform liefert Analysen. Die lassen sich als Tabelle exportieren, und die Tabelle kommt in der Sprache, die der Nutzer eingestellt hat.

### 3. Das Vorfeld arbeitet

Das Vorfeld ist die Stelle vor dem finiten Verb. Es ist die Anschlussstelle des deutschen Satzes: Dort steht, was an den Vorsatz anknüpft, ein Rahmen (Zeit, Ort, Bedingung), ein Kontrast oder das Thema. Speyers Korpusdaten: Das Subjekt besetzt das Vorfeld nur in etwa der Hälfte der Sätze; im Konkurrenzfall gilt Rahmensetzer vor Kontrast vor Topik. Deutscher Prosafluss entsteht wesentlich dadurch, dass das Vorfeld wechselnd belegt wird.

Arbeitsanweisung: Satzanfänge zählen. Beginnen mehr als etwa 60 Prozent der Sätze eines Absatzes mit dem Subjekt, umbauen: Rahmensetzer nach vorn („Seit Januar …“, „In Bremen …“, „Wenn das stimmt, …“), Kontrast nach vorn („Den Preis dagegen …“), Wiederaufnahme nach vorn („Diesen Vorschlag …“). Das Vorfeld nie mit einer leeren Floskel füllen („Es ist anzumerken, dass …“); dann leistet es keine Anschlussarbeit.

> Vorher: Der Vorstand hat den Plan gebilligt. Der Vorstand hat aber Bedingungen gestellt. Die Bedingungen betreffen das Budget.
> Nachher: Der Vorstand hat den Plan gebilligt. Bedingungen hat er trotzdem gestellt, und die betreffen das Budget.

### 4. Das Neue steht hinten

Thema-Rhema: Bekanntes vorn, Neues hinten. Im Deutschen stehen „Satzglieder mit dem größten Mitteilungswert in der Regel am Ende des Satzes“ (Behaghels zweites Gesetz). Das Satzende ist die stärkste Stelle. Wer dort Nebensächliches oder eine Floskel stehen lässt („…, was von großer Bedeutung ist“), verschenkt sie.

Arbeitsanweisung: Jeden Satz in Bekanntes und Neues sortieren. Das Neue ans Ende, möglichst in die rechte Satzklammer oder direkt davor. Satzenden auf Ballast prüfen.

> Vorher: Der neue Prozess wurde im März eingeführt, was die Bearbeitungszeit auf zwei Tage verkürzte, wie die Auswertung zeigt.
> Nachher: Im März kam der neue Prozess. Seitdem dauert die Bearbeitung zwei Tage statt acht.

### 5. Zusammenhalt durch Wiederaufnahme, nicht durch Anschlusswörter

Brinker unterscheidet Wiederaufnahme (Wiederholung, Pronomen, Synonym, Oberbegriff, sachliche Nähe wie Antrag → Frist) von Konnektoren, die nur sagen, wie zwei Sätze zusammenhängen. Irrgang u. a. finden bei Menschen eine höhere mittlere Satzähnlichkeit (sie greifen Inhalte wieder auf), bei Modellen mehr Diskursmarker. Menschlicher Zusammenhalt entsteht durch Inhalt, maschineller durch „zudem“.

Arbeitsanweisung: Additive Konnektoren am Satzanfang („Darüber hinaus“, „Zudem“, „Außerdem“, „Des Weiteren“) streichen und den Anschluss durch Wiederaufnahme herstellen. Konnektoren nur für echte logische Relationen: Grund, Gegensatz, Bedingung, Folge.

> Vorher: Das Tool erkennt Duplikate. Darüber hinaus schlägt es Zusammenführungen vor. Zudem protokolliert es jede Änderung.
> Nachher: Das Tool erkennt Duplikate und schlägt vor, sie zusammenzuführen. Jede dieser Zusammenführungen landet im Protokoll.

### 6. Schlüsselwörter bleiben gleich, Strukturen variieren

Das englische Ideal der eleganten Variation gilt im Deutschen nicht. Das wiederholte Wort hält den Referenten eindeutig; Ersatzsynonymik („der Konzern, das Unternehmen, die Firma, der Hersteller“) erzeugt Unsicherheit. Zugleich wiederholen Modelle Strukturen und Füllwörter und variieren Schlüsselwörter; Menschen tun das Umgekehrte.

Arbeitsanweisung: Thema, Akteure und Fachtermini konsequent gleich benennen. Variation bei Satzbau, Satzanfang, Satzlänge und den nicht-terminologischen Wörtern. Zwei aufeinanderfolgende Sätze dürfen sich nicht in der Abfolge Subjekt, Verb, Objekt, Adverbial gleichen. Eine Anapher oder ein Parallelismus als Figur höchstens einmal je Text.

> Vorher: Der Antrag wurde geprüft. Das Gesuch enthielt Fehler. Die Eingabe wurde zurückgewiesen.
> Nachher: Der Antrag wurde geprüft. Er enthielt Fehler, zwei fehlende Unterschriften, und ging zurück.

## Satzebene

### 7. Satzlängen streuen

Die Varianz der Satzlänge ist das robusteste Merkmal menschlicher Prosa in allen Detektorstudien; der metrische „Prosarhythmus“ dagegen ist empirisch nicht belegt. Kurze Sätze tragen Bewegung und Pointe, lange nehmen den Leser mit. Fontane: Sätze von vierzehn Zeilen neben solchen von vierzehn Buchstaben.

Arbeitsanweisung: Nicht auf eine Zielsatzlänge hin schreiben, sondern auf Streuung innerhalb des Korridors der Stufe. In einem Absatz von fünf bis acht Sätzen steht ein Satz unter acht Wörtern und einer über dem Korridormittel. Der kürzeste Satz steht dort, wo die Pointe oder der Widerspruch ist. Nie drei Sätze annähernd gleicher Länge hintereinander.

> Vorher: Die Umfrage zeigt eine hohe Zufriedenheit. Die Werte sind im Vergleich zum Vorjahr gestiegen. Besonders positiv wurde der Support bewertet. Verbesserungsbedarf gibt es bei der Dokumentation.
> Nachher: Die Zufriedenheit ist gestiegen, im Vergleich zum Vorjahr deutlich, und am besten schneidet der Support ab. Die Dokumentation nicht.

### 8. Logik steht in der Hierarchie, nicht in der Reihung

Hypotaxe ist nicht schlecht. Sie ist das Mittel, Abhängigkeiten sichtbar zu machen: Grund, Bedingung, Einräumung, Gleichzeitigkeit. Reinhart u. a. messen bei Modellen mehr Koordination („und“, „sowie“, „aber auch“); die Reihung versteckt die Logik.

Arbeitsanweisung: Koordinationen prüfen: Verbirgt sich hinter dem „und“ ein Weil, ein Obwohl, ein Während? Dann unterordnen. Je Absatz mindestens ein echtes Satzgefüge, wo eine Abhängigkeit besteht. Auf Stufe 1 gilt die Beschränkung auf weil, wenn, dass.

> Vorher: Die Kosten sind gestiegen und die Nachfrage ist gesunken und das Unternehmen hat die Produktion gedrosselt.
> Nachher: Weil die Kosten stiegen, während die Nachfrage sank, hat das Unternehmen die Produktion gedrosselt.

### 9. Die Klammer bleibt kurz, kurz vor lang

Zwischen dem finiten Verb und dem Verbrest (der rechten Satzklammer) liegt das Mittelfeld. Ist es überladen, wandert das sinntragende Verbteil ans Ende einer Strecke, die der Leser im Gedächtnis halten muss. Behaghel: Zusammengehöriges nebeneinander; das kürzere Glied vor dem längeren („Kinder und Kindeskinder“, „Rat und Unterstützung“).

Arbeitsanweisung: Höchstens etwa zwölf Wörter zwischen linker und rechter Klammer, auf Stufe 1 bis 3 sechs. Darüber ausklammern (Nachfeld: „…, in der Fassung, die …“) oder teilen. Aufzählungen nach Länge aufsteigend ordnen, wenn keine sachliche Reihenfolge dagegen spricht. Attribute nicht von ihrem Bezugswort trennen.

> Vorher: Wir haben die von der Rechtsabteilung nach mehreren Abstimmungsrunden mit externen Beratern überarbeitete Fassung des Vertrags gestern unterschrieben.
> Nachher: Gestern haben wir den Vertrag unterschrieben, in der Fassung, die die Rechtsabteilung nach mehreren Runden mit externen Beratern überarbeitet hatte.

### 10. Satzarten mischen, Figuren sparsam

Ellipse, Frage, Ausruf, Inversion sind in allen Textsorten zu Hause, nicht nur in der Literatur (Eroms). Modelle nutzen sie kaum; Bewerter erkennen menschliche Texte an einer Stimme, die „vertraut, menschlich oder persönlich“ wirkt (Casal/Kessler 2023). Manier beginnt bei der dritten rhetorischen Frage.

Arbeitsanweisung: Ab etwa 300 Wörtern eine echte Frage an die Sache oder den Leser, eine Ellipse als Pointe, ein Satz, der nicht mit einer Nominalphrase beginnt. Nicht mehr.

> Vorher: Es stellt sich die Frage, ob dieser Ansatz in der Praxis funktioniert. Die Antwort ist differenziert zu betrachten.
> Nachher: Funktioniert das in der Praxis? Teils. In kleinen Teams ja, ab zwanzig Leuten nicht mehr.

## Wortebene

### 11. Handlungen stehen im Verb, mit Handlungsträger

Nominalstil ist ein Werkzeug der Verdichtung mit eigenen Grenzen (Hennig 2020), kein Fehler an sich. Aber: Reinhart u. a. messen bei Modellen anderthalb- bis zweimal so viele Nominalisierungen, zwei- bis fünfmal so viele Partizipialkonstruktionen und einen durchgängig „nomenlastigen“ Stil; Menschen verankern ihre Sprache in Tempus, Aspekt und Modus. Das Verb ist das menschliche Register.

Arbeitsanweisung: Nominalisierungen und Streckverben in Vollverben mit Handelndem zurückverwandeln, außer als eingeführter Terminus oder als Wiederaufnahme einer schon erzählten Handlung (dann sind sie Kohäsionsmittel). Partizipialketten in Nebensätze auflösen. Tempus bewusst: Vergangenheit für Geschehenes, Konjunktiv für Fremdes, Futur sparsam.

> Vorher: Die Durchführung der Analyse erfolgt unter Berücksichtigung der Ergebnisse der Vorstudie mit dem Ziel der Ableitung von Handlungsempfehlungen.
> Nachher: Wir werten die Daten aus, gleichen sie mit der Vorstudie ab und leiten daraus ab, was zu tun ist.

### 12. Konkret vor abstrakt, Beobachtung vor Deutung

Linden (Duden-Handbuch): Adjektive kaschieren oft „einen Mangel an Präzision, die Unfähigkeit, genau hinzusehen“. Wie groß ist eine „riesige Halle“? „Eine Halle, groß wie ein Fußballfeld“ erzeugt die Vorstellung. Abstraktheit ist ein KI-Marker (Casal/Kessler, Liao u. a.); Eigennamen, Daten, Erfahrungswörter sind Menschenmarker (Irrgang u. a.). Die Bewertung entsteht beim Leser aus der Beschreibung, nicht aus dem Adjektiv: Grimm schreibt nicht „der grausame Wolf verschlang die hilflose Großmutter“, sondern „ging zum Bett der Großmutter und verschluckte sie“.

Arbeitsanweisung: Jede Abstraktion (Prozess, Maßnahme, Struktur, Lösung, Aspekt, Herausforderung) daraufhin prüfen, ob ein Beispiel, eine Zahl, ein Name, ein Ort, ein Gegenstand dahintersteht, und den nennen. Adjektive sortieren: spezifizierend (rot, dreijährig, fehlerhaft) bleibt; bewertend (beeindruckend, wichtig, spannend, umfassend) fällt oder wird Sachverhalt; Wörterehen (kläglich scheitern, nachhaltig verbessern) werden getrennt. Nichts erfinden: Wo das Original kein Detail liefert, die Stelle so bauen, dass sie eines tragen kann, und `[PRÜFEN: Zahl? Name? Beispiel?]` setzen.

> Vorher: Verschiedene Herausforderungen im Bereich der Logistik führten zu Verzögerungen.
> Nachher: Der Lieferant in Bratislava hat drei Wochen lang nichts geschickt; deshalb stand die Linie 2 still. `[PRÜFEN: Ort, Dauer, Linie aus dem Original?]`

### 13. Eine Stilebene, ein Bildfeld, ein Register

Stilbruch ist der unmotivierte Wechsel der Ebene (Sowinski): der Sprung vom sachlichen Bericht in den Broschürenton am Absatzende („Ein echter Meilenstein!“). Als bewusstes Mittel ist der Wechsel Figur, als Unfall Fehler; der Leser muss die Absicht erkennen. Bilder gehören zu Bildfeldern (Weinrich): Ein Fundament nimmt keine Fahrt auf. Abgenutzte Felder (Weg, Reise, Meilenstein, Brücke, Landschaft, Ökosystem, Schlüssel) sind zugleich KI-Felder. Fremdwörter sind Registersignal und KI-Signatur zugleich (Irrgang u. a.: Fremdwörter als KI-Merkmal in deutschen Texten).

Arbeitsanweisung: Zielebene vorab festlegen. Ebenensprünge auf Funktion prüfen. Bilder inventarisieren, gemischte entmischen, abgenutzte durch wörtliche Rede oder ein Bild aus dem Sachbereich ersetzen. Fremdwörter nur als Terminus. Eine gehobene Wendung je Absatz ist Akzent, drei sind Kostüm. Kollokationen idiomatisch: Man trifft eine Entscheidung, fasst einen Entschluss, stellt einen Antrag; „eine Entscheidung machen“ und „Erfolge realisieren“ sind Modellprosa.

> Vorher: Auf dem Weg zur Digitalisierung ist die neue Plattform ein Meilenstein, der die Brücke zu einem lebendigen Ökosystem schlägt.
> Nachher: Die neue Plattform ist die erste, auf der die drei Abteilungen dieselben Daten sehen. Vorher hatte jede ihre eigene Tabelle.

### 14. Standpunkt und Eigenheit bleiben

Reinhart u. a.: Modelle nutzen weniger Abschwächungen und Verstärkungen, weniger Modalverben, weniger Ich-Beteiligung; ihr Text ist „unbeteiligter, unpersönlicher“, das Sentiment neutral bis positiv. Yang u. a.: Modelle zeigen „weniger interpersonale Themen“, also weniger Interaktion mit dem Leser und weniger eigene Meinung. Menschlicher Text hat einen Standpunkt, und der zeigt sich in Abstufung (vermutlich, eher, kaum, immerhin), nicht in Superlativen. Stylometrie: KI-Text ist „auffällig uniform“, menschlicher „variabel und idiosynkratisch“. Wackwitz: Zu glatte Klarheit ist selbst ein Mangel.

Arbeitsanweisung: Die Wertungen des Autors stehen lassen, als Aussage. Symmetrische Abwägungen („einerseits, andererseits“, „sowohl als auch“) auflösen, wenn das Original eine Seite bevorzugt: Eine Seite bekommt das letzte Wort. Positive Bilanzsätze am Absatzende streichen. Echte Unsicherheit als Unsicherheit stehen lassen. Die drei auffälligsten Eigenheiten des Originals (Lieblingswörter, Ton, Rhythmus) bewahren; eine sperrige Stelle darf sperrig bleiben, wenn sie einen Gedanken trägt. Der Redakteur fügt keinen eigenen Standpunkt hinzu; er schützt den vorhandenen.

> Vorher: Beide Ansätze haben Vor- und Nachteile. Insgesamt bietet die Kombination beider Methoden ein vielversprechendes Potenzial.
> Nachher (wenn das Original den zweiten Ansatz bevorzugt): Der zweite Ansatz ist die bessere Wahl. Der erste ist eleganter, aber niemand im Team hat ihn in Produktion gesehen.

## Die Stilprüfung

Nach dem Umschreiben und nach der Messung, vor dem Substanzabgleich. Acht Fragen, Absatz für Absatz; jede Antwort „nein“ ist eine Stelle zum Umbauen.

1. Erkennt man die Textsorte am ersten Absatz, und hält der Text sie durch?
2. Greift mindestens jeder zweite Satz etwas aus dem Vorsatz auf, statt nur dasselbe Subjekt zu wiederholen?
3. Beginnen weniger als zwei Drittel der Sätze mit dem Subjekt?
4. Steht in jedem Absatz ein Satz unter acht Wörtern und einer deutlich über dem Mittel?
5. Enthält jeder Absatz mindestens ein konkretes Datum: Zahl, Name, Ort, Vorfall, Detail?
6. Trägt jeder Konnektor eine logische Relation, und steht kein „zudem“ am Satzanfang?
7. Kann jedes Subjekt tun, was sein Verb behauptet? Ein Prompt kürzt nichts, eine Studie fordert nichts, ein Markt belohnt niemanden. Das gilt auch für Pronomen: Worauf verweist „sie“ im nächsten Satz?
8. Klingt der Text nach dem Autor: Wertung, Ton, eine Eigenheit, die ein Modell nicht geschrieben hätte?

`scripts/messen.py` misst davon, was sich messen lässt (Subjekt-Anfänge, Streuung der Satzlängen, Konnektoren) und meldet es als Hinweis; bei Frage 7 erkennt es die offen genannten Fälle („Die Studie fordert“). Ein Pronomen, das auf ein Unbelebtes zurückweist, sieht es nicht: Dafür müsste es wissen, worauf „sie“ verweist. Fragen 1, 2, 5, 8 und der Pronomenfall in 7 bleiben Sache des Redakteurs.

## Quellen

Hans-Werner Eroms: *Stil und Stilistik* (2008) · Willy Sanders: *Stil und Stilistik* (1995), *Gutes Deutsch, besseres Deutsch* · Elise Riesel, Evgenia Schendels: *Deutsche Stilistik* (1975) · Wolfgang Fleischer, Georg Michel: *Stilistik der deutschen Gegenwartssprache* · Bernhard Sowinski: *Stilistik* · Barbara Sandig: *Textstilistik des Deutschen* (2006) · Ulla Fix u. a.: *Textlinguistik und Stilistik für Einsteiger* · Klaus Brinker: *Linguistische Textanalyse* · František Daneš: Zur linguistischen Analyse der Textstruktur (1970) · Augustin Speyer: Topicalization and Clash Avoidance (2008) · Otto Behaghel: *Deutsche Syntax* IV (1932) · Harald Weinrich: Semantik der kühnen Metapher (1963) · Mathilde Hennig: *Nominalstil* (2020) · Peter Linden: *Duden Handbuch Stilsicher schreiben* (2023) · Hanns-Josef Ortheil: *Schreiben dicht am Leben* (2012) · Stephan Wackwitz: Über Unverständlichkeit (2011) · Reinhart u. a.: Do LLMs write like humans?, PNAS 2025 · Irrgang u. a.: Features and Detectability of German Texts Generated with LLMs, KONVENS 2024 · Yang u. a.: Thematic progression patterns in human-written and AI-generated texts, System 2024 · Linguistic Characteristics of AI-Generated Text: A Survey (2025).
