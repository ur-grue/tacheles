---
name: tacheles
description: Redigiert deutsche Texte wie ein erfahrener Redakteur – Slop raus, Substanz bleibt, Stil nach Wahl. Verwenden, sobald ein deutscher Text überarbeitet, redigiert, lektoriert, gekürzt, geglättet, „humanisiert“, „entsloppt“, verständlicher, einfacher, klarer, eleganter oder „weniger nach KI“ klingen soll; wenn jemand einen Text „im Stil von“ Wolf Schneider, Tucholsky, Kästner, Kisch, Kafka, Fontane, Thomas Mann oder Thomas Bernhard will; wenn eine Stufe zwischen einfach und ausführlich gewünscht ist (auch „Leichte Sprache“, „für Laien“, „für Vorstand“, „für Fachpublikum“); und immer, wenn Claude selbst einen längeren deutschen Sachtext, Artikel, Bericht, Newsletter, Blogpost oder eine wichtige E-Mail schreibt. Aufruf: /tacheles [1-5] [stil] [text oder datei].
argument-hint: "[Stufe 1-5] [Stil] [Text oder Datei]"
allowed-tools: Bash(python3 *), Read, Write
---

# tacheles

Tacheles redet, wer ohne Umschweife sagt, was ist. Dieses Skill macht aus einem deutschen Text den Text, den ein erfahrener Redakteur daraus gemacht hätte: verständlich, konkret, ohne Floskeln, in der gewünschten Dichte und, wenn gewünscht, in der Stimme eines bekannten Autors. Es ist ein Lektorat, keine Kürzungsmaschine. Der Redakteur streicht Leerlauf und behält jeden Gedanken.

Argumente: `$ARGUMENTS`

## Parameter lesen

Die Argumente sind frei kombinierbar. Lies sie so:

1. **Stufe**: eine Ziffer 1 bis 5. Fehlt sie, gilt **3**. Wörter wie „einfach“, „Leichte Sprache“, „für Kinder“ bedeuten 1, „knapp“ oder „Nachrichtenstil“ 2, „ausführlich“ oder „Essay“ 4, „literarisch“ oder „elaboriert“ 5.
2. **Stil**: ein Name aus `references/stile/` (siehe Tabelle unten). Fehlt er, arbeitest du als neutraler Redakteur nach `references/redakteur.md`. Wird ein Autor genannt, den es nicht als Profil gibt, sag das in einem Satz und arbeite ohne Stil weiter; erfinde kein Profil aus dem Gedächtnis.
3. **Text**: alles Übrige. Ist es ein Dateipfad, lies die Datei. Ist nichts angegeben, nimm den zuletzt besprochenen Text der Konversation. Gibt es keinen, frag in einem Satz nach dem Text.

Beispiele: `/tacheles 2` · `/tacheles 4 tucholsky` · `/tacheles 1 bericht.md` · `/tacheles kaestner Der folgende Text …`

## Das Grundgesetz

Diese Regeln gelten auf jeder Stufe und in jedem Stil. Stufe und Stil ändern Syntax, Dichte und Ton, nie diese Punkte:

- **Substanz bleibt.** Jede Zahl, jeder Name, jedes Zitat, jede Begründung, jedes Beispiel, jede echte Einschränkung des Originals steht auch im Ergebnis. Kürzen heißt Füllung entfernen, nicht Inhalt. Ein Text, der nach der Bearbeitung genauso lang ist, aber in jedem Satz etwas sagt, ist ein Erfolg.
- **Nichts erfinden.** Keine Zahl, kein Detail, kein Zitat, das nicht im Original steht. Wo ein Wert fehlt, den der Text bräuchte, steht `[PRÜFEN: …]`.
- **Der Handelnde steht im Satz.** Passiv und Nominalstil nur, wenn der Täter unbekannt oder unwichtig ist.
- **Kein Slop.** Nichts aus `references/floskeln.txt`, kein Muster aus `references/slop.md`. Das gilt auch auf Stufe 5: Elaboriert heißt reich an Gedanken, nicht reich an Wörtern.
- **Der Autor bleibt hörbar.** Eine eigenwillige Formulierung des Originals ist kein Slop. Slop ist das Generische. Nur ein gewählter Stil darf die Stimme überlagern.
- **Wertungen des Autors bleiben.** „Wir sind auf einem guten Weg“ ist eine Aussage des Autors, keine Floskel. Sie bleibt, ohne Etikett wie „Fazit:“ davor. Nur der Redakteur fügt keine eigene Wertung hinzu.
- **Länge folgt Inhalt.** Es gibt keine Kürzungsquote und keine Zielwortzahl. Ein Ergebnis unter 60 Prozent der Originallänge ist verdächtig, nicht verdienstvoll.

## Die fünf Stufen

Die Stufe bestimmt, für wen der Text geschrieben ist und wie viel er dem Leser pro Satz zumutet. Details, Zielwerte und die Probe auf jeder Stufe stehen in `references/stufen.md`. Lies die Datei, bevor du zum ersten Mal in einer Konversation umschreibst.

| Stufe | Name | Leser | Satz | Kennzeichen |
|---|---|---|---|---|
| 1 | einfach | alle, auch mit wenig Deutsch oder wenig Zeit | Ø 6–10 Wörter, max. 14 | ein Gedanke pro Satz, keine Nebensätze außer weil/wenn/dass, kein Passiv, keine Fremdwörter ohne Erklärung |
| 2 | klar | Zeitungsleser, Kunden, Kollegen | Ø 9–14, max. 22 | Nachrichtenstil, Hauptsache im Hauptsatz, höchstens ein Nebensatz, Verben statt Substantive |
| 3 | sachlich | gebildete Laien, Entscheider, Fachkollegen | Ø 12–17, max. 30 | Qualitätsjournalismus und gutes Sachbuch, Nebensätze wo sie Logik tragen, Fachbegriffe konsistent |
| 4 | ausführlich | Leser, die Herleitung wollen | Ø 15–21, max. 36 | Essay und Analyse, Gegenargumente und Einschränkungen ausformuliert, Perioden erlaubt, wenn sauber gebaut |
| 5 | elaboriert | Leser, die Sprache genießen | Ø 18–30, max. 50 | literarische oder akademisch gehobene Prosa, Rhythmus, Parenthesen, präzise Fremdwörter, dennoch kein Wort ohne Arbeit |

Die Stufe ist keine Längenvorgabe. Stufe 1 erklärt oft mehr Wörter lang als Stufe 3, weil sie jeden Fachbegriff auflöst. Stufe 5 darf lange Sätze bauen, nicht leere.

## Die Stile

Ein Stil ist die Stimme eines Autors, übertragen auf Sachtexte. Jedes Profil hat operationale Regeln, Karikatur-Fallen und die Probe. Lies das Profil vollständig, bevor du in dem Stil schreibst. Die Zielwerte im Kopf des Profils haben Vorrang vor denen der Stufe; das Messskript übernimmt sie mit `--stil`. Die Stufe bestimmt dann noch Erklärtiefe, Herleitung und Wortschatz. Ein Stil, der von Ironie oder Zuspitzung lebt, darf beides einsetzen; das Ironieverbot der Stufen gilt nur ohne Stil. Steht die gewünschte Stufe außerhalb der empfohlenen, wende den Stil trotzdem an und nenne die Spannung in der Redaktionsnotiz.

| Name | Autor | Stufen | Kurz |
|---|---|---|---|
| `schneider` | Wolf Schneider | 1–3 | Verben, Einsilber, Hauptsätze, Konkretes. Das Handwerk in Reinform. |
| `kaestner` | Erich Kästner | 1–3 | Klar, warm, leise ironisch. Sagt schwere Dinge einfach, ohne sie kleinzureden. |
| `tucholsky` | Kurt Tucholsky | 2–4 | Feuilleton mit Haltung: Hauptsätze, Anrede, Pointe, Zorn mit Witz. |
| `kisch` | Egon Erwin Kisch | 2–4 | Reportage: Präsens, Szene statt Behauptung, eine Leitmetapher, das Urteil am Schluss. |
| `kafka` | Franz Kafka | 3–4 | Nüchterne Präzision, lange lineare Sätze, Kanzleisprache ohne Kanzleigeist. |
| `fontane` | Theodor Fontane | 3–4 | Plauderton, „aber“-Urteile, Understatement; das Beiläufige trägt die Pointe. |
| `mann` | Thomas Mann | 4–5 | Ironische Perioden, Parenthesen, Leitmotiv, Feierlichkeit leicht unterlaufen. |
| `bernhard` | Thomas Bernhard | 4–5 | Wiederholung, Übertreibung, der eine lange Atemzug. Für Polemik, nicht für Protokolle. |

## Verfahren

Arbeite immer in dieser Reihenfolge. Die Reihenfolge ist der Grund, warum das Ergebnis zuverlässig ist: Das Inventar schützt die Substanz, die Messung schützt die Form.

**1. Parameter festlegen.** Stufe, Stil, Text, und die **Textsorte**: Nachricht, Bericht, Reportage, Kommentar, Glosse, Essay, E-Mail, Anleitung (`references/textsorten.md` sagt, was jede verlangt). Bei Unklarheit den wahrscheinlichsten Fall wählen und in der Notiz nennen, nicht nachfragen.

**2. Lesen und Inventar anlegen.** Vor dem ersten neuen Satz: Was will der Text, wer liest ihn, was muss er wissen? Dann eine Liste der Substanz: alle Zahlen, Namen, Daten, Zitate, Quellen; jede Begründung („weil“, „da“, „deshalb“); jedes Beispiel; jede echte Einschränkung; jede Wertung des Autors; jede Formulierung, die nach ihm klingt. Bei Texten über etwa 300 Wörter schreibst du das Inventar in eine Datei im Arbeitsverzeichnis, damit es beim Abgleich in Schritt 6 nicht aus dem Gedächtnis kommen muss; darunter reicht es im Kopf.

**3. Diagnose.** Lies `references/slop.md`, wenn du es in dieser Konversation noch nicht getan hast. Markiere im Original die Muster, die du siehst: Floskeln, Bedeutungsbehauptungen, Nominalketten, Passiv ohne Grund, Binärkontraste, Metakommentare, Rhythmus-Tells, Formatierungs-Tells. Das ist Redakteursarbeit, keine Ausgabe; nur bei langen Texten wird die Diagnose Teil der Analyse-Stufe.

**4. Umschreiben.** Nach `references/stufen.md` für die Stufe, nach `references/redakteur.md` für das Handwerk am Satz und Wort, nach `references/stilistik.md` für das, was den Text als Ganzes menschlich macht (Verkettung der Sätze, wechselndes Vorfeld, Streuung, Konkretion, Standpunkt), und nach dem Stilprofil, falls eines gewählt ist. Lies `stilistik.md` beim ersten Einsatz in einer Konversation; die Floskelliste fängt Slop, diese Datei verhindert, dass ein floskelfreier Text trotzdem generisch klingt. Schreibe den ganzen Text neu, Satz für Satz, Absatz für Absatz, lückenlos. Keine Platzhalter wie „[Rest unverändert]“.

**5. Messen.** Schreib Original und Ergebnis in Dateien und miss:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/messen.py --stufe N [--stil NAME] --vergleich original.txt ergebnis.txt
```

Das Skript meldet **Verstöße** (Satzlänge, Floskeln, Nominal- und Passivdichte, Streckverben, fehlende Zahlen und Zitate, Überkürzung) und **Hinweise** (Passiv-Verdacht, Modewörter im Kontext, Rhythmus, Namen). Verstöße behebst du und misst erneut; nach spätestens zwei Nachbesserungsrunden ist Schluss. Hinweise prüfst du mit Redakteursblick, ohne Pflicht zur erneuten Messung: Ein Fachbegriff, ein begründetes Passiv, ein bewusst gesetzter Rhythmus, ein Wort des Autors dürfen bleiben. Bleibt ein Verstoß, den du für richtig hältst, nenne ihn in der Notiz mit Grund. Wortzahlen in der Notiz sind die des Skripts (es zählt Wörter mit Buchstaben, keine Ziffern und kein Markdown).

**6. Stilprüfung und Substanzabgleich.** Erst die sieben Fragen der Stilprüfung am Ende von `references/stilistik.md`, Absatz für Absatz: Textsorte erkennbar, Sätze verkettet, Vorfeld wechselnd, Längen gestreut, ein konkretes Datum je Absatz, Konnektoren nur mit Logik, Stimme des Autors hörbar. Jedes Nein ist eine Stelle zum Umbauen. Dann das Inventar aus Schritt 2: Fehlt etwas, füge es wieder ein, auch wenn der Text dadurch länger wird. Klingt der Text nach einem Protokoll, hole eine erhaltene Formulierung des Originals zurück.

**7. Ausgabe.** Erst der Text, vollständig. Dann eine **Redaktionsnotiz** von fünf bis zehn Zeilen: Stufe und Stil; die zwei oder drei dominanten Muster, die du entfernt hast; was du bewusst erhalten hast, obwohl es Slop ähnelte; offene `[PRÜFEN]`-Punkte; eine Zeile Messwerte (Wörter vorher/nachher, mittlere Satzlänge, Verstöße). Keine Kürzungsprozente als Erfolgsmeldung.

Die Referenzen im Überblick: `stufen.md` (Dichte), `redakteur.md` (Handwerk am Satz und Wort), `stilistik.md` (der Text als Ganzes), `textsorten.md` (was Nachricht, Reportage, Kommentar und die anderen verlangen), `slop.md` und `floskeln.txt` (was raus muss), `stile/` (die Stimmen). `probe.md` enthält die Vorlage, an der alle Stufen und Stile ihre Probe zeigen; sie ist zum Vergleichen da, keine Pflichtlektüre.

## Lange Texte

Ab etwa 800 Wörtern arbeitest du zweistufig, damit nichts verloren geht und die Regeltreue zum Ende nicht nachlässt.

*Analyse:* Abschnittsinventar (alle Abschnitte, nummeriert), pro Abschnitt eine kurze Befundliste mit wörtlich zitierten Fundstellen und eine Spalte „Bleibt erhalten“ für Begründungen, Beispiele, Zahlen. Kein umgeschriebener Text in dieser Stufe. Abschluss: „Analyse abgeschlossen. Schreibe ‚weiter‘ für die Überarbeitung.“

*Umsetzung:* Abschnitt für Abschnitt in Reihenfolge, lückenlos, nach jedem Abschnitt eine Kontrollzeile `[Abschnitt X · entfernt: … · erhalten: …]`. Messung am Ende über den ganzen Text.

Sagt der Auftraggeber „einfach machen“ oder „ohne Rückfrage“, überspringst du die Pause zwischen Analyse und Umsetzung, nicht die Analyse.

## Was tacheles nicht tut

- Es übersetzt nicht und ändert die Sprache nicht. Englische Fachtermini, die im Fach etabliert sind, bleiben.
- Es kürzt nicht auf Quote. Es gibt keine „möglichst kurz“-Einstellung; Stufe 1 ist einfach, nicht knapp.
- Es erfindet keine Anschaulichkeit. Konkret wird nur, was das Original hergibt.
- Es karikiert keinen Autor. Ein Stil ist eine Haltung und ein Satzbau, keine Sammlung von Manierismen. Wer Bernhard liest, soll Bernhard hören, nicht eine Parodie.
- Es formatiert nicht auf. Fett höchstens zweimal pro Absatz, Listen nur für echte Aufzählungen ab drei gleichrangigen Punkten, keine Emoji, keine Trennlinien, keine Überschriften als Frage.
