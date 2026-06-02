#!/usr/bin/env python3
"""Point d'entrée CLI du moteur de prospection.

Usage :
    python3 main.py --target 100 --out result

Produit `result.csv` et `result.json` contenant au moins `target`
prospects collectés en direct sur DuckDuckGo.
"""

from __future__ import annotations

import argparse
import sys

from prospect_search import pipeline
from prospect_search.writer import write_csv, write_json


def _progress(found: int, target: int, name: str) -> None:
    print(f"  [{found:>3}/{target}] {name}", flush=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Recherche de prospects web.")
    parser.add_argument("--target", type=int, default=100,
                        help="Nombre minimum de prospects à collecter.")
    parser.add_argument("--out", default="result",
                        help="Préfixe des fichiers de sortie (result.csv/json).")
    parser.add_argument("--no-enrich", action="store_true",
                        help="Ne pas visiter les pages (plus rapide, moins de tel/email).")
    parser.add_argument("--max-queries", type=int, default=None,
                        help="Limite le nombre de requêtes moteur (debug).")
    parser.add_argument("--source", default="both",
                        choices=["both", "search", "overpass", "grandscomptes",
                                 "besoins"],
                        help="Sources : moteur web, Overpass/OSM, grands comptes (GE/ETI), "
                             "besoins exprimés (BOAMP), ou 'both' (web+OSM).")
    parser.add_argument("--date-min", default="2025-09-01",
                        help="Date mini de parution des appels d'offres (source besoins). "
                             "Élargir (ex. 2023-01-01) augmente le taux de contact mais "
                             "ramène des avis plus anciens.")
    args = parser.parse_args(argv)

    if args.source == "grandscomptes":
        print(f"Collecte de >= {args.target} grands comptes (GE/ETI, API entreprises)...")
        prospects = pipeline.collect_grands_comptes(
            target=args.target, progress=_progress)
    elif args.source == "besoins":
        print(f"Collecte de >= {args.target} besoins logiciels exprimés "
              f"(BOAMP, depuis {args.date_min})...")
        prospects = pipeline.collect_besoins(
            target=args.target, date_min=args.date_min, progress=_progress)
    else:
        sources = {"both": ("search", "overpass"),
                   "search": ("search",),
                   "overpass": ("overpass",)}[args.source]
        print(f"Collecte de >= {args.target} prospects "
              f"(sources: {', '.join(sources)})...")
        prospects = pipeline.collect(
            target=args.target,
            sources=sources,
            enrich=not args.no_enrich,
            progress=_progress,
            max_queries=args.max_queries,
        )

    csv_path = f"{args.out}.csv"
    json_path = f"{args.out}.json"
    write_csv(prospects, csv_path)
    write_json(prospects, json_path)

    with_phone = sum(1 for p in prospects if p.telephone)
    with_email = sum(1 for p in prospects if p.email)
    print(f"\n{len(prospects)} prospects écrits dans {csv_path} / {json_path}")
    print(f"  - avec téléphone : {with_phone}")
    print(f"  - avec email     : {with_email}")
    return 0 if len(prospects) >= args.target else 1


if __name__ == "__main__":
    sys.exit(main())
