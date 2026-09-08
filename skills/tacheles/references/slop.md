# Slop: die Muster

Slop ist Text, der nach Text klingt, ohne etwas zu sagen. Er entsteht, wenn ein Sprachmodell oder ein müder Mensch die Form eines Gedankens erzeugt, ohne den Gedanken zu haben. Die Wortliste dazu liegt in `floskeln.txt`; diese Datei beschreibt die Strukturen, die keine Wortliste erfasst.

Zur Beleglage: Die Muster stammen aus den Wikipedia-Projektseiten zu KI-generierten Texten (deutsch und englisch), aus Praxislisten deutscher Lektorate und aus zwei empirischen Studien zu deutschen Texten (Juzek 2026, 34 Sprachen: Betonungsverben wie „betonen“, „hervorheben“, Bedeutungsnomen, Innovationsadjektive und Konnektoren wie „zudem“, „insbesondere“ sind in KI-Texten um das Zehn- bis Dreißigfache überrepräsentiert; Irrgang u. a. 2024, TU Berlin: mehr wiederholte Lemmata, höhere Satzähnlichkeit, mehr Adverbien je Verb, mehr Fremdwörter). Was nur Folklore ist, steht am Ende.

Für jedes Muster gilt dieselbe Regel: Die Aussage bleibt, wenn sie eine hat. Ersatzlos gestrichen wird nur, was keine hat.

## 1. Bedeutungsbehauptungen

Der Text behauptet, dass etwas wichtig ist, statt zu zeigen, wofür.

| Muster | Was tun |
|---|---|
| „spielt eine entscheidende Rolle“, „ist von zentraler Bedeutung“, „wichtiger denn je“ | Wofür? Die Konsequenz schreiben: „Ohne X scheitert Y.“ Gibt es keine, streichen. |
| „…, was die Bedeutung von X unterstreicht“ (Alibi-Nachsatz) | Streichen, oder die Bedeutung konkret machen: Was folgt daraus, für wen, bis wann? |
| „markiert einen Wendepunkt“, „Meilenstein“, „Gamechanger“, „Paradigmenwechsel“ | Was ist danach anders als davor? Das schreiben. |
| „eröffnet neue Möglichkeiten“, „wertvolle Einblicke“, „volles Potenzial“ | Die Möglichkeiten benennen oder streichen. |
| „steht als Zeugnis für“, „bleibendes Vermächtnis“, „tief verwurzelt“ | Enzyklopädie-Slop. Den Fakt behalten, die Weihe streichen. |
| „…, seine Bedeutung hervorhebend“ (Partizip-Anhängsel) | Eigener Satz mit Inhalt, oder weg. Deutsche Sachprosa hängt keine Partizipien an. |

Testfrage: Könnte derselbe Satz unter jedem beliebigen Absatz stehen? Dann ist er eine Behauptung, kein Inhalt.

## 2. Binärkontraste und negative Parallelismen

Verneinung, dann Behauptung. Erzeugt Dramatik aus nichts.

| Muster | Was tun |
|---|---|
| „Nicht X, sondern Y“ · „Es geht nicht um X, es geht um Y“ · „Die Frage ist nicht X. Die Frage ist Y.“ | Y sagen. Wenn die Abgrenzung zu X echte Information ist (ein Missverständnis ausräumen), als eigener Satz: „Y. X spielt keine Rolle, weil …“ |
| „Nicht nur X, sondern auch Y“ | „X und Y.“ Oder gewichten: „Vor allem Y, daneben X.“ |
| „Weniger X, mehr Y“ · „X ist tot, es lebe Y“ | Konkret: Was ändert sich, für wen? |
| „Kein X. Kein Y. Sondern Z.“ | Z sagen. Der Leser braucht keine Startbahn. |

## 3. Falsche Handlungsträger

Unbelebtes bekommt menschliche Verben. Das Muster versteckt, wer handelt.

| Muster | Was tun |
|---|---|
| „Die Entscheidung entsteht / reift“ | Wer entscheidet? „Die Redaktion entscheidet im März.“ |
| „Die Daten zeigen uns“, „Die Studie betont“ | Wer hat ausgewertet? „Aus den Daten lesen wir …“ |
| „Der Markt belohnt“, „Das Projekt gewinnt an Fahrt“ | Wer kauft, wer zahlt, wer hat was beschleunigt? |
| „dient als“, „fungiert als“, „stellt … dar“, „verfügt über“ (Kopula-Vermeidung) | „ist“, „hat“. Das Modell meidet die einfache Kopula; der Redakteur nicht. |

Ausnahme: etablierte Fachsprache („der Kurs fällt“, „die Kosten steigen“) ist kein Slop.

## 4. Metakommentare und Rahmen

Der Text kündigt an, was er gleich sagt, oder kommentiert, dass er es gesagt hat.

| Muster | Was tun |
|---|---|
| „Es ist wichtig zu beachten, dass X“ · „Es sei erwähnt“ · „Interessanterweise“ | Rahmen löschen, X direkt sagen. |
| „Im Folgenden wird gezeigt“ · „Bevor wir zu X kommen“ · „Werfen wir einen Blick auf“ | Streichen. Der Text zeigt es einfach. |
| „Zusammenfassend lässt sich sagen“ · Abschnitt „Fazit“ | Die Schlussfolgerung ohne Etikett. Und nur, wenn sie Neues bringt (eine Handlung, eine offene Frage), nicht als Wiederholung. |
| Rhetorische Frage als Einstieg („Was bedeutet das?“, „Hand aufs Herz:“) | Mit der Antwort beginnen. |
| „Die gute Nachricht:“, „Der Punkt ist:“, „Und genau das macht den Unterschied.“ | Streichen. Das ist Inszenierung, nicht Inhalt. |
| Chatbot-Reste: „Natürlich!“, „Ich hoffe, das hilft“, „Wenn du magst, passe ich …“ | Streichen, ohne Ausnahme. |

## 5. Scheinbelege

| Muster | Was tun |
|---|---|
| „Studien zeigen“, „Experten sind sich einig“, „Beobachter“, „Kritiker argumentieren“ | Quelle mit Namen und Jahr, oder streichen. Empirisch ist „Experte“ eines der stärksten deutschen KI-Signale. |
| „Schätzungen zufolge“, „ein nicht unerheblicher Teil“, „immer mehr Menschen“ | Zahl aus dem Original. Keine Zahl: `[PRÜFEN: Quelle?]` |
| Erfundene Zitate, Buchtitel, Institutionen | Beim Lektorat: nichts ergänzen, was nicht im Original steht. Verdächtiges markieren. |

Beim Lektorat gilt: Die Aussage bleibt, der Beleg wird angefordert. „Sicherheitsexperten raten zu 2FA“ wird zu „Fachleute raten zu 2FA [PRÜFEN: Wer? Quelle?]“. Gestrichen wird der Scheinbeleg nur, wenn die Aussage ohne ihn nichts mehr sagt („Experten sehen großes Potenzial“).

## 6. Rhythmus-Tells

Das Modell schreibt gleichmäßig; Menschen schreiben ungleichmäßig.

| Muster | Was tun |
|---|---|
| Dreierfiguren als Ornament („schneller, günstiger, besser“; „Zeit, Fokus und Wohlbefinden“) | Nur, wenn jedes Glied eigene Information trägt. Sonst zwei Glieder oder eins. Die Zahl der Glieder variieren. |
| Anaphern, gleiche Satzanfänge („Dieser Ansatz … Diese Methode … Dieses Ergebnis …“) | Subjekt wechseln, Sätze verschmelzen, mit der Handlung beginnen. |
| Drei gleich lange Sätze in Folge; alle Absätze gleich lang | Einen Satz umbauen; verlängern ist so legitim wie kürzen. Absatzlänge folgt dem Inhalt. |
| Stakkato-Fragmente („Ein Wort. Mehr nicht.“) | Vollständige Sätze. |
| Jeder Absatz endet mit Pointe oder Einzeiler | Absatzenden variieren. Ein Absatz darf mit einem Detail enden. |
| Gedankenstrich-Inflation | Satz umbauen: Punkt, Komma, Doppelpunkt oder eigener Satz. Kein bloßer Zeichentausch. Der Geviertstrich ohne Leerzeichen (—) ist im Deutschen falsch. |
| Synonym-Rotation („Digital Detox“, „digitale Auszeit“, „Medienfasten“) | Ein Begriff, eine Sache. |
| „von X bis Y“ als Scheinweite („von Kunst bis Wissenschaft“) | Aufzählen oder streichen. |

## 7. Konnektoren-Inflation

Empirisch das deutlichste deutsche Signal: „zudem“, „insbesondere“, „dabei“, „daher“, „dennoch“, „stattdessen“, „vielmehr“, „weiterhin“, „gleichzeitig“ sind in KI-Texten zehn- bis zwanzigfach häufiger. Jeder einzelne ist erlaubt; die Dichte ist das Problem.

Was tun: Nur Konnektoren behalten, die eine logische Beziehung tragen („deshalb“, „trotzdem“, „dagegen“). Additive Konnektoren („zudem“, „darüber hinaus“, „außerdem“) meist streichen; der neue Satz reiht sich von selbst. Bemerkenswert: „allerdings“, „ferner“, „insgesamt“ sind keine KI-Signale, eher Menschenwörter.

## 8. Hedging-Kaskaden

| Slop (streichen) | Substanz (behalten) |
|---|---|
| „Es könnte durchaus sein, dass sich gewissermaßen Chancen ergeben dürften.“ | „Die Zulassung dürfte sich verzögern; das Amt hat noch nicht geantwortet.“ |
| Doppelte und dreifache Absicherung, „tendenziell eher“, „in gewisser Weise“ | Ein Marker je Aussage, mit erkennbarem Grund. |

Falsche Gewissheit ist der schwerere Fehler als ein Modalverb. Ein Hedge mit Grund bleibt.

## 9. Formatierungs-Tells

- Bullet-Inflation: Fließtext-Gedanken als Pseudoliste. Listen nur für echte Aufzählungen ab drei gleichrangigen Punkten.
- Fett und Doppelpunkt als Listenkopf („**Skalierbarkeit:** Das System wächst mit.“), Fettwüsten, gefettete Halbsätze. Höchstens zwei Fettungen je Absatz, und nur für Erstnennungen und entscheidungsrelevante Zahlen.
- Emoji, Trennlinien, Deko-Blockquotes.
- Überschriften-Inflation: eine Zwischenüberschrift über zwei Sätzen. Überschrift erst ab etwa 150 Wörtern Abschnitt.
- Doppelpunkt-Titel mit Enthüllung („Skalierung: Warum jetzt der richtige Zeitpunkt ist“) und Überschriften als Frage. Überschriften sind Aussagen oder Sachbezeichnungen. Ein sachlicher Doppelpunkt („Protokoll: Sitzung vom 3. März“) ist keiner.
- Title Case im Deutschen („Warum Diese Strategie Funktioniert“).
- Symmetrische Abschnitte: jeder exakt drei Absätze. Länge folgt Inhalt.

## 10. Denglische Konstruktionen

- Nachgestellte Partizipien und absolute Konstruktionen („Sie betrat den Raum, ihre Miene undurchdringlich“).
- Direkt übersetzte Rahmen („Es ist erwähnenswert, dass“, „keine Diskussion wäre vollständig ohne“).
- Bindestriche in Komposita, die im Deutschen zusammengeschrieben werden, außer auf Stufe 1.
- Lichtmetaphern und temperierte Gefühle („tauchte den Raum in goldenes Licht“, „ein Schatten von Sorge“) in Sachtexten.

## 11. Nominalstil und Papierdeutsch

Kein KI-Spezifikum, dieselbe Wirkung: Der Text klingt nach Textbaustein.

- „-ung“-Ketten: „Durchführung der Umsetzung der Maßnahmen“ wird zu „Wir setzen die Maßnahmen um.“
- „erfolgen“-Passiv: „Die Prüfung erfolgt durch X“ wird zu „X prüft.“
- Papierpräpositionen: „seitens“, „mittels“, „zwecks“, „bezüglich“, „im Rahmen von“, „im Zuge von“, „hinsichtlich“.
- „zeitnah“ wird zu einem Datum, „Thematik“ zu Thema, „zur Verfügung stellen“ zu geben oder liefern, „Berücksichtigung finden“ zu berücksichtigen.

## Was kein Slop ist

- **Ein Hedge mit Grund.** „Dürfte sich verzögern, weil …“ ist Information.
- **Ein logischer Übergang.** „Deshalb“, „trotzdem“, „im Gegensatz dazu“ tragen das Argument.
- **Ein Beispiel.** Es ist der Beleg der abstrakten Aussage, keine Redundanz.
- **Ein einzelnes Modewort im Fachkontext.** „Nachhaltig“ als ökologischer Begriff, „agil“ als Methode, „skalierbar“ mit Bezugsgröße, „robust“ als technische Eigenschaft.
- **Eine eigenwillige Formulierung des Autors.** Slop ist das Generische, nicht das Individuelle.
- **Kalkulierte Wiederholung** bei schwieriger Sache (Hamburger Modell: etwas Redundanz erwünscht).
- **Perfekte Grammatik, gehobener Ton, fehlende Rechtschreibfehler.** Die englische Wikipedia führt sie ausdrücklich als unwirksame Indikatoren. Ein Text ist nicht Slop, weil er sauber ist.

## Folklore

Diese Behauptungen kursieren, sind aber für Deutsch nicht belegt oder widerlegt: „Zeugnis“, „maßgeschneidert“, „Landschaft“, „Reise“, „Ebene“, „Dimension“ und „Vielzahl“ als sichere KI-Marker (in Nachrichtendaten unauffällig; nur im Marketing-Register verdächtig); „allerdings“, „ferner“, „insgesamt“ als KI-Wörter (eher das Gegenteil); Ich-Form oder Kontraktionen als Menschlichkeitsbeweis; Hilfsverbhäufung; feste Wortlisten als Detektor (sie altern binnen Monaten und funktionieren bei manchen Modellen kaum über Zufall). Deshalb entscheidet in tacheles nie ein einzelnes Wort, sondern der Redakteursblick auf den Satz: Sagt er etwas, und sagt er es so, dass der Leser es beim ersten Lesen versteht?
