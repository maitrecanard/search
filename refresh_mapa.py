#!/usr/bin/env python3
"""Rafraîchit la liste des MAPA web/logiciel ENCORE OUVERTS (BOAMP).

Script autonome (stdlib + requests) : interroge l'API BOAMP v2, garde les
appels d'offres en **procédure adaptée (MAPA)** dont l'objet porte une
intention web/logiciel et dont la **date limite de réponse n'est pas dépassée**,
puis écrit `MAPA_OUVERTS.md` trié par date limite croissante.

Usage : python3 refresh_mapa.py
"""

from __future__ import annotations

import datetime as _dt

import requests

API = ("https://boamp-datadila.opendatasoft.com/api/explore/v2.1/"
       "catalog/datasets/boamp/records")
UA = "prospect-search-mapa/1.0"

OBJET_KEYWORDS = [
    "site internet", "site web", "application mobile", "application web",
    "plateforme numérique", "refonte du site", "développement logiciel",
    "portail web", "solution logicielle",
]

# Code département -> nom (localité de repli).
DEPARTEMENTS = {
    "01": "Ain", "02": "Aisne", "03": "Allier", "04": "Alpes-de-Haute-Provence",
    "05": "Hautes-Alpes", "06": "Alpes-Maritimes", "07": "Ardèche",
    "08": "Ardennes", "09": "Ariège", "10": "Aube", "11": "Aude",
    "12": "Aveyron", "13": "Bouches-du-Rhône", "14": "Calvados", "15": "Cantal",
    "16": "Charente", "17": "Charente-Maritime", "18": "Cher", "19": "Corrèze",
    "2A": "Corse-du-Sud", "2B": "Haute-Corse", "21": "Côte-d'Or",
    "22": "Côtes-d'Armor", "23": "Creuse", "24": "Dordogne", "25": "Doubs",
    "26": "Drôme", "27": "Eure", "28": "Eure-et-Loir", "29": "Finistère",
    "30": "Gard", "31": "Haute-Garonne", "32": "Gers", "33": "Gironde",
    "34": "Hérault", "35": "Ille-et-Vilaine", "36": "Indre", "37": "Indre-et-Loire",
    "38": "Isère", "39": "Jura", "40": "Landes", "41": "Loir-et-Cher",
    "42": "Loire", "43": "Haute-Loire", "44": "Loire-Atlantique", "45": "Loiret",
    "46": "Lot", "47": "Lot-et-Garonne", "48": "Lozère", "49": "Maine-et-Loire",
    "50": "Manche", "51": "Marne", "52": "Haute-Marne", "53": "Mayenne",
    "54": "Meurthe-et-Moselle", "55": "Meuse", "56": "Morbihan", "57": "Moselle",
    "58": "Nièvre", "59": "Nord", "60": "Oise", "61": "Orne", "62": "Pas-de-Calais",
    "63": "Puy-de-Dôme", "64": "Pyrénées-Atlantiques", "65": "Hautes-Pyrénées",
    "66": "Pyrénées-Orientales", "67": "Bas-Rhin", "68": "Haut-Rhin", "69": "Rhône",
    "70": "Haute-Saône", "71": "Saône-et-Loire", "72": "Sarthe", "73": "Savoie",
    "74": "Haute-Savoie", "75": "Paris", "76": "Seine-Maritime",
    "77": "Seine-et-Marne", "78": "Yvelines", "79": "Deux-Sèvres", "80": "Somme",
    "81": "Tarn", "82": "Tarn-et-Garonne", "83": "Var", "84": "Vaucluse",
    "85": "Vendée", "86": "Vienne", "87": "Haute-Vienne", "88": "Vosges",
    "89": "Yonne", "90": "Territoire de Belfort", "91": "Essonne",
    "92": "Hauts-de-Seine", "93": "Seine-Saint-Denis", "94": "Val-de-Marne",
    "95": "Val-d'Oise", "971": "Guadeloupe", "972": "Martinique",
    "973": "Guyane", "974": "La Réunion", "976": "Mayotte",
}


def _dept_name(rec) -> str:
    cd = rec.get("code_departement")
    code = cd[0] if isinstance(cd, list) and cd else (cd if isinstance(cd, str) else "")
    return DEPARTEMENTS.get(code, code or "—")


def fetch_open_mapa(today: str) -> list:
    intents = " or ".join(f'objet like "{kw}"' for kw in OBJET_KEYWORDS)
    where = (f"({intents}) and nature_categorise_libelle like \"Avis de marché\" "
             "and type_procedure = \"PROCEDURE_ADAPTE\" "
             f"and datelimitereponse > date'{today}'")
    rows, seen = [], set()
    for offset in range(0, 400, 100):
        r = requests.get(API, params={"where": where,
                                      "order_by": "datelimitereponse asc",
                                      "limit": 100, "offset": offset},
                         headers={"User-Agent": UA}, timeout=30)
        r.raise_for_status()
        batch = r.json().get("results", [])
        for rec in batch:
            idweb = rec.get("idweb")
            if idweb in seen:
                continue
            seen.add(idweb)
            rows.append(rec)
        if len(batch) < 100:
            break
    return rows


def write_markdown(rows: list, today: str, path: str = "MAPA_OUVERTS.md") -> None:
    lines = [
        "# MAPA web/logiciel encore ouverts",
        "",
        f"> Mise à jour : **{today}** — {len(rows)} appel(s) d'offres en procédure "
        "adaptée (accessibles à un freelance), date limite non dépassée, triés du "
        "plus urgent au plus lointain. Source : BOAMP (open data).",
        "",
        "| Date limite | Acheteur | Département | Objet | Avis |",
        "|---|---|---|---|---|",
    ]
    for rec in rows:
        dl = (rec.get("datelimitereponse") or "")[:16].replace("T", " ")
        ach = (rec.get("nomacheteur") or "?").replace("|", "/")[:40]
        obj = (rec.get("objet") or "").replace("|", "/").replace("\n", " ")[:60]
        url = f"https://www.boamp.fr/pages/avis/?q=idweb:{rec.get('idweb')}"
        lines.append(f"| {dl} | {ach} | {_dept_name(rec)} | {obj} | [voir]({url}) |")
    lines.append("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def main() -> int:
    today = _dt.date.today().isoformat()
    rows = fetch_open_mapa(today)
    write_markdown(rows, today)
    print(f"{len(rows)} MAPA ouverts écrits dans MAPA_OUVERTS.md ({today})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
