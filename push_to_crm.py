#!/usr/bin/env python3
"""Pousse les prospects (result_*.json) et les appels d'offres ouverts au CRM.

À lancer sur le serveur du moteur de prospection. Configure d'abord :
    export CRM_URL=https://crm.exemple.fr
    export CRM_TOKEN=<token généré par `php artisan crm:api-token`>

Usage :
    python3 push_to_crm.py                # prospects + appels d'offres
    python3 push_to_crm.py --prospects    # prospects seuls
    python3 push_to_crm.py --tenders      # appels d'offres seuls
"""

from __future__ import annotations

import json
import os
import sys

from crm_sdk import CrmClient, CrmError

# Fichier source -> libellé interne (même convention que l'import local).
FILES = {
    "result_webapp.json": "webapp",
    "result_salesforce.json": "salesforce",
    "result_intranet.json": "intranet",
    "result.json": "pme",
    "result_clients_tech.json": "clients_tech",
    "result_grands_comptes.json": "grands_comptes",
    "result_besoins_logiciels.json": "besoins",
}


def push_prospects(crm: CrmClient, base_dir: str) -> None:
    for file, source in FILES.items():
        path = os.path.join(base_dir, file)
        if not os.path.isfile(path):
            print(f"  ⨯ {file} introuvable")
            continue
        rows = json.load(open(path, encoding="utf-8"))
        res = crm.push_prospects(rows, source=source)
        print(f"  ✓ {file:32} créés={res['created']:4} maj={res['updated']:4} "
              f"ignorés={res['skipped']:3} (total CRM={res['total']})")


def push_tenders(crm: CrmClient) -> None:
    # On réutilise la logique de récupération des MAPA ouverts.
    import datetime as _dt

    import refresh_mapa as rm

    recs = rm.fetch_open_mapa(_dt.date.today().isoformat())
    tenders = []
    for f in recs:
        cd = f.get("code_departement")
        code = cd[0] if isinstance(cd, list) and cd else (cd if isinstance(cd, str) else "")
        idweb = f.get("idweb")
        tenders.append({
            "idweb": idweb,
            "objet": f.get("objet") or "",
            "acheteur": f.get("nomacheteur"),
            "departement": rm.DEPARTEMENTS.get(code, code),
            "date_parution": f.get("dateparution"),
            "date_limite": f.get("datelimitereponse"),
            "url": f"https://www.boamp.fr/pages/avis/?q=idweb:{idweb}",
        })
    if not tenders:
        print("  (aucun appel d'offres ouvert)")
        return
    res = crm.push_tenders(tenders)
    print(f"  ✓ appels d'offres : créés={res['created']} maj={res['updated']} "
          f"(total CRM={res['total']})")


def main(argv) -> int:
    do_p = "--tenders" not in argv
    do_t = "--prospects" not in argv
    base_dir = os.path.dirname(os.path.abspath(__file__))

    try:
        crm = CrmClient.from_env()
        user = crm.ping()
        print(f"Connecté au CRM ({crm.base}) en tant que {user.get('email', '?')}")
    except CrmError as e:
        print(f"Erreur CRM : {e}\nVérifie CRM_URL et CRM_TOKEN.", file=sys.stderr)
        return 1

    if do_p:
        print("→ Prospects :")
        push_prospects(crm, base_dir)
    if do_t:
        print("→ Appels d'offres :")
        push_tenders(crm)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
