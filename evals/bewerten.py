#!/usr/bin/env python3
"""
Benotet die Eval-Läufe gegen evals.json. Nur Standardbibliothek.

    python3 evals/bewerten.py <workspace>/iteration-N [--json]

Erwartete Ablage je Lauf:
    <workspace>/iteration-N/<eval-name>/<variante>/outputs/ergebnis.md

Jeder Lauf bekommt sieben Prüfungen, die das Skript alle selbst ausrechnet.
Die Redaktionsnotiz und die weichen Substanzpunkte stehen daneben, ungezählt:
Eine Notiz kann der Lauf ohne Skill nicht haben, und über sinngemäße
Erhaltung urteilt kein Zeichenvergleich.

Zur Substanzprüfung: Ein harter Punkt gilt als erhalten, wenn er wörtlich im
Text steht, wenn alle seine Bestandteile vorkommen („27 zu 19“ wird „27
Mitglieder stimmten dafür, 19 dagegen“) oder wenn jeder Bestandteil mit
toleranter Endung vorkommt („neun Monaten“ findet „neun Monate“). Punkte aus
substanz_weich zählt das Skript nicht, es listet sie nur: Ob „kostenlos“ als
„kostet nichts“ erhalten ist, kann ein Zeichenvergleich nicht entscheiden.
Diese Grenze gehört in die Eval, nicht ins Ergebnis.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MESSEN = os.path.join(WURZEL, "skills", "tacheles", "scripts", "messen.py")
VARIANTEN = ("with_skill", "without_skill")
VERBOTENE_KATEGORIEN = ("Einstiegsfloskeln", "Schlussfloskeln", "Bedeutungsbehauptungen",
                        "Metakommentare", "Buzzwords")

sys.path.insert(0, os.path.join(WURZEL, "skills", "tacheles", "scripts"))
import messen  # noqa: E402


def normalisieren(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("\u00a0", " ")).strip()


def _formen(wort: str) -> list[str]:
    """Das Wort und seine gekürzten Stämme, für tolerante Flexion.

    „Monaten“ liefert auch „Monat“, damit „neun Monaten“ im Ergebnis „neun
    Monate“ findet. Gekürzt wird nur, was aus Buchstaben besteht und lang
    genug ist: Zahlen und kurze Wörter müssen exakt stehen.
    """
    w = wort.lower()
    if len(w) >= 5 and w.isalpha():
        return [w, w[:-1], w[:-2], w[:-3]]
    return [w]


def substanz_gefunden(punkt: str, text: str) -> tuple[bool, str]:
    """(gefunden, art) – 'wörtlich', 'sinngemäß', 'flektiert' oder 'fehlt'."""
    t = normalisieren(text).lower()
    p = normalisieren(punkt)
    if p.lower() in t:
        return True, "wörtlich"
    teile = [x for x in re.split(r"[\s,]+", p) if len(x) > 1]
    if not teile:
        return False, "fehlt"
    if all(x.lower() in t for x in teile):
        return True, "sinngemäß"
    if all(any(f in t for f in _formen(x)) for x in teile):
        return True, "flektiert"
    return False, "fehlt"


def messung(ergebnis: str, quelle: str | None, stufe: int, stil: str | None) -> dict:
    argv = ["--stufe", str(stufe)]
    if stil:
        argv += ["--stil", stil]
    if quelle:
        argv += ["--vergleich", quelle]
    argv += ["--json", ergebnis]
    p = subprocess.run([sys.executable, MESSEN] + argv, capture_output=True, text=True)
    if p.returncode == 2 or not p.stdout.strip():
        raise RuntimeError(f"messen.py scheitert: {p.stderr.strip()[:200]}")
    return json.loads(p.stdout)


def pruefe(eval_def: dict, variante: str, lauf_dir: str, floskeln: dict,
           original: dict) -> dict:
    ergebnis_pfad = os.path.join(lauf_dir, "outputs", "ergebnis.md")
    if not os.path.exists(ergebnis_pfad):
        return {"variante": variante, "fehlt": True, "expectations": []}

    quelle = os.path.join(WURZEL, eval_def["datei"])
    text = open(ergebnis_pfad, encoding="utf-8").read()
    m = messung(ergebnis_pfad, quelle, eval_def["stufe"], eval_def.get("stil"))

    verstoesse = [b for b in m["befunde"] if b["art"] == "verstoss"]
    hinweise = [b for b in m["befunde"] if b["art"] == "hinweis"]
    zahl_fehlt = [b for b in verstoesse if "Zahlen aus dem Original fehlen" in b["text"]]
    zitat_fehlt = [b for b in verstoesse if "Zitat" in b["text"]]

    # Harte Substanzpunkte: benotet
    treffer = [(p, *substanz_gefunden(p, text)) for p in eval_def["substanz"]]
    fehlend = [p for p, ok, _ in treffer if not ok]
    abgeleitet = [p for p, ok, art in treffer if ok and art in ("sinngemäß", "flektiert")]

    # Weiche Substanzpunkte: nur gelistet, nicht benotet
    weich = [(p, *substanz_gefunden(p, text)) for p in eval_def.get("substanz_weich", [])]
    weich_offen = [p for p, ok, _ in weich if not ok]

    # Verbotene Floskelkategorien
    gefundene_floskeln = []
    for kat in VERBOTENE_KATEGORIEN:
        for ph in floskeln.get(kat, []):
            if messen.phrase_zu_regex(ph).search(text):
                gefundene_floskeln.append(f"{kat}: {ph}")

    # Redaktionsnotiz
    notiz_pfad = os.path.join(lauf_dir, "outputs", "notiz.md")
    notiz = open(notiz_pfad, encoding="utf-8").read() if os.path.exists(notiz_pfad) else ""

    e = []

    def add(text_, passed, evidence):
        e.append({"text": text_, "passed": bool(passed), "evidence": evidence})

    add(f"Null Verstöße auf Stufe {eval_def['stufe']}", not verstoesse,
        "keine" if not verstoesse else "; ".join(b["text"][:110] for b in verstoesse[:4]))
    add("Keine Zahl des Originals fehlt", not zahl_fehlt,
        "keine" if not zahl_fehlt else zahl_fehlt[0]["text"][:160])
    add("Kein Zitat verändert oder entfernt", not zitat_fehlt,
        "keine" if not zitat_fehlt else zitat_fehlt[0]["text"][:160])
    add(f"Alle {len(eval_def['substanz'])} harten Substanzpunkte erhalten", not fehlend,
        ("alle" + (f", davon {len(abgeleitet)} umformuliert" if abgeleitet else ""))
        if not fehlend else f"{len(fehlend)} fehlen: " + ", ".join(fehlend[:8]))
    add("Keine Floskel aus den verbotenen Kategorien", not gefundene_floskeln,
        "keine" if not gefundene_floskeln else "; ".join(gefundene_floskeln[:6]))
    lo, hi = m["ziele"]["satz_avg"]
    im_korridor = lo <= m["satz_avg"] <= hi
    add(f"Mittlere Satzlänge im Zielkorridor {lo}\u2013{hi} Wörter", im_korridor,
        f"Ø {m['satz_avg']}"
        + ("" if im_korridor else " – die verlangte Stufe ist nicht getroffen"))

    anteil = 100 * m["woerter"] / original["woerter"] if original["woerter"] else 0
    laenge_ok = 67 <= anteil <= 133
    add("Länge zwischen 67 und 133 Prozent des Originals", laenge_ok,
        f"{anteil:.0f} Prozent ({m['woerter']} von {original['woerter']} Wörtern)"
        + ("" if laenge_ok else
           " – gekürzt bis zum Substanzverlust" if anteil < 67 else " – aufgeblasen"))

    return {
        "variante": variante,
        "fehlt": False,
        "expectations": e,
        "bestanden": sum(1 for x in e if x["passed"]),
        "gesamt": len(e),
        "weich_offen": weich_offen,
        "notiz_woerter": len(notiz.split()),
        "messwerte": {
            "woerter": m["woerter"], "saetze": m["saetze"],
            "satz_avg": m["satz_avg"], "satz_max": m["satz_max"],
            "flesch": m["flesch"], "passiv": m["passiv"],
            "nominal_pro100": round(100 * m["nominal"] / m["woerter"], 1) if m["woerter"] else 0,
            "verstoesse": len(verstoesse), "hinweise": len(hinweise),
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    defs = json.load(open(os.path.join(WURZEL, "evals", "evals.json"), encoding="utf-8"))
    floskeln = messen.floskeln_laden(os.path.join(WURZEL, "skills", "tacheles",
                                                  "references", "floskeln.txt"))
    bericht = {"evals": []}

    for ed in defs["evals"]:
        eintrag = {"id": ed["id"], "name": ed["name"], "textsorte": ed["textsorte"],
                   "stufe": ed["stufe"], "stil": ed.get("stil"), "laeufe": []}
        original = messung(os.path.join(WURZEL, ed["datei"]), None,
                           ed["stufe"], ed.get("stil"))
        for v in VARIANTEN:
            lauf_dir = os.path.join(a.workspace, f"{ed['id']}-{ed['name']}", v)
            if not os.path.isdir(lauf_dir):
                continue
            r = pruefe(ed, v, lauf_dir, floskeln, original)
            eintrag["laeufe"].append(r)
            if not r["fehlt"]:
                os.makedirs(lauf_dir, exist_ok=True)
                with open(os.path.join(lauf_dir, "grading.json"), "w", encoding="utf-8") as f:
                    json.dump({
                        "summary": {"pass_rate": round(r["bestanden"] / r["gesamt"], 4)},
                        "expectations": r["expectations"],
                    }, f, ensure_ascii=False, indent=2)
        bericht["evals"].append(eintrag)

    if a.json:
        print(json.dumps(bericht, ensure_ascii=False, indent=2))
        return 0

    print("TACHELES · Eval-Benotung")
    print("=" * 78)
    summen = {v: [0, 0] for v in VARIANTEN}
    for e in bericht["evals"]:
        kopf = f"{e['id']} {e['name']} · {e['textsorte']} · Stufe {e['stufe']}"
        print(f"\n{kopf}" + (f" · Stil {e['stil']}" if e["stil"] else ""))
        print("-" * 78)
        for r in e["laeufe"]:
            if r["fehlt"]:
                print(f"  {r['variante']:14} kein ergebnis.md")
                continue
            w = r["messwerte"]
            summen[r["variante"]][0] += r["bestanden"]
            summen[r["variante"]][1] += r["gesamt"]
            print(f"  {r['variante']:14} {r['bestanden']}/{r['gesamt']} Prüfungen · "
                  f"{w['woerter']} Wörter · Ø {w['satz_avg']} · längster {w['satz_max']} · "
                  f"Flesch {w['flesch']} · Verstöße {w['verstoesse']}")
            for x in r["expectations"]:
                if not x["passed"]:
                    print(f"       ✗ {x['text']}: {x['evidence']}")
            if r["variante"] == "with_skill":
                print(f"       · Redaktionsnotiz: "
                      + (f"{r['notiz_woerter']} Wörter" if r["notiz_woerter"] else "fehlt"))
            if r["weich_offen"]:
                print("       · vom Leser zu prüfen (nicht benotet): "
                      + ", ".join(r["weich_offen"]))
    print("\n" + "=" * 78)
    for v in VARIANTEN:
        b, g = summen[v]
        quote = f"{100 * b / g:.0f} %" if g else "—"
        print(f"{v:14} {b}/{g} Prüfungen bestanden ({quote})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
