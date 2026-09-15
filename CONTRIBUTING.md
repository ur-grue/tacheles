# Mitmachen

Zwei Beiträge helfen mehr als alle anderen: eine fehlende Floskel und ein falscher Alarm.
Für beide braucht es keine Zeile Python.

## Eine Floskel fehlt

Die Liste steht in [`skills/tacheles/references/floskeln.txt`](skills/tacheles/references/floskeln.txt).
Es ist eine Textdatei, kein Code. Skill und Messskript lesen dieselbe Datei.

Eine Phrase pro Zeile, in den passenden Abschnitt. `…` steht für ein bis fünf beliebige Wörter,
Groß- und Kleinschreibung ist egal:

```
[Bedeutungsbehauptungen]
spielt eine … rolle
```

Welcher Abschnitt, entscheidet eine Frage: **Kann diese Phrase in irgendeinem Zusammenhang
Information tragen?**

- **Nein, nie** → `[Einstiegsfloskeln]`, `[Schlussfloskeln]`, `[Bedeutungsbehauptungen]`,
  `[Metakommentare]`, `[Buzzwords]`, `[Scheinbelege]`, `[Chatbot-Reste]`. Das gibt einen **Verstoß**,
  den das Skill nachbessern muss.
- **Ja, manchmal** → ein Abschnitt, dessen Name mit `Füll` oder `Kontext` beginnt. Das gibt einen
  **Hinweis**, über den der Redakteur entscheidet. „Nachhaltig“ gehört hierher: In einem Text über
  Forstwirtschaft ist es ein Fachbegriff, in einem Werbetext ein Füllwort.

Im Zweifel: Hinweis. Ein falscher Verstoß ärgert mehr als ein übersehener.

Nach dem Eintrag:

```bash
python3 -m unittest discover -s tests
python3 skills/tacheles/scripts/messen.py --stufe 3 irgendein-text.md
```

## Falscher Alarm

Wenn das Skript etwas anstreicht, was keiner ist, ist das ein Fehler im Werkzeug — kein
Bedienfehler. Die beiden zuletzt gefundenen kamen aus den Evals: Der Nominalisierungszähler hielt
den Buchtitel „Die Erfindung des Ungehorsams“ für Nominalstil, und „Buchhandlung“ für eine
Handlung. Beides ist repariert, beides steht jetzt als Test in
[`tests/test_messen.py`](tests/test_messen.py).

Ein guter Fehlerbericht enthält den Satz, der falsch angestrichen wurde, den Befehl und die
Ausgabe. Die [Vorlage](.github/ISSUE_TEMPLATE/falscher-alarm.yml) fragt genau das ab.

Wer den Fehler selbst beheben will: Zu jeder Korrektur gehört ein Test, der ohne sie fehlschlägt.

## Ein Stilprofil

Wie ein Profil aufgebaut ist, steht im [README](README.md#einen-eigenen-stil-ergänzen). Drei Dinge
entscheiden, ob es taugt: operationale Regeln statt Adjektive („Hauptsätze, Anrede, Pointe“ statt
„lebendig“), Karikatur-Fallen, damit aus dem Stil keine Parodie wird, und Quellen für die Regeln.
Die Tests prüfen jedes neue Profil auf Aufbau und plausible Schwellen.

## Tests

```bash
python3 -m unittest discover -s tests    # 46 Tests, keine Abhängigkeiten
```

Die CI läuft auf Python 3.10 und 3.13. Beide müssen grün sein.

## Der Ton

Das Repo hält sich an das, was es predigt: Das README ist mit tacheles auf Stufe 3 redigiert.
Wer Prosa beisteuert, kann sie messen lassen:

```bash
python3 skills/tacheles/scripts/messen.py --stufe 3 README.md
```

Tabellen und Listen zählt das Skript als Sätze; ein paar Meldungen sind dort normal.
