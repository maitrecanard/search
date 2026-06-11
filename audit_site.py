#!/usr/bin/env python3
"""Audit SEO + sécurité d'un site et génération d'un mail de prospection.

Usage :
    python3 audit_site.py --url https://exemple.fr
    python3 audit_site.py --url exemple.fr --entreprise "Exemple SARL" --out audit.md
    python3 audit_site.py --from-prospects result.json --limit 5 --out audits.md
    python3 audit_site.py --url exemple.fr --no-llm        # mail gabarit seulement

Le mail est rédigé par Claude (session Anthropic courante). Sans identifiant,
un mail bâti sur gabarit est produit à la place (l'audit, lui, marche toujours).
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import List

import requests

from prospect_search import outreach, site_audit


def load_profil() -> dict:
    for path in ("profil.json", "profil.example.json"):
        try:
            with open(path, encoding="utf-8") as fh:
                if path == "profil.example.json":
                    print("ℹ️  profil.json absent → profil.example.json utilisé.")
                return json.load(fh)
        except FileNotFoundError:
            continue
    print("⚠️  Aucun profil trouvé : signature minimale.")
    return {}


def _render(entreprise: str, url: str, snap: site_audit.SiteSnapshot,
            findings: List[site_audit.Finding], mail: dict) -> str:
    s = site_audit.summarize(findings)
    lines = [
        f"## {entreprise or url}",
        f"- **Site** : {snap.final_url or url} "
        f"(HTTP {snap.status}, {snap.elapsed_ms} ms)",
        f"- **Anomalies** : {s['total']} "
        f"({s['par_categorie']['seo']} SEO, {s['par_categorie']['securite']} sécurité — "
        f"{s['par_severite']['haute']} haute / {s['par_severite']['moyenne']} moyenne / "
        f"{s['par_severite']['basse']} basse)",
        "",
        "| Cat. | Sév. | Anomalie | Constat |",
        "|---|---|---|---|",
    ]
    for f in findings:
        lines.append(f"| {f.category} | {f.severity} | {f.title} | {f.detail} |")
    lines += [
        "",
        f"**Mail proposé** _(via {mail['via']}"
        + (f" — {mail['note']}" if mail['note'] else "") + ")_",
        "",
        f"> **Objet :** {mail['objet']}",
        "",
        "```",
        mail["corps"],
        "```",
        "",
    ]
    return "\n".join(lines)


def audit_one(url: str, entreprise: str, profil: dict, session: requests.Session,
              use_llm: bool) -> str:
    print(f"→ Audit {url} …", flush=True)
    snap = site_audit.fetch_site(url, session=session)
    if not snap.ok:
        msg = snap.error or f"HTTP {snap.status}"
        print(f"  ⨯ inaccessible ({msg})")
        return f"## {entreprise or url}\n- ⨯ Site inaccessible ({msg}).\n"
    findings = site_audit.audit(snap)
    s = site_audit.summarize(findings)
    print(f"  {s['total']} anomalies "
          f"({s['par_categorie']['seo']} SEO, {s['par_categorie']['securite']} sécu)")
    mail = outreach.generate_email(entreprise, snap.final_url or url, findings,
                                   profil, use_llm=use_llm)
    print(f"  mail via {mail['via']}"
          + (f" ({mail['note']})" if mail['note'] else ""))
    return _render(entreprise, url, snap, findings, mail)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Audit SEO/sécurité + mail de prospection.")
    p.add_argument("--url", help="URL du site à auditer.")
    p.add_argument("--entreprise", default="", help="Nom de l'entreprise (optionnel).")
    p.add_argument("--from-prospects",
                   help="Fichier result*.json : audite les prospects ayant un site.")
    p.add_argument("--limit", type=int, default=20,
                   help="Nombre max de prospects à auditer (avec --from-prospects).")
    p.add_argument("--out", help="Fichier markdown de sortie (sinon stdout).")
    p.add_argument("--no-llm", action="store_true",
                   help="Ne pas appeler Claude : mail bâti sur gabarit.")
    args = p.parse_args(argv)

    if not args.url and not args.from_prospects:
        p.error("Fournir --url ou --from-prospects.")

    profil = load_profil()
    session = requests.Session()
    use_llm = not args.no_llm
    blocks: List[str] = []

    if args.url:
        blocks.append(audit_one(args.url, args.entreprise, profil, session, use_llm))

    if args.from_prospects:
        with open(args.from_prospects, encoding="utf-8") as fh:
            prospects = json.load(fh)
        done = 0
        from prospect_search.extractor import is_blacklisted
        for pr in prospects:
            url = pr.get("source_url", "")
            if not url or is_blacklisted(url):
                continue
            blocks.append(audit_one(url, pr.get("entreprise", ""), profil,
                                    session, use_llm))
            done += 1
            if done >= args.limit:
                break
        print(f"\n{done} prospect(s) audité(s).")

    report = ("# Audits de site & mails de prospection\n\n"
              + "\n".join(blocks))
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(report)
        print(f"\n✅ Rapport écrit dans {args.out}")
    else:
        print("\n" + report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
