"""SDK Python pour envoyer prospects & appels d'offres au CRM (API Sanctum).

Le moteur de prospection tourne sur un serveur ; le CRM sur un autre. Ce client
pousse les données directement à l'API du CRM, par token Bearer.

Configuration (variables d'environnement) :
  CRM_URL    = https://crm.exemple.fr      (base, sans /api)
  CRM_TOKEN  = <token Sanctum>             (généré par `php artisan crm:api-token`)

Exemple :
    from crm_sdk import CrmClient
    crm = CrmClient.from_env()
    crm.push_prospects(rows, source="clients_tech")
"""

from __future__ import annotations

import os
from typing import Iterable, List, Optional

import requests


class CrmError(RuntimeError):
    pass


class CrmClient:
    def __init__(self, base_url: str, token: str, *, timeout: int = 30,
                 chunk_size: int = 500):
        if not base_url or not token:
            raise CrmError("CRM_URL et CRM_TOKEN sont requis.")
        self.base = base_url.rstrip("/")
        self.timeout = timeout
        self.chunk_size = chunk_size
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        })

    @classmethod
    def from_env(cls) -> "CrmClient":
        return cls(os.environ.get("CRM_URL", ""), os.environ.get("CRM_TOKEN", ""))

    # --- helpers ---
    def _post(self, path: str, payload: dict) -> dict:
        url = f"{self.base}/api/{path.lstrip('/')}"
        resp = self.session.post(url, json=payload, timeout=self.timeout)
        if resp.status_code == 401:
            raise CrmError("401 : token invalide ou manquant.")
        if not resp.ok:
            raise CrmError(f"{resp.status_code} sur {path} : {resp.text[:300]}")
        return resp.json() if resp.content else {}

    @staticmethod
    def _chunks(items: List[dict], size: int) -> Iterable[List[dict]]:
        for i in range(0, len(items), size):
            yield items[i:i + size]

    def ping(self) -> dict:
        """Vérifie le token (GET /api/user)."""
        resp = self.session.get(f"{self.base}/api/user", timeout=self.timeout)
        if resp.status_code == 401:
            raise CrmError("401 : token invalide.")
        resp.raise_for_status()
        return resp.json()

    # --- envois ---
    def push_prospects(self, rows: List[dict], source: Optional[str] = None) -> dict:
        """Envoie une liste de prospects (par lots). Renvoie les totaux cumulés."""
        agg = {"created": 0, "updated": 0, "skipped": 0, "total": None}
        for chunk in self._chunks(list(rows), self.chunk_size):
            res = self._post("prospects/bulk", {"prospects": chunk, "source": source})
            for k in ("created", "updated", "skipped"):
                agg[k] += res.get(k, 0)
            agg["total"] = res.get("total", agg["total"])
        return agg

    def push_tenders(self, rows: List[dict]) -> dict:
        """Envoie une liste d'appels d'offres (par lots)."""
        agg = {"created": 0, "updated": 0, "skipped": 0, "total": None}
        for chunk in self._chunks(list(rows), self.chunk_size):
            res = self._post("tenders/bulk", {"tenders": chunk})
            for k in ("created", "updated", "skipped"):
                agg[k] += res.get(k, 0)
            agg["total"] = res.get("total", agg["total"])
        return agg
