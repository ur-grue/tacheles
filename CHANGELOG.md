# Änderungen

Das Format folgt [Keep a Changelog](https://keepachangelog.com/de/1.1.0/),
die Nummern folgen [Semantic Versioning](https://semver.org/lang/de/).

## 1.2.0 — 2026-09-15

### Neu
- `evals/`: sechs Eingangstexte aus der Praxis (Lokalbericht, Entscheidungsvorlage,
  Exposé, Rede, Newsletter, lange E-Mail), jeder mit einem Inventar seiner Substanz.
- `evals/bewerten.py` benotet jeden Lauf mit sieben Prüfungen und schreibt
  `grading.json` je Lauf.
- Die zwölf Ergebnisse von Lauf 1 liegen in `evals/ergebnisse/`.

### Behoben
- Der Nominalisierungszähler in `messen.py` verbuchte Buchtitel als Nominalstil.
  Zitate und Werktitel zählen nicht mehr mit, die Ausnahmeliste hat 24 Einträge mehr.

### Geändert
- `tests/`: 43 → 46 Tests.
- README: Abschnitt „Nachweis“ mit dem Ergebnis von Lauf 1.

## 1.1.0 — 2026-09-08

### Behoben
- Regex-Bug im Singular.
- Falscher Handlungsträger: Prüfung nachgerüstet.
- Vier veraltete Doku-Stellen.

### Geändert
- README mit tacheles auf Stufe 3 redigiert.

## 1.0.0 — 2026-09-08

Erste Fassung: Skill, Messskript, Floskelliste, acht Stilprofile,
fünf Stufen, Plugin-Manifest, CI.
