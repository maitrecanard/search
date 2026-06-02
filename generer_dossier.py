#!/usr/bin/env python3
"""Génère un dossier de RÉPONSE à un appel d'offres BOAMP (pré-rempli).

Usage :
    python3 generer_dossier.py <idweb> [<idweb> ...]
    python3 generer_dossier.py --open      # tous les MAPA encore ouverts

Pour chaque avis, crée `dossiers/<idweb>-<slug>/` contenant :
  00-resume.md · 01-memoire-technique.md · 02-dpgf.md · 03-acte-engagement.md

Les champs marché (acheteur, objet, dates, procédure, lien) viennent de l'API
BOAMP ; tes infos (nom, SIRET, TJM, IBAN…) de `profil.json` (sinon
`profil.example.json`). Le prix est calculé sur ton TJM. Les parties liées au
CCTP restent à compléter (`‹CCTP›`).
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import re
import shutil
import sys

import requests

API = ("https://boamp-datadila.opendatasoft.com/api/explore/v2.1/"
       "catalog/datasets/boamp/records")
UA = "prospect-search-dossier/1.0"
TPL_DIR = "guide-appels-offres/_templates"
OUT_DIR = "dossiers"

PROCEDURE_LABELS = {"PROCEDURE_ADAPTE": "Procédure adaptée (MAPA)",
                    "OUVERT": "Appel d'offres ouvert",
                    "NEGOCIE": "Procédure négociée"}

# Décomposition de charge (jours) — base d'une refonte web ; ajuste au besoin.
POSTES = [
    ("Cadrage & ateliers de lancement", 4),
    ("Spécifications & arborescence", 3),
    ("Conception UX / wireframes", 5),
    ("Maquettes UI responsive (charte)", 8),
    ("Développement CMS + thème sur-mesure", 18),
    ("Fonctionnalités spécifiques / espace dédié", 10),
    ("Reprise de contenus & migration", 6),
    ("Accessibilité RGAA (intégration, audit, déclaration)", 7),
    ("RGPD / cookies / mentions légales", 2),
    ("Recette & corrections", 5),
    ("Mise en production & redirections", 2),
    ("Formation & documentation", 4),
    ("Gestion de projet (transverse)", 6),
]

# Charge incluse dans le forfait — base ; ajuste/retire selon le CCTP.

DEPARTEMENTS = {
    "01": "Ain", "02": "Aisne", "03": "Allier", "06": "Alpes-Maritimes",
    "13": "Bouches-du-Rhône", "29": "Finistère", "31": "Haute-Garonne",
    "33": "Gironde", "34": "Hérault", "35": "Ille-et-Vilaine", "44": "Loire-Atlantique",
    "45": "Loiret", "59": "Nord", "67": "Bas-Rhin", "69": "Rhône", "75": "Paris",
    "76": "Seine-Maritime", "77": "Seine-et-Marne", "78": "Yvelines", "83": "Var",
    "84": "Vaucluse", "91": "Essonne", "92": "Hauts-de-Seine", "93": "Seine-Saint-Denis",
    "94": "Val-de-Marne", "95": "Val-d'Oise",
}


def load_profil() -> dict:
    for path in ("profil.json", "profil.example.json"):
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                p = json.load(fh)
            if path == "profil.example.json":
                print("ℹ️  profil.json absent → profil.example.json utilisé "
                      "(copie-le en profil.json et remplis tes infos).")
            return p
    raise SystemExit("Aucun profil.json / profil.example.json trouvé.")


def fetch(idweb: str) -> dict | None:
    r = requests.get(API, params={"where": f'idweb="{idweb}"', "limit": 1},
                     headers={"User-Agent": UA}, timeout=30)
    r.raise_for_status()
    res = r.json().get("results", [])
    return res[0] if res else None


def fetch_open_mapa() -> list:
    today = _dt.date.today().isoformat()
    kw = ["site internet", "site web", "application mobile", "application web",
          "plateforme numérique", "refonte du site", "développement logiciel",
          "portail web", "solution logicielle"]
    intents = " or ".join(f'objet like "{k}"' for k in kw)
    where = (f'({intents}) and nature_categorise_libelle like "Avis de marché" '
             f'and type_procedure = "PROCEDURE_ADAPTE" '
             f"and datelimitereponse > date'{today}'")
    r = requests.get(API, params={"where": where, "order_by": "datelimitereponse asc",
                                  "limit": 100}, headers={"User-Agent": UA}, timeout=30)
    r.raise_for_status()
    return r.json().get("results", [])


def _dept(rec) -> str:
    cd = rec.get("code_departement")
    code = cd[0] if isinstance(cd, list) and cd else (cd if isinstance(cd, str) else "")
    return DEPARTEMENTS.get(code, code or "—")


def _slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return s[:50] or "marche"


def _fmt(n: int) -> str:
    return f"{n:,}".replace(",", " ")


def render(template: str, ctx: dict) -> str:
    out = template
    for k, v in ctx.items():
        out = out.replace("{{" + k + "}}", str(v))
    return out


def dpgf_markdown(ctx: dict, tjm: int) -> str:
    lines = [f"# DPGF — {ctx['acheteur']}", "",
             f"**Marché** : {ctx['objet']} · idweb {ctx['idweb']} · {ctx['procedure']}",
             f"*(TJM {tjm} € HT/j — ajuste jours/TJM selon le CCTP.)*", "",
             "| # | Poste | Jours | PU € HT | Montant € HT |",
             "|---|-------|------:|--------:|-------------:|"]
    total_j = 0
    for i, (label, jours) in enumerate(POSTES, 1):
        total_j += jours
        lines.append(f"| {i} | {label} | {jours} | {tjm} | {_fmt(jours*tjm)} |")
    total = total_j * tjm
    lines += [f"| | **TOTAL** | **{total_j}** | | **{_fmt(total)}** |", "",
              f"**Total HT : {_fmt(total)} €** · Garantie {ctx['garantie_mois']} mois incluse.",
              "", "### Options (BPU)",
              "| Prestation | Unité | PU € HT |", "|---|---|--:|",
              f"| TMA / maintenance | an | {_fmt(round(total*0.1))} |",
              "| Hébergement & infogérance | an | 1 800 |",
              f"| Jour supplémentaire | jour | {tjm} |", ""]
    return "\n".join(lines)


def build(rec: dict, profil: dict, generated_at: str) -> str:
    tjm = int(profil.get("tjm", 500))
    total_ht = sum(j for _, j in POSTES) * tjm
    franchise = "293 B" in (profil.get("tva", ""))
    tva_montant = "—" if franchise else f"{_fmt(round(total_ht*0.2))} €"
    total_ttc = total_ht if franchise else round(total_ht * 1.2)

    ctx = dict(profil)
    ctx.update({
        "acheteur": rec.get("nomacheteur") or "?",
        "objet": (rec.get("objet") or "").replace("\n", " ").strip(),
        "idweb": rec.get("idweb") or "",
        "url": f"https://www.boamp.fr/pages/avis/?q=idweb:{rec.get('idweb')}",
        "dateparution": rec.get("dateparution") or "",
        "datelimite": (rec.get("datelimitereponse") or "").replace("T", " ")[:16] or "‹voir avis›",
        "departement": _dept(rec),
        "procedure": PROCEDURE_LABELS.get(rec.get("type_procedure"), rec.get("type_procedure") or "—"),
        "generated_at": generated_at,
        "total_ht": _fmt(total_ht),
        "tva_montant": tva_montant,
        "total_ttc": _fmt(total_ttc),
    })

    folder = os.path.join(OUT_DIR, f"{ctx['idweb']}-{_slug(ctx['objet'])}")
    os.makedirs(folder, exist_ok=True)
    for tpl_name, out_name in [("00-resume.tpl.md", "00-resume.md"),
                               ("01-memoire-technique.tpl.md", "01-memoire-technique.md"),
                               ("03-acte-engagement.tpl.md", "03-acte-engagement.md")]:
        with open(os.path.join(TPL_DIR, tpl_name), encoding="utf-8") as fh:
            tpl = fh.read()
        with open(os.path.join(folder, out_name), "w", encoding="utf-8") as fh:
            fh.write(render(tpl, ctx))
    with open(os.path.join(folder, "02-dpgf.md"), "w", encoding="utf-8") as fh:
        fh.write(dpgf_markdown(ctx, tjm))
    return folder


def archive_expired(open_idwebs: set) -> int:
    """Déplace dans dossiers/_archive/ les dossiers dont le marché n'est plus
    ouvert (idweb absent de la liste courante). Préserve le travail éventuel ;
    _archive est ignoré par git."""
    if not os.path.isdir(OUT_DIR):
        return 0
    archive = os.path.join(OUT_DIR, "_archive")
    moved = 0
    for name in os.listdir(OUT_DIR):
        path = os.path.join(OUT_DIR, name)
        if name == "_archive" or not os.path.isdir(path):
            continue
        parts = name.split("-")
        idweb = "-".join(parts[:2]) if len(parts) >= 2 else name
        if idweb not in open_idwebs:
            os.makedirs(archive, exist_ok=True)
            dest = os.path.join(archive, name)
            if os.path.exists(dest):
                shutil.rmtree(dest)
            shutil.move(path, dest)
            moved += 1
    return moved


def main(argv) -> int:
    if not argv:
        print(__doc__)
        return 1
    profil = load_profil()
    generated_at = _dt.date.today().isoformat()

    if argv[0] == "--open":
        recs = fetch_open_mapa()
        print(f"{len(recs)} MAPA ouverts → génération des dossiers…")
    else:
        recs = []
        for idweb in argv:
            rec = fetch(idweb)
            if rec:
                recs.append(rec)
            else:
                print(f"⚠️  idweb {idweb} introuvable")

    for rec in recs:
        folder = build(rec, profil, generated_at)
        print(f"✅ {folder}")

    # En mode --open, archive les dossiers des marchés qui ne sont plus ouverts.
    if argv[0] == "--open":
        moved = archive_expired({r.get("idweb") for r in recs})
        if moved:
            print(f"🗄️  {moved} dossier(s) expiré(s) archivé(s) dans {OUT_DIR}/_archive")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
