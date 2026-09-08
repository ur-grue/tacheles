#!/usr/bin/env python3
"""
Tests für scripts/messen.py. Nur Standardbibliothek, Aufruf:

    python3 -m unittest discover -s tests -v
    python3 tests/test_messen.py

Die Tests halten drei Versprechen des Skills nach: Das Skript findet Slop,
es meldet sauberen Text als sauber, und es merkt, wenn beim Umschreiben
Substanz verloren geht.
"""

import os
import re
import subprocess
import sys
import unittest

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(WURZEL, "skills", "tacheles")
sys.path.insert(0, os.path.join(SKILL, "scripts"))

import messen  # noqa: E402

FLOSKELN = messen.floskeln_laden(os.path.join(SKILL, "references", "floskeln.txt"))

SLOP = """In der heutigen schnelllebigen Welt spielt die Digitalisierung der Kassensysteme
eine entscheidende Rolle. Es ist wichtig zu beachten, dass die Umstellung aller 40 Filialen
der Müller GmbH bis Ende 2026 erfolgen soll, da für das bestehende System seit Januar 2020
keine Sicherheitsupdates mehr zur Verfügung gestellt werden. Die Durchführung eines
Pilotprojekts hat gezeigt, dass eine signifikante Beschleunigung des Kassiervorgangs von
55 auf 40 Sekunden realisiert werden konnte."""

SAUBER = """Die Müller GmbH tauscht bis Ende 2026 die Kassen in allen 40 Filialen aus.
Der Grund: Für das alte System gibt es seit Januar 2020 keine Sicherheitsupdates mehr.
Zwei Filialen in Bremen haben die neuen Kassen getestet. Dort dauert ein Kassiervorgang
jetzt 40 statt 55 Sekunden. Die Geschäftsführung hat 1,2 Millionen Euro freigegeben."""


def miss(text, stufe=3, ziele=None):
    return messen.messen(text, stufe, ziele or messen.STUFEN[stufe], FLOSKELN)


def verstoesse(m):
    return [b.text for b in m.befunde if b.art == "verstoss"]


class TextZerlegung(unittest.TestCase):
    def test_abkuerzung_beendet_keinen_satz(self):
        s = messen.saetze_teilen("Wir liefern bis 3. März, z. B. nach Bremen. Danach nicht mehr.")
        self.assertEqual(len(s), 2, s)

    def test_ueberschriften_zaehlen_nicht_als_satz(self):
        s = messen.saetze_teilen(messen.markdown_entfernen("# Titel\n\nEin Satz steht hier."))
        self.assertEqual(len(s), 1, s)

    def test_silben_deutsch(self):
        for wort, erwartet in [("Haus", 1), ("Kassen", 2), ("Digitalisierung", 6), ("Bau", 1)]:
            self.assertEqual(messen.silben(wort), erwartet, wort)

    def test_woerter_ohne_ziffern(self):
        self.assertEqual(messen.woerter("40 Filialen und 1,2 Millionen"), ["Filialen", "und", "Millionen"])


class SlopErkennung(unittest.TestCase):
    def test_slop_erzeugt_verstoesse(self):
        self.assertGreaterEqual(len(verstoesse(miss(SLOP))), 5)

    def test_sauberer_text_ohne_verstoesse(self):
        self.assertEqual(verstoesse(miss(SAUBER, stufe=2)), [])

    def test_einstiegsfloskel_wird_benannt(self):
        treffer = [b.text for b in miss(SLOP).befunde if "heutigen" in b.text]
        self.assertTrue(treffer, "Einstiegsfloskel nicht gemeldet")

    def test_flexion_wird_erkannt(self):
        m = miss("Das System ist effizienter und die Lösung nahtloser als bisher.")
        self.assertTrue([b for b in m.befunde if "nahtlos" in b.text])

    def test_floskel_wird_nur_einmal_gemeldet(self):
        m = miss("Die Lösung ist nahtlos.")
        self.assertEqual(len([b for b in m.befunde if "nahtlos" in b.text]), 1)

    def test_emoji_ist_verstoss(self):
        self.assertTrue([t for t in verstoesse(miss("Das Team hat geliefert. 🚀")) if "Emoji" in t])

    def test_streckverb_und_nominalstil(self):
        m = miss("Die Durchführung der Prüfung erfolgt nach Fertigstellung der Bearbeitung.")
        self.assertGreater(m.streck, 0)
        self.assertGreater(m.nominal, 0)

    def test_falscher_handlungstraeger(self):
        m = miss("Anti-Slop-Prompts machen zwei Fehler. Der Markt belohnt schnelle Anbieter.")
        treffer = [b for b in m.befunde if "Handlungsträger" in b.text]
        self.assertEqual(len(treffer), 2, [b.text for b in m.befunde])

    def test_handlungstraeger_auch_im_singular(self):
        """Wörter auf -ung, -ion und -nis müssen im Singular treffen, nicht nur im Plural."""
        for satz in ("Die Entscheidung entsteht im Ausschuss.",
                     "Die Untersuchung fordert mehr Personal.",
                     "Die Diskussion will eine Antwort.",
                     "Die Erkenntnis reift langsam."):
            m = miss(satz)
            self.assertTrue([b for b in m.befunde if "Handlungsträger" in b.text], satz)

    def test_daten_duerfen_entstehen(self):
        """„Daten entstehen“ versteckt keinen Handelnden und ist richtiges Deutsch."""
        m = miss("Daten entstehen bei jeder Messung. Die Kosten steigen weiter.")
        self.assertEqual([b for b in m.befunde if "Handlungsträger" in b.text], [])

    def test_software_darf_messen(self):
        """Ein Werkzeug, das wirklich misst und prüft, ist kein falscher Handlungsträger."""
        m = miss("Das Skript misst die Satzlänge. Das Tool erkennt Duplikate und prüft die Quellen.")
        self.assertEqual([b for b in m.befunde if "Handlungsträger" in b.text], [])

    def test_passiv_nicht_bei_perfekt(self):
        m = miss("Die Redaktion hat den Text geprüft und ihn danach veröffentlicht.")
        self.assertEqual(m.passiv, 0, [b.text for b in m.befunde])

    def test_passiv_bei_werden(self):
        m = miss("Der Text wird von der Redaktion geprüft und danach veröffentlicht.")
        self.assertGreater(m.passiv, 0)


class Stilistik(unittest.TestCase):
    gereiht = (
        "Die Plattform bietet Analysen. Die Plattform ermöglicht Exporte. "
        "Die Plattform unterstützt Sprachen. Die Firma hat das geprüft. "
        "Der Vorstand hat zugestimmt. Die Kosten sind bekannt. Zudem ist das Team bereit. "
        "Zudem läuft der Test."
    )

    def test_vorfeld_hinweis(self):
        m = miss(self.gereiht)
        self.assertTrue([b for b in m.befunde if "Subjekt" in b.text])

    def test_streuungs_hinweis(self):
        m = miss(self.gereiht)
        self.assertTrue([b for b in m.befunde if "streuen" in b.text])

    def test_konnektor_hinweis(self):
        m = miss(self.gereiht)
        self.assertTrue([b for b in m.befunde if "Konnektor" in b.text])


class Stufen(unittest.TestCase):
    def test_korridore_steigen_monoton(self):
        werte = [messen.STUFEN[i] for i in range(1, 6)]
        for a, b in zip(werte, werte[1:]):
            self.assertLess(a["satz_avg"][1], b["satz_avg"][1])
            self.assertLess(a["satz_max"], b["satz_max"])
            self.assertGreater(a["flesch_min"], b["flesch_min"])

    def test_langer_satz_nur_auf_hoher_stufe_erlaubt(self):
        satz = ("Die Geschäftsführung hat im Juni entschieden, dass die Filialen bis Ende 2026 "
                "neue Kassen bekommen, weil das alte System seit Januar 2020 keine "
                "Sicherheitsupdates mehr erhält und der Betrieb sonst gefährdet wäre.")
        self.assertTrue([t for t in verstoesse(miss(satz, stufe=1)) if "Wörter" in t])
        self.assertFalse([t for t in verstoesse(miss(satz, stufe=5)) if "Wörter" in t])


class Substanzabgleich(unittest.TestCase):
    def test_fehlende_zahl_wird_gemeldet(self):
        b = messen.substanz("Die Firma zahlt 1,2 Millionen Euro für 40 Filialen.",
                            "Die Firma zahlt Geld für ihre Filialen.")
        self.assertTrue([x for x in b if "Zahlen" in x.text])

    def test_zahlwort_zaehlt_als_zahl(self):
        b = messen.substanz("Zwei Filialen testen das System.", "Zwei Filialen testen das System.")
        self.assertFalse([x for x in b if "Zahlen" in x.text])

    def test_ueberkuerzung_ist_verstoss(self):
        b = messen.substanz(SLOP, "Die Firma kauft Kassen.")
        self.assertTrue([x for x in b if x.art == "verstoss" and "gekürzt" in x.text])

    def test_entferntes_zitat_wird_gemeldet(self):
        b = messen.substanz('Müller sagte: „Wir bleiben dabei.“ Das gilt weiter.',
                            "Müller bleibt bei seiner Haltung.")
        self.assertTrue([x for x in b if "Zitat" in x.text])

    def test_saubere_fassung_ohne_verstoss(self):
        b = messen.substanz(SLOP, SAUBER)
        self.assertEqual([x.text for x in b if x.art == "verstoss"], [])


class Stilprofile(unittest.TestCase):
    namen = ["schneider", "kaestner", "tucholsky", "kisch", "kafka", "fontane", "mann", "bernhard"]

    def test_alle_profile_laden(self):
        for name in self.namen:
            werte = messen.stil_laden(name)
            self.assertIn("satz_avg", werte, name)
            self.assertIn("satz_max", werte, name)
            lo, hi = werte["satz_avg"]
            self.assertLess(lo, hi, name)
            self.assertLessEqual(hi, werte["satz_max"], name)

    def test_profile_beginnen_mit_einleitungsprosa(self):
        """Alle acht Profile sind gleich gebaut: Titel, zwei Absätze Prosa, dann die Regeln."""
        for name in self.namen:
            pfad = os.path.join(SKILL, "references", "stile", f"{name}.md")
            with open(pfad, encoding="utf-8") as f:
                koerper = f.read().split("---", 2)[2]
            vor_regeln = koerper.split("## Regeln")[0].strip().splitlines()
            self.assertTrue(vor_regeln[0].startswith("# "), name)
            self.assertGreaterEqual(len([z for z in vor_regeln[1:] if z.strip()]), 2, name)

    def test_profile_haben_pflichtabschnitte(self):
        for name in self.namen:
            pfad = os.path.join(SKILL, "references", "stile", f"{name}.md")
            with open(pfad, encoding="utf-8") as f:
                inhalt = f.read()
            for abschnitt in ("## Regeln", "## Karikatur-Fallen", "## Probe", "## Quellen"):
                self.assertIn(abschnitt, inhalt, f"{name}: {abschnitt} fehlt")

    def test_unbekanntes_profil_bricht_ab(self):
        with self.assertRaises(SystemExit):
            messen.stil_laden("gibtsnicht")


class Floskelliste(unittest.TestCase):
    def test_liste_ist_gross_genug(self):
        self.assertGreater(sum(len(v) for v in FLOSKELN.values()), 500)

    def test_kategorien_vorhanden(self):
        for kat in ("Einstiegsfloskeln", "Schlussfloskeln", "Bedeutungsbehauptungen",
                    "Metakommentare", "Buzzwords", "Füllwörter"):
            self.assertIn(kat, FLOSKELN)

    def test_keine_doppelten_eintraege(self):
        alle = [p.lower() for v in FLOSKELN.values() for p in v]
        doppelt = {p for p in alle if alle.count(p) > 1}
        self.assertEqual(doppelt, set())

    def test_jede_phrase_ist_uebersetzbar(self):
        for kat, phrasen in FLOSKELN.items():
            for p in phrasen:
                try:
                    messen.phrase_zu_regex(p)
                except re.error as e:
                    self.fail(f"{kat}/{p}: {e}")


class Kommandozeile(unittest.TestCase):
    skript = os.path.join(SKILL, "scripts", "messen.py")

    def lauf(self, argv, eingabe=""):
        return subprocess.run([sys.executable, self.skript] + argv, input=eingabe,
                              capture_output=True, text=True)

    def test_rueckgabewert_1_bei_verstoss(self):
        p = self.lauf(["--stufe", "3", "-"], SLOP)
        self.assertEqual(p.returncode, 1)
        self.assertIn("VERSTÖSSE", p.stdout)

    def test_rueckgabewert_0_ohne_verstoss(self):
        p = self.lauf(["--stufe", "2", "-"], SAUBER)
        self.assertEqual(p.returncode, 0, p.stdout)

    def test_json_ist_gueltig(self):
        import json
        p = self.lauf(["--stufe", "3", "--json", "-"], SAUBER)
        d = json.loads(p.stdout)
        self.assertIn("flesch", d)
        self.assertIn("befunde", d)

    def test_leerer_text_meldet_bedienfehler(self):
        self.assertEqual(self.lauf(["-"], "   ").returncode, 2)

    def test_stil_wird_uebernommen(self):
        p = self.lauf(["--stufe", "3", "--stil", "bernhard", "-"], SAUBER)
        self.assertIn("Stil bernhard", p.stdout)


class Dokumentation(unittest.TestCase):
    def test_skill_nennt_alle_referenzen(self):
        with open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8") as f:
            skill = f.read()
        for datei in ("stufen.md", "redakteur.md", "stilistik.md", "textsorten.md",
                      "slop.md", "floskeln.txt", "probe.md"):
            self.assertIn(datei, skill, f"{datei} wird in SKILL.md nicht erwähnt")

    def test_alle_referenzen_existieren(self):
        for pfad in re.findall(r"references/[\w/.-]+", open(os.path.join(SKILL, "SKILL.md"),
                                                            encoding="utf-8").read()):
            voll = os.path.join(SKILL, pfad.rstrip("."))
            if voll.endswith("/"):
                continue
            self.assertTrue(os.path.exists(voll) or os.path.isdir(voll), pfad)

    def test_plugin_manifest_stimmt_mit_skill_ueberein(self):
        import json
        with open(os.path.join(WURZEL, ".claude-plugin", "plugin.json"), encoding="utf-8") as f:
            plugin = json.load(f)
        self.assertEqual(plugin["name"], "tacheles")
        with open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8") as f:
            kopf = f.read().split("---")[1]
        self.assertIn("name: tacheles", kopf)


if __name__ == "__main__":
    unittest.main(verbosity=2)
