#!/usr/bin/env bash
# Veille MAPA — exécuté par cron (hebdo). Régénère MAPA_OUVERTS.md et le pousse
# si la liste a changé. Journalise dans mapa_refresh.log.
set -u
set -o pipefail   # un pipe ... | sed renvoie le code du 1er échec, pas celui de sed
export HOME=/home/mathieu
export PATH=/usr/local/bin:/usr/bin:/bin
REPO=/home/mathieu/search
BRANCH=prospection/result-100
cd "$REPO" || exit 1

ts() { date -u +'%Y-%m-%dT%H:%M:%SZ'; }
echo "[$(ts)] --- refresh MAPA ---"

git checkout "$BRANCH" >/dev/null 2>&1
git pull --ff-only origin "$BRANCH" >/dev/null 2>&1

python3 refresh_mapa.py || { echo "[$(ts)] échec refresh_mapa"; exit 1; }

# Génère un dossier de réponse pré-rempli pour chaque MAPA encore ouvert.
python3 generer_dossier.py --open || echo "[$(ts)] avertissement: génération des dossiers incomplète"

# Les dossiers (dossiers/) restent LOCAUX (données perso) : on ne pousse que la
# liste publique des MAPA ouverts.
git add MAPA_OUVERTS.md >/dev/null 2>&1
if ! git diff --cached --quiet 2>/dev/null; then
  n=$(ls -d dossiers/*/ 2>/dev/null | grep -v _archive | wc -l)
  git commit -m "Rafraîchissement hebdo des MAPA ouverts" >/dev/null 2>&1
  if git push origin "$BRANCH" >/dev/null 2>&1; then
    echo "[$(ts)] MAPA_OUVERTS.md + dossiers mis à jour et poussés (${n} dossiers)"
  else
    echo "[$(ts)] commit OK mais push échoué (vérifier gh/credentials)"
  fi
else
  echo "[$(ts)] aucun changement"
fi

# Ciblage recentré sur la NICHE INDUSTRIE : les collectes free-work
# (salesforce / intranet / webapp) ont été retirées — non poussées au CRM.

# --- NICHE INDUSTRIE : aéronautique + logistique + conseil IT (SIRENE, PME/ETI) ---
echo "[$(ts)] recherche niche industrie…"
if python3 main.py --source niche --target 100 --out result_niche \
     2>&1 | sed "s/^/[$(ts)] niche: /"; then
  echo "[$(ts)] collecte niche terminée"
else
  echo "[$(ts)] avertissement: collecte niche incomplète"
fi

# --- Envoi des données au CRM distant (si configuré) ---
if [ -f "$REPO/.crm.env" ]; then
  set -a; . "$REPO/.crm.env"; set +a
  if [ -n "${CRM_URL:-}" ] && [ -n "${CRM_TOKEN:-}" ] && \
     [ "$CRM_URL" != "https://crm.exemple.fr" ]; then
    echo "[$(ts)] envoi au CRM ($CRM_URL)…"
    python3 push_to_crm.py 2>&1 | sed "s/^/[$(ts)] crm: /"
  else
    echo "[$(ts)] .crm.env présent mais non configuré → envoi CRM ignoré"
  fi
else
  echo "[$(ts)] pas de .crm.env → envoi CRM désactivé"
fi
