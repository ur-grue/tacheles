# Evals

Sechs Textsorten, zwölf Läufe, sieben Prüfungen je Lauf. Die Evals messen, ob
tacheles hält, was es verspricht: Slop raus, Substanz drin, verlangte Stufe
getroffen. Jeder Fall läuft zweimal: einmal mit Skill, einmal ohne. Der Lauf
ohne Skill ist die Vergleichsgröße: Was ein Modell ohne Anleitung schon kann,
ist kein Verdienst des Skills.

## Aufruf

```bash
# 1. Läufe erzeugen: je Eval ein Durchgang mit Skill, einer ohne
#    Ablage: <workspace>/<id>-<name>/{with_skill,without_skill}/outputs/ergebnis.md
# 2. Benoten
python3 evals/bewerten.py <workspace>
```

Das Skript braucht nur die Standardbibliothek. Es ruft `messen.py` auf, prüft
die Substanzpunkte aus `evals.json` und schreibt je Lauf eine `grading.json`.

## Die sechs Fälle

| # | Textsorte | Stufe | Stil | Probe |
|---|-----------|-------|------|-------|
| 1 | Lokalbericht | 2 | ohne | Behördendeutsch, Passiv ohne Täter, ein Zitat, eine Gegenstimme |
| 2 | Entscheidungsvorlage | 3 | ohne | Beratersprache, ein Widerspruch zwischen Empfehlung und Risiko |
| 3 | Exposé | 4 | ohne | Pitch-Floskeln, drei Figuren, eine Finanzierungslücke |
| 4 | Rede | 3 | kaestner | Festredenfloskeln, eine schlechte Nachricht, ein Stilprofil |
| 5 | Newsletter | 2 | ohne | Marketingsprache, Emoji, acht Termine und Preise als Nutzwert |
| 6 | lange E-Mail | 3 | ohne | Weichmacher, Verantwortungsvermeidung, eine unangenehme Ursache |

Die Eingangstexte stehen in `texte/`, jeder mit echter Substanz und echtem
Slop. Dazu listet `evals.json` je Fall die Substanzpunkte, die im Ergebnis
stehen müssen. Es nennt auch die Fallen, in die ein Lektorat tappen kann.

## Die sieben Prüfungen

1. Null Verstöße auf der Zielstufe
2. Keine Zahl des Originals fehlt
3. Kein Zitat verändert oder verschwunden
4. Jeder harte Substanzpunkt steht im Ergebnis, Flexion toleriert
5. Keine Floskel aus den fünf verbotenen Kategorien der `floskeln.txt`
6. Die mittlere Satzlänge liegt im Zielkorridor der Stufe, bei gesetztem Stil
   in dem des Profils
7. Die Länge liegt zwischen 67 und 133 Prozent des Originals

Nicht benotet, nur gelistet: die Redaktionsnotiz, weil der Lauf ohne Skill
keine haben kann, und die weichen Substanzpunkte, weil kein Zeichenvergleich
entscheidet, ob „kostenlos“ als „kostet nichts“ erhalten ist.

## Lauf 1

| # | Textsorte | mit Skill | ohne Skill | Ø Satz mit / ohne | Korridor |
|---|-----------|-----------|------------|-------------------|----------|
| 1 | Lokalbericht | 7/7 | 6/7 | 10,2 / 8,7 | 9–14 |
| 2 | Entscheidungsvorlage | 7/7 | 5/7 | 12,3 / 9,2 | 12–17 |
| 3 | Exposé | 7/7 | 6/7 | 15,6 / 15,4 | 15–21 |
| 4 | Rede (Kästner) | 7/7 | 7/7 | 7,0 / 10,8 | 7–14 |
| 5 | Newsletter | 7/7 | 4/7 | 9,0 / 7,3 | 9–14 |
| 6 | lange E-Mail | 7/7 | 6/7 | 13,2 / 9,3 | 12–17 |
| | **Summe** | **42/42** | **34/42** | | |

Der Unterschied liegt nicht beim Slop: Floskeln streicht ein Modell auch ohne
Anleitung. Er liegt bei der Stufe und bei der Länge. Ohne Skill verfehlen vier
von sechs Läufen den verlangten Korridor, alle vier nach unten: Das Modell
schreibt kurz, weil kurz als gut gilt, nicht weil Stufe 3 es verlangt. Zwei
Läufe kürzen auf 64 und 67 Prozent, einer bläht auf 142 Prozent auf. Beides
ist der Punkt, an dem Substanz verloren geht oder Erfundenes hinzukommt.

## Was Lauf 1 am Werkzeug gefunden hat

Zwei Defekte, beide außerhalb der Ergebnisse:

**Das Benotungsskript meldete vier Substanzlücken, die keine waren.** Es
verglich Zeichenketten: „zwei Enthaltungen“ gegen „zwei enthielten sich“,
„neun Monaten“ gegen „neun Monate“. Jetzt toleriert der Vergleich Flexion. Was
er nicht entscheiden kann, steht in `substanz_weich` und wird gelistet statt
benotet.

**Der Nominalisierungszähler in `messen.py` zählte Buchtitel mit.** Er
verbuchte „Die Erfindung des Ungehorsams“ als Nominalstil des Absenders, dazu
„Buchhandlung“, „Lieferungen“ und „Fertigung“. Diese Wörter benennen eine
Sache, ein Haus oder eine Abteilung, keine Verbhandlung. Zitate und Werktitel
zählt das Skript jetzt nicht mehr mit, die Ausnahmeliste ist länger geworden,
drei Tests halten das fest.

Der zweite Fund hebt die Quote mit Skill von 41 auf 42 von 42. Die Eval hat
also nicht nur gemessen, sie hat das Messgerät korrigiert. Die Zahl danach
ist zum Teil Ergebnis dieser Korrektur. Wer die Quote liest, soll das
mitlesen.

## Grenzen

Ein Lauf je Variante zeigt eine Richtung, keine Streuung. Die Längenspanne 67
bis 133 Prozent ist eine Faustregel, keine Messung; Läufe dicht an der Grenze
muss ein Mensch lesen. Und keine der sieben Prüfungen beurteilt, ob der Text
gut klingt. Das bleibt beim Leser, dafür liegen die zwölf Ergebnisse in
`ergebnisse/`.
