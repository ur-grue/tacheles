#!/usr/bin/env python3
"""
tacheles · messen.py — misst einen deutschen Text gegen die Zielwerte einer Stufe.

Nur Standardbibliothek. Keine Abhängigkeiten.

Aufruf:
    python3 messen.py [--stufe N] [--stil NAME] [--vergleich ORIGINAL] [--json] [DATEI | -]

    DATEI       Textdatei (UTF-8). Ohne Angabe oder "-" wird von stdin gelesen.
    --stufe N   1 (einfach) … 5 (elaboriert). Standard: 3.
    --stil NAME lädt Schwellen-Überschreibungen aus references/stile/NAME.md
    --vergleich ORIGINAL  Substanzabgleich: Zahlen, Zitate, Namen, Länge gegen das Original.
    --json      Maschinenlesbare Ausgabe.
    --liste     Zeigt die geladene Floskelliste und endet.

Rückgabewert: 0 ohne Verstöße, 1 mit Verstößen, 2 bei Bedienfehlern.

Alle Werte sind Heuristiken. Silben, Passiv und Nominalstil werden ohne
Wörterbuch geschätzt. Das Skript ersetzt keinen Redakteur; es zeigt ihm,
wo er hinsehen muss.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import signal
import statistics
import sys
from dataclasses import dataclass, field

HIER = os.path.dirname(os.path.abspath(__file__))
REFERENZEN = os.path.join(HIER, "..", "references")

# ---------------------------------------------------------------------------
# Stufen: Zielwerte
# ---------------------------------------------------------------------------
# satz_avg: Korridor für die mittlere Satzlänge (Wörter). Unterschreiten ist
#           nur ein Hinweis, Überschreiten ein Verstoß.
# satz_max: kein Satz länger als das (Verstoß).
# lang_anteil: höchstens dieser Anteil der Sätze darf über satz_lang liegen.
# passiv, nominal: je 100 Wörter (Verstoß bei Überschreitung).
# flesch_min: Flesch-Reading-Ease nach Amstad, Untergrenze (Verstoß).
STUFEN = {
    1: dict(name="einfach", satz_avg=(6, 11), satz_max=15, satz_lang=12, lang_anteil=0.15,
            passiv=1.0, nominal=2.0, streck=0.0, flesch_min=70, fuell=1.0, strich=0.0),
    2: dict(name="klar", satz_avg=(9, 14), satz_max=22, satz_lang=18, lang_anteil=0.20,
            passiv=3.0, nominal=3.0, streck=0.5, flesch_min=60, fuell=1.5, strich=0.5),
    3: dict(name="sachlich", satz_avg=(12, 17), satz_max=30, satz_lang=24, lang_anteil=0.20,
            passiv=5.0, nominal=4.0, streck=1.0, flesch_min=50, fuell=2.0, strich=1.0),
    4: dict(name="ausführlich", satz_avg=(15, 21), satz_max=38, satz_lang=30, lang_anteil=0.25,
            passiv=6.0, nominal=5.0, streck=1.0, flesch_min=40, fuell=2.0, strich=1.5),
    5: dict(name="elaboriert", satz_avg=(18, 26), satz_max=50, satz_lang=38, lang_anteil=0.30,
            passiv=8.0, nominal=6.0, streck=1.5, flesch_min=30, fuell=2.5, strich=2.0),
}

# ---------------------------------------------------------------------------
# Textzerlegung
# ---------------------------------------------------------------------------
ABKUERZUNGEN = [
    "z. B.", "z.B.", "u. a.", "u.a.", "d. h.", "d.h.", "u. U.", "u.U.", "s. o.", "s. u.",
    "bzw.", "ca.", "etc.", "usw.", "vgl.", "evtl.", "ggf.", "inkl.", "exkl.", "max.", "min.",
    "Nr.", "Dr.", "Prof.", "Hr.", "Fr.", "St.", "Str.", "Mio.", "Mrd.", "Tsd.", "Jh.",
    "Abs.", "Art.", "Bd.", "Hrsg.", "Jg.", "Kap.", "Mo.", "Di.", "Mi.", "Do.", "Sa.", "So.",
    "Jan.", "Feb.", "Mrz.", "Apr.", "Aug.", "Sept.", "Okt.", "Nov.", "Dez.", "o. Ä.", "o.Ä.",
    "i. d. R.", "i.d.R.", "sog.", "bspw.", "geb.", "gest.", "ehem.", "engl.", "dt.", "lat.",
]

WORT_RE = re.compile(r"[A-Za-zÄÖÜäöüßéèáàóòúùâêîôû]+(?:[-'][A-Za-zÄÖÜäöüß]+)*")
ZAHL_RE = re.compile(r"\d+(?:[.,]\d+)*(?:\s?%)?")
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]")
STRICH_RE = re.compile(r"(?:\s[–—]\s|—|\s-\s)")
UEBERSCHRIFT_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.*)$")
LISTE_RE = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s+")
FETT_RE = re.compile(r"\*\*[^*\n]+\*\*|__[^_\n]+__")


def markdown_entfernen(text: str) -> str:
    """Entfernt Markdown-Auszeichnung, behält den Wortlaut."""
    t = text
    t = re.sub(r"```.*?```", " ", t, flags=re.S)
    t = re.sub(r"`([^`]*)`", r"\1", t)
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"^\s{0,3}#{1,6}\s+.*$", "", t, flags=re.M)
    t = re.sub(r"^\s*(?:[-*•]|\d+[.)])\s+", "", t, flags=re.M)
    t = re.sub(r"^\s*>\s?", "", t, flags=re.M)
    t = re.sub(r"\*\*|__|(?<!\w)[*_](?!\s)|(?<!\s)[*_](?!\w)", "", t)
    t = re.sub(r"^\s*[-*_]{3,}\s*$", "", t, flags=re.M)
    return t


def saetze_teilen(text: str) -> list[str]:
    """Zerlegt in Sätze. Abkürzungen und Zahlen mit Punkt werden geschützt."""
    t = text
    for abk in ABKUERZUNGEN:
        t = t.replace(abk, abk.replace(".", "․").replace(" ", " "))
    t = re.sub(r"(\d)\.(\d)", r"\1․\2", t)
    t = re.sub(r"(\d)\.(\s)", r"\1․\2", t)  # "am 3. März", "1. Halbjahr"
    t = re.sub(r"\b([A-ZÄÖÜ])\.\s", r"\1․ ", t)  # Initialen
    absaetze = [a for a in re.split(r"\n\s*\n", t) if a.strip()]
    saetze: list[str] = []
    for absatz in absaetze:
        absatz = " ".join(absatz.split())
        teile = re.split(r"(?<=[.!?…])[\"“”»«’']?\s+(?=[\"„»«»‚(A-ZÄÖÜ0-9])", absatz)
        for s in teile:
            s = s.replace("․", ".").replace(" ", " ").strip()
            if WORT_RE.search(s):
                saetze.append(s)
    return saetze


def woerter(text: str) -> list[str]:
    return WORT_RE.findall(text)


VOKAL_RE = re.compile(r"[aeiouyäöüáéíóúàèâêîôû]+", re.I)


def silben(wort: str) -> int:
    """Silbenzählung für deutsche Wörter: Vokalgruppen, Diphthonge als eine Silbe."""
    w = wort.lower()
    gruppen = VOKAL_RE.findall(w)
    n = len(gruppen)
    # Häufige Fälle, in denen zwei Vokale zwei Silben sind
    for g in gruppen:
        if len(g) >= 2 and g not in ("ie", "ei", "ai", "au", "eu", "äu", "ee", "oo", "aa", "ue", "oe", "ae", "ey", "ay", "ui", "ou"):
            n += len(g) - 1
    return max(1, n)


# ---------------------------------------------------------------------------
# Muster
# ---------------------------------------------------------------------------
WERDEN_RE = re.compile(r"\b(?:wird|werden|wurde|wurden|worden|würde|würden|werde|wirst|werdet|wurdest|wurdet)\b", re.I)
PARTIZIP_RE = re.compile(r"\b(?:\w*ge\w{2,}(?:t|en)|\w{3,}iert)\b", re.I)
PARTIZIP_AUSNAHMEN = {"gegen", "gegenüber", "gegenteil", "gegend", "gegenden", "gegenwart", "gegenstand", "gegenstände", "gelegenheit", "gelegenheiten", "gemeinden", "gemeinsamen", "gesamten", "gestalten", "geraten", "gebieten", "geräten", "gedanken", "gegebenheiten"}

HABEN_SEIN = {"hat", "haben", "habe", "hatte", "hatten", "hast", "habt", "hätte", "hätten",
              "ist", "sind", "war", "waren", "bin", "bist", "seid", "wäre", "wären", "sei", "gewesen"}


def passiv_kandidaten(satz: str) -> list[str]:
    """Partizipien, die zu einer werden-Form gehören könnten. Perfekt mit haben/sein wird ausgeschlossen."""
    tokens = re.findall(r"[\wäöüÄÖÜß]+", satz)
    low = [t.lower() for t in tokens]
    treffer = []
    for i, t in enumerate(tokens):
        if not PARTIZIP_RE.fullmatch(t) or low[i] in PARTIZIP_AUSNAHMEN:
            continue
        nachbarn = {low[i - 1] if i > 0 else "", low[i + 1] if i + 1 < len(low) else ""}
        if nachbarn & HABEN_SEIN:
            continue
        # steht vor dem Partizip eine werden-Form ohne dazwischenliegende haben/sein-Form?
        vorher = low[:i]
        if any(WERDEN_RE.fullmatch(v) for v in vorher) or any(WERDEN_RE.fullmatch(v) for v in low[i + 1:i + 3]):
            treffer.append(t)
    return treffer


NOMINAL_RE = re.compile(r"\b[A-ZÄÖÜ]\w*(?:ung|ungen|heit|heiten|keit|keiten|ität|itäten|ierung|ierungen|isierung|isierungen)\b")
NOMINAL_AUSNAHMEN = {"zeitung", "zeitungen", "wohnung", "wohnungen", "rechnung", "rechnungen", "regierung", "regierungen",
                     "bedingung", "bedingungen", "sitzung", "sitzungen", "meinung", "meinungen", "ordnung", "zeitungen",
                     "kleidung", "nahrung", "richtung", "richtungen", "abteilung", "abteilungen", "verwaltung", "universität",
                     "universitäten", "stadt", "wahrheit", "freiheit", "gesundheit", "krankheit", "krankheiten", "sicherheit",
                     "mehrheit", "minderheit", "kindheit", "einheit", "einheiten", "möglichkeit", "möglichkeiten",
                     "schwierigkeit", "schwierigkeiten", "öffentlichkeit", "persönlichkeit", "qualität", "identität",
                     "zeitungen", "stellung", "leitung", "leitungen", "lösung", "lösungen", "erfahrung", "erfahrungen",
                     "forschung", "bildung", "ausbildung", "beziehung", "beziehungen", "bevölkerung", "bewegung", "übung", "übungen"}

STRECKVERBEN = [
    r"zur verfügung (?:stellen|stellt|stellte|gestellt|stehen|steht|stand)",
    r"in betracht (?:ziehen|zieht|zog|gezogen|kommen|kommt|kam)",
    r"zum ausdruck (?:bringen|bringt|brachte|gebracht|kommen|kommt|kam)",
    r"berücksichtigung (?:finden|findet|fand|gefunden)",
    r"anwendung (?:finden|findet|fand|gefunden)",
    r"verwendung (?:finden|findet|fand|gefunden)",
    r"beachtung (?:finden|findet|fand|gefunden|schenken|schenkt)",
    r"zur anwendung (?:kommen|kommt|kam|gekommen|bringen|bringt|gebracht)",
    r"zum einsatz (?:kommen|kommt|kam|gekommen|bringen|bringt|gebracht)",
    r"in erwägung (?:ziehen|zieht|zog|gezogen)",
    r"rechnung (?:tragen|trägt|trug|getragen)",
    r"unter beweis (?:stellen|stellt|stellte|gestellt)",
    r"in kenntnis (?:setzen|setzt|setzte|gesetzt)",
    r"zur kenntnis (?:nehmen|nimmt|nahm|genommen)",
    r"in angriff (?:nehmen|nimmt|nahm|genommen)",
    r"zum abschluss (?:bringen|bringt|brachte|gebracht|kommen|kommt|kam)",
    r"in frage (?:stellen|stellt|stellte|gestellt|kommen|kommt|kam)",
    r"zur sprache (?:bringen|bringt|brachte|gebracht|kommen|kommt|kam)",
    r"eine entscheidung (?:treffen|trifft|traf|getroffen)",
    r"eine (?:prüfung|überprüfung|analyse|bewertung|untersuchung|auswertung) (?:vornehmen|vorgenommen|durchführen|durchgeführt|durchzuführen|vorzunehmen)",
    r"(?:die|eine) (?:umsetzung|durchführung|einführung|erstellung|bereitstellung|erarbeitung|entwicklung|prüfung) (?:erfolgt|erfolgte|erfolgen|vornehmen|vorgenommen|durchführen|durchgeführt)",
    r"\berfolgt(?:e|en)?\b",
    r"\bin die wege (?:leiten|leitet|leitete|geleitet)",
    r"\bzur durchführung (?:bringen|gelangen|kommen)",
    r"\bzustimmung (?:erteilen|erteilt|erteilte)",
    r"\bhilfestellung (?:leisten|leistet|geben|gibt)",
    r"\bsorge (?:tragen|trägt|trug)",
    r"\bin erfahrung (?:bringen|bringt|brachte|gebracht)",
    r"\bgebrauch (?:machen|macht|machte|gemacht)",
]
STRECK_RE = re.compile("|".join(f"(?:{p})" for p in STRECKVERBEN), re.I)

BINAER_RE = re.compile(r"\bnicht\s+(?:nur\s+)?[^.;:!?]{2,80}?,\s*sondern\b", re.I)
NICHTNUR_RE = re.compile(r"\bnicht nur\b[^.!?]{0,120}?\bsondern auch\b", re.I)
FRAGE_ANFANG_RE = re.compile(r"^[^.!?]{3,160}\?\s*$")
DREIER_RE = re.compile(r"\b(\w+),\s+(\w+)\s+(?:und|oder)\s+(\w+)\b")
FAZIT_RE = re.compile(r"^\s*(?:\*\*)?(?:fazit|zusammenfassend|zusammenfassung|abschließend|insgesamt lässt sich|alles in allem|unterm strich|zusammengefasst)\b", re.I)
KOLON_TITEL_RE = re.compile(r"^[^:\n]{3,60}:\s+(?:warum|wie|was|wenn|der|die|das|ein|eine)\b", re.I)


# ---------------------------------------------------------------------------
# Floskelliste
# ---------------------------------------------------------------------------
def floskeln_laden(pfad: str | None = None) -> dict[str, list[str]]:
    """Liest references/floskeln.txt. Abschnitte: [Name], eine Phrase pro Zeile, # Kommentar."""
    pfad = pfad or os.path.join(REFERENZEN, "floskeln.txt")
    kategorien: dict[str, list[str]] = {}
    aktuell = "Floskeln"
    if not os.path.exists(pfad):
        return kategorien
    with open(pfad, encoding="utf-8") as f:
        for zeile in f:
            z = zeile.strip()
            if not z or z.startswith("#"):
                continue
            m = re.match(r"^\[(.+)\]$", z)
            if m:
                aktuell = m.group(1).strip()
                kategorien.setdefault(aktuell, [])
                continue
            kategorien.setdefault(aktuell, []).append(z)
    return kategorien


def phrase_zu_regex(phrase: str) -> re.Pattern:
    """'…' in der Phrase steht für beliebige 1–5 Wörter. Wortgrenzen außen."""
    teile = [re.escape(t.strip()) for t in phrase.split("…")]
    muster = r"(?:\s+\S+){1,5}\s+".join(teile)
    muster = muster.replace(r"\ ", r"\s+")
    return re.compile(r"(?<![\wäöüß])" + muster + r"(?![\wäöüß])", re.I)


# ---------------------------------------------------------------------------
# Messung
# ---------------------------------------------------------------------------
@dataclass
class Befund:
    art: str          # "verstoss" | "hinweis"
    text: str
    satz: int | None = None
    beleg: str | None = None


@dataclass
class Messung:
    stufe: int
    woerter: int = 0
    saetze: int = 0
    absaetze: int = 0
    satz_avg: float = 0.0
    satz_median: float = 0.0
    satz_max: int = 0
    satz_max_text: str = ""
    satz_lang_anteil: float = 0.0
    silben_pro_wort: float = 0.0
    flesch: float = 0.0
    wsf: float = 0.0
    lix: float = 0.0
    passiv: int = 0
    nominal: int = 0
    streck: int = 0
    floskeln: dict = field(default_factory=dict)
    fuellwoerter: int = 0
    striche: int = 0
    befunde: list = field(default_factory=list)

    def pro100(self, n: int) -> float:
        return round(100.0 * n / self.woerter, 1) if self.woerter else 0.0


def kuerzen(s: str, n: int = 90) -> str:
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def messen(rohtext: str, stufe: int, ziele: dict, floskeln: dict[str, list[str]]) -> Messung:
    m = Messung(stufe=stufe)
    text = markdown_entfernen(rohtext)
    saetze = saetze_teilen(text)
    absaetze = [a for a in re.split(r"\n\s*\n", rohtext) if WORT_RE.search(a)]
    m.saetze = len(saetze)
    m.absaetze = len(absaetze)
    alle = woerter(text)
    m.woerter = len(alle)
    if not alle or not saetze:
        m.befunde.append(Befund("hinweis", "Kein auswertbarer Text."))
        return m

    laengen = [len(woerter(s)) for s in saetze]
    m.satz_avg = round(sum(laengen) / len(laengen), 1)
    m.satz_median = statistics.median(laengen)
    m.satz_max = max(laengen)
    m.satz_max_text = saetze[laengen.index(m.satz_max)]
    lange = [i for i, l in enumerate(laengen) if l > ziele["satz_lang"]]
    m.satz_lang_anteil = round(len(lange) / len(laengen), 2)

    sil = [silben(w) for w in alle]
    m.silben_pro_wort = round(sum(sil) / len(sil), 2)
    asl = sum(laengen) / len(laengen)
    asw = sum(sil) / len(sil)
    m.flesch = round(180 - asl - 58.5 * asw, 1)
    ms = 100.0 * sum(1 for s in sil if s >= 3) / len(sil)
    iw = 100.0 * sum(1 for w in alle if len(w) > 6) / len(alle)
    es = 100.0 * sum(1 for s in sil if s == 1) / len(sil)
    m.wsf = round(0.1935 * ms + 0.1672 * asl + 0.1297 * iw - 0.0327 * es - 0.875, 1)
    m.lix = round(asl + iw, 1)

    # --- Sätze: Länge, Passiv, Streckverben, Binärkontraste ---
    for i, s in enumerate(saetze, 1):
        l = laengen[i - 1]
        if l > ziele["satz_max"]:
            m.befunde.append(Befund("verstoss", f"Satz {i} hat {l} Wörter (Stufe {stufe}: höchstens {ziele['satz_max']})", i, kuerzen(s)))
        if WERDEN_RE.search(s):
            kandidaten = passiv_kandidaten(s)
            if kandidaten:
                m.passiv += 1
                m.befunde.append(Befund("hinweis", f"Passiv-Verdacht ({', '.join(kandidaten[:2])})", i, kuerzen(s)))
        for tr in STRECK_RE.finditer(s):
            m.streck += 1
            m.befunde.append(Befund("verstoss" if ziele["streck"] == 0 else "hinweis", f"Streckverb „{tr.group(0)}“", i, kuerzen(s)))
        if NICHTNUR_RE.search(s):
            m.befunde.append(Befund("hinweis", "„nicht nur … sondern auch“ – meist reicht „und“", i, kuerzen(s)))
        elif BINAER_RE.search(s):
            m.befunde.append(Befund("hinweis", "Binärkontrast „nicht X, sondern Y“ – Y direkt sagen", i, kuerzen(s)))
        if stufe <= 2 and s.count(",") >= 3:
            m.befunde.append(Befund("hinweis", f"{s.count(',')} Kommas – Schachtelsatz-Verdacht", i, kuerzen(s)))

    # --- Nominalstil ---
    nominale = [w for w in NOMINAL_RE.findall(text) if w.lower() not in NOMINAL_AUSNAHMEN]
    m.nominal = len(nominale)

    # --- Floskeln und Füllwörter ---
    for kat, phrasen in floskeln.items():
        for ph in phrasen:
            rx = phrase_zu_regex(ph)
            treffer = [(i, s) for i, s in enumerate(saetze, 1) if rx.search(s)]
            if not treffer:
                continue
            m.floskeln.setdefault(kat, {})[ph] = len(treffer)
            if kat.lower().startswith("füll"):
                m.fuellwoerter += len(treffer)
            art = "hinweis" if kat.lower().startswith("füll") or kat.lower().startswith("kontext") else "verstoss"
            for i, s in treffer[:3]:
                m.befunde.append(Befund(art, f"{kat}: „{ph}“", i, kuerzen(s)))

    # --- Struktur ---
    m.striche = len(STRICH_RE.findall(text))
    if m.pro100(m.striche) > ziele["strich"]:
        m.befunde.append(Befund("verstoss", f"{m.striche} Gedankenstriche ({m.pro100(m.striche)} je 100 Wörter, Stufe {stufe}: höchstens {ziele['strich']}) – Sätze umbauen statt einschieben"))
    emojis = EMOJI_RE.findall(rohtext)
    if emojis:
        m.befunde.append(Befund("verstoss", f"{len(emojis)} Emoji im Text"))
    fett = FETT_RE.findall(rohtext)
    if len(fett) > max(2, m.absaetze * 2):
        m.befunde.append(Befund("verstoss", f"{len(fett)} Fettungen bei {m.absaetze} Absätzen – höchstens zwei je Absatz"))
    listen = [z for z in rohtext.splitlines() if LISTE_RE.match(z)]
    if listen and m.woerter and len(listen) * 100 / max(1, m.saetze) > 40:
        m.befunde.append(Befund("hinweis", f"{len(listen)} Listenpunkte bei {m.saetze} Sätzen – Fließtext-Gedanken als Pseudoliste?"))
    ueberschriften = [UEBERSCHRIFT_RE.match(z).group(1) for z in rohtext.splitlines() if UEBERSCHRIFT_RE.match(z)]
    for u in ueberschriften:
        if u.strip().endswith("?"):
            m.befunde.append(Befund("hinweis", f"Überschrift als Frage: „{kuerzen(u, 60)}“ – Aussage statt Frage"))
        elif KOLON_TITEL_RE.match(u):
            m.befunde.append(Befund("hinweis", f"Doppelpunkt-Titel: „{kuerzen(u, 60)}“"))
    if len(ueberschriften) > 0 and m.woerter / len(ueberschriften) < 80:
        m.befunde.append(Befund("hinweis", f"{len(ueberschriften)} Überschriften auf {m.woerter} Wörter – Überschriften-Inflation"))

    # Absätze: Fragen als Einstieg, Fazit-Floskel, Symmetrie
    for a in absaetze:
        erster = saetze_teilen(markdown_entfernen(a))
        if erster and FRAGE_ANFANG_RE.match(erster[0]) and not erster[0].lower().startswith(("wer ", "wen ", "wem ", "wessen ")):
            m.befunde.append(Befund("hinweis", "Absatz beginnt mit rhetorischer Frage", None, kuerzen(erster[0])))
        if FAZIT_RE.match(a):
            m.befunde.append(Befund("verstoss", "Fazit-Ankündigung – die Schlussfolgerung ohne Etikett schreiben", None, kuerzen(a)))
    if len(absaetze) >= 4:
        al = [len(woerter(a)) for a in absaetze]
        if statistics.pstdev(al) / (sum(al) / len(al)) < 0.15:
            m.befunde.append(Befund("hinweis", "Alle Absätze fast gleich lang – Länge sollte dem Inhalt folgen, nicht einem Raster"))

    # Rhythmus: drei gleich lange Sätze, gleiche Satzanfänge, Dreierfiguren
    for i in range(len(laengen) - 2):
        a, b, c = laengen[i: i + 3]
        if max(a, b, c) - min(a, b, c) <= 1 and a >= 6:
            m.befunde.append(Befund("hinweis", f"Sätze {i+1}–{i+3} sind gleich lang ({a}/{b}/{c} Wörter) – Rhythmus variieren"))
            break
    anfaenge = [woerter(s)[0].lower() for s in saetze if woerter(s)]
    for i in range(len(anfaenge) - 2):
        if anfaenge[i] == anfaenge[i + 1] == anfaenge[i + 2] and anfaenge[i] not in ("der", "die", "das", "es", "wir", "sie", "ich"):
            m.befunde.append(Befund("hinweis", f"Sätze {i+1}–{i+3} beginnen alle mit „{anfaenge[i]}“ – Anapher oder Zufall?"))
            break
    dreier = DREIER_RE.findall(text)
    if len(dreier) >= 3 and m.pro100(len(dreier)) > 1.0:
        m.befunde.append(Befund("hinweis", f"{len(dreier)} Dreier-Aufzählungen – trägt jedes dritte Glied eigene Information?"))

    # --- Schwellen ---
    lo, hi = ziele["satz_avg"]
    if m.satz_avg > hi:
        m.befunde.append(Befund("verstoss", f"Mittlere Satzlänge {m.satz_avg} Wörter (Stufe {stufe}: höchstens {hi})"))
    elif m.satz_avg < lo and m.saetze >= 5:
        m.befunde.append(Befund("hinweis", f"Mittlere Satzlänge {m.satz_avg} Wörter liegt unter dem Korridor der Stufe {stufe} ({lo}–{hi}) – Stakkato-Verdacht"))
    if m.satz_lang_anteil > ziele["lang_anteil"] and m.saetze >= 5:
        m.befunde.append(Befund("verstoss", f"{int(m.satz_lang_anteil*100)} % der Sätze länger als {ziele['satz_lang']} Wörter (höchstens {int(ziele['lang_anteil']*100)} %)"))
    if m.pro100(m.passiv) > ziele["passiv"] and m.saetze >= 5:
        m.befunde.append(Befund("verstoss", f"Passiv in {m.passiv} Sätzen ({m.pro100(m.passiv)} je 100 Wörter, Stufe {stufe}: höchstens {ziele['passiv']})"))
    if m.pro100(m.nominal) > ziele["nominal"]:
        m.befunde.append(Befund("verstoss", f"{m.nominal} Nominalisierungen ({m.pro100(m.nominal)} je 100 Wörter, Stufe {stufe}: höchstens {ziele['nominal']}): {', '.join(sorted(set(nominale))[:8])}"))
    if m.pro100(m.streck) > ziele["streck"]:
        m.befunde.append(Befund("verstoss", f"{m.streck} Streckverben ({m.pro100(m.streck)} je 100 Wörter, Stufe {stufe}: höchstens {ziele['streck']})"))
    if m.pro100(m.fuellwoerter) > ziele["fuell"]:
        m.befunde.append(Befund("verstoss", f"{m.fuellwoerter} Füllwörter ({m.pro100(m.fuellwoerter)} je 100 Wörter, Stufe {stufe}: höchstens {ziele['fuell']})"))
    if m.flesch < ziele["flesch_min"] and m.woerter >= 60:
        m.befunde.append(Befund("verstoss", f"Flesch-Amstad {m.flesch} (Stufe {stufe}: mindestens {ziele['flesch_min']}) – kürzere Sätze oder kürzere Wörter"))

    return m


# ---------------------------------------------------------------------------
# Substanzabgleich
# ---------------------------------------------------------------------------
ZITAT_RE = re.compile(r"[„»\"“]([^“”«\"\n]{6,200})[“”«\"]")
URL_RE = re.compile(r"https?://\S+|www\.\S+|\b[\w.+-]+@[\w-]+\.[\w.]+\b")
AKRONYM_RE = re.compile(r"\b(?:[A-ZÄÖÜ]{2,}[a-zäöü]*[A-ZÄÖÜ]*|[A-Za-z]+[A-ZÄÖÜ][a-zäöü]+)\b")


def substanz(original: str, neu: str) -> list[Befund]:
    befunde: list[Befund] = []
    o = markdown_entfernen(original)
    n = markdown_entfernen(neu)
    n_low = n.lower()
    n_kompakt = re.sub(r"[\s.,]", "", n_low)

    wo, wn = len(woerter(o)), len(woerter(n))
    if wo:
        q = wn / wo
        if q < 0.6:
            befunde.append(Befund("verstoss", f"Text auf {int(q*100)} % gekürzt – Begründungen, Beispiele und Einschränkungen prüfen. Kürze ist kein Verdienst."))
        elif q > 1.5:
            befunde.append(Befund("hinweis", f"Text auf {int(q*100)} % verlängert – ist alles Neue Substanz aus dem Original?"))

    fehlende_zahlen = []
    for z in sorted(set(ZAHL_RE.findall(o))):
        k = re.sub(r"[\s.,]", "", z)
        if k and k not in n_kompakt:
            fehlende_zahlen.append(z)
    if fehlende_zahlen:
        befunde.append(Befund("verstoss", f"Zahlen aus dem Original fehlen: {', '.join(fehlende_zahlen[:15])}"))

    fehlende_zitate = [z for z in ZITAT_RE.findall(o) if z.strip().lower() not in n_low]
    for z in fehlende_zitate[:5]:
        befunde.append(Befund("verstoss", "Zitat verändert oder entfernt", None, kuerzen(z)))

    fehlende_urls = [u for u in set(URL_RE.findall(o)) if u.lower() not in n_low]
    if fehlende_urls:
        befunde.append(Befund("verstoss", f"Adressen fehlen: {', '.join(fehlende_urls[:5])}"))

    fehlende_akr = sorted({a for a in AKRONYM_RE.findall(o) if a.lower() not in n_low})
    if fehlende_akr:
        befunde.append(Befund("hinweis", f"Eigennamen/Kürzel aus dem Original nicht mehr im Text: {', '.join(fehlende_akr[:15])}"))

    # Namen-Kandidaten: zwei großgeschriebene Wörter hintereinander mitten im Satz
    # („Müller GmbH“, „Anbieter A“, „Wolf Schneider“). Einzelne Substantive wären zu unscharf.
    namen = set()
    for s_ in saetze_teilen(o):
        ws = woerter(s_)
        for a, b in zip(ws[1:], ws[2:]):
            if a[0].isupper() and b[0].isupper() and not (a.lower() in ("der", "die", "das") or b.lower() in ("der", "die", "das")):
                namen.add(f"{a} {b}")
    fehlende_namen = sorted(n_ for n_ in namen if n_.lower() not in n_low and not all(t.lower() in n_low for t in n_.split()))
    if fehlende_namen:
        befunde.append(Befund("hinweis", f"Namen aus dem Original ohne Entsprechung: {', '.join(fehlende_namen[:15])}"))

    if "[PRÜFEN" in neu or "[prüfen" in neu.lower():
        befunde.append(Befund("hinweis", f"{neu.count('[PRÜFEN')} offene PRÜFEN-Marker im Text"))
    return befunde


# ---------------------------------------------------------------------------
# Stilprofile: Schwellen aus references/stile/NAME.md (Frontmatter)
# ---------------------------------------------------------------------------
def stil_laden(name: str) -> dict:
    pfad = os.path.join(REFERENZEN, "stile", f"{name.lower()}.md")
    if not os.path.exists(pfad):
        sys.exit(f"Stilprofil nicht gefunden: {pfad}")
    with open(pfad, encoding="utf-8") as f:
        inhalt = f.read()
    m = re.match(r"^---\n(.*?)\n---", inhalt, re.S)
    werte: dict = {}
    if not m:
        return werte
    for zeile in m.group(1).splitlines():
        if ":" not in zeile:
            continue
        k, v = zeile.split(":", 1)
        k, v = k.strip(), v.strip()
        if k in ("satz_max", "satz_lang"):
            werte[k] = int(v)
        elif k in ("passiv", "nominal", "streck", "flesch_min", "fuell", "strich", "lang_anteil"):
            werte[k] = float(v)
        elif k == "satz_avg":
            lo, hi = re.findall(r"\d+", v)[:2]
            werte[k] = (int(lo), int(hi))
        elif k == "stufen":
            werte[k] = v
    return werte


# ---------------------------------------------------------------------------
# Ausgabe
# ---------------------------------------------------------------------------
def bericht(m: Messung, ziele: dict, extra: list[Befund], stil: str | None) -> str:
    lo, hi = ziele["satz_avg"]
    z = []
    kopf = f"TACHELES · Messung · Stufe {m.stufe} ({ziele['name']})" + (f" · Stil {stil}" if stil else "")
    z.append(kopf)
    z.append("=" * len(kopf))
    z.append(f"Wörter {m.woerter} · Sätze {m.saetze} · Absätze {m.absaetze}")
    z.append(f"Satzlänge  Ø {m.satz_avg} · Median {m.satz_median:g} · längster {m.satz_max}   (Ziel Ø {lo}–{hi}, kein Satz über {ziele['satz_max']})")
    z.append(f"Lesbarkeit Flesch-Amstad {m.flesch} (Ziel ≥ {ziele['flesch_min']}) · Wiener Sachtextformel {m.wsf} · LIX {m.lix} · Silben/Wort {m.silben_pro_wort}")
    z.append(f"Passiv {m.passiv} ({m.pro100(m.passiv)}/100, max {ziele['passiv']}) · Nominalisierungen {m.nominal} ({m.pro100(m.nominal)}/100, max {ziele['nominal']}) · Streckverben {m.streck}")
    n_fl = sum(v for kat, d in m.floskeln.items() for v in d.values())
    z.append(f"Floskeln/Füllwörter {n_fl} · Gedankenstriche {m.striche}")
    alle = m.befunde + extra
    verst = [b for b in alle if b.art == "verstoss"]
    hinw = [b for b in alle if b.art == "hinweis"]

    def zeile(b: Befund) -> str:
        wo = f" [Satz {b.satz}]" if b.satz else ""
        s = f"  {'✗' if b.art == 'verstoss' else '·'} {b.text}{wo}"
        if b.beleg:
            s += f"\n      „{b.beleg}“"
        return s

    z.append("")
    z.append(f"VERSTÖSSE ({len(verst)})")
    z.extend(zeile(b) for b in verst) if verst else z.append("  keine")
    z.append("")
    z.append(f"HINWEISE ({len(hinw)})")
    z.extend(zeile(b) for b in hinw[:40]) if hinw else z.append("  keine")
    if len(hinw) > 40:
        z.append(f"  … und {len(hinw) - 40} weitere")
    z.append("")
    if verst:
        z.append(f"Befund: {len(verst)} Verstöße, {len(hinw)} Hinweise. Nachbessern, dann erneut messen.")
    else:
        z.append(f"Befund: keine Verstöße, {len(hinw)} Hinweise. Hinweise sind Redakteurssache, keine Pflicht.")
    return "\n".join(z)


def main(argv: list[str] | None = None) -> int:
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    p = argparse.ArgumentParser(description="Misst einen deutschen Text gegen die Zielwerte einer tacheles-Stufe.")
    p.add_argument("datei", nargs="?", default="-", help="Textdatei oder - für stdin")
    p.add_argument("--stufe", type=int, default=3, choices=[1, 2, 3, 4, 5])
    p.add_argument("--stil", default=None, help="Stilprofil aus references/stile/")
    p.add_argument("--vergleich", default=None, metavar="ORIGINAL", help="Original zum Substanzabgleich")
    p.add_argument("--json", action="store_true")
    p.add_argument("--liste", action="store_true", help="Floskelliste anzeigen")
    a = p.parse_args(argv)

    floskeln = floskeln_laden()
    if a.liste:
        for kat, ph in floskeln.items():
            print(f"[{kat}] {len(ph)}")
            for x in ph:
                print("  " + x)
        return 0

    try:
        text = sys.stdin.read() if a.datei == "-" else open(a.datei, encoding="utf-8").read()
    except OSError as e:
        print(f"Datei nicht lesbar: {e}", file=sys.stderr)
        return 2
    if not text.strip():
        print("Leerer Text.", file=sys.stderr)
        return 2

    ziele = dict(STUFEN[a.stufe])
    if a.stil:
        ziele.update({k: v for k, v in stil_laden(a.stil).items() if k != "stufen"})

    m = messen(text, a.stufe, ziele, floskeln)
    extra: list[Befund] = []
    if a.vergleich:
        try:
            original = open(a.vergleich, encoding="utf-8").read()
        except OSError as e:
            print(f"Original nicht lesbar: {e}", file=sys.stderr)
            return 2
        extra = substanz(original, text)

    if a.json:
        d = {k: v for k, v in m.__dict__.items() if k != "befunde"}
        d["ziele"] = ziele
        d["befunde"] = [b.__dict__ for b in m.befunde + extra]
        print(json.dumps(d, ensure_ascii=False, indent=2))
    else:
        print(bericht(m, ziele, extra, a.stil))
    return 1 if any(b.art == "verstoss" for b in m.befunde + extra) else 0


if __name__ == "__main__":
    sys.exit(main())
