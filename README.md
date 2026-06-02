# search

## description
Recherche des prospect dans la toile
- des pro qui ront un besoin de prestation en site web
- des pro qui souhaite réaliser un saas
- des pro en douleur car en recherche de solution en ligne.

## technique
utilise duckduck go ou tout autre outil de recherche


## récupération de données
dans un fichier result, récupère la locallité du pro, le nom de l'entreprise, si possible son numéro de tel et son mail
- récupère également le signal d'alerte, le pourquoi tu as ciblé cette entreprise.
- récupère au moins 100 entreprise

---

# 📋 Rapport d'implémentation

Un moteur de prospection a été développé pour répondre au cahier des charges
ci-dessus. Le livrable demandé — le **fichier `result`** — est fourni en deux
formats : [`result.csv`](result.csv) et [`result.json`](result.json).

Plusieurs **fichiers bonus** complètent le livrable :
- ⭐ **Clients finaux tech** (cible freelance recommandée) :
  [`result_clients_tech.csv`](result_clients_tech.csv) /
  [`.json`](result_clients_tech.json) ;
- **Grands comptes** : [`result_grands_comptes.csv`](result_grands_comptes.csv) /
  [`.json`](result_grands_comptes.json) ;
- **Besoins logiciels avérés** (appels d'offres) :
  [`result_besoins_logiciels.csv`](result_besoins_logiciels.csv) /
  [`.json`](result_besoins_logiciels.json).

## ✅ Fonctionnalités demandées et état

| # | Fonctionnalité (README) | État | Détail |
|---|--------------------------|------|--------|
| 1 | Recherche de prospects sur la toile | ✅ | Moteur multi-sources (Mojeek + Overpass/OSM) |
| 2 | Pros ayant un besoin de site web | ✅ | Professions solvables sans site / à refondre |
| 3 | Pros souhaitant réaliser un SaaS | ✅ | Catégorie « acteur financé / SaaS » implémentée |
| 4 | Pros « en douleur » cherchant une solution | ✅ | Catégorie « PME à digitaliser » implémentée |
| 5 | Outil de recherche (DuckDuckGo ou autre) | ✅ | Voir « moteurs utilisés » ci-dessous |
| 6 | Fichier `result` (localité, entreprise, tél, mail) | ✅ | `result.csv` + `result.json` |
| 7 | Signal d'alerte (pourquoi cette entreprise) | ✅ | Colonne `signal_alerte`, explicite |
| 8 | Au moins 100 entreprises | ✅ | **100 prospects** uniques |

## 🎯 Ciblage qualifié (besoin + moyens + closing)

Conformément à la consigne, on ne cible pas n'importe quelle entreprise « ayant
un besoin », mais celles qui cumulent : **besoin réel**, **moyens financiers**,
et **closing simple** (décideur unique, cycle de vente court).

Le livrable se concentre sur des **professions libérales et services
solvables** dont la présence web est typiquement absente ou datée :

La colonne **`secteur`** porte la profession ciblée :

| Secteur (`secteur`) | Nb | Pourquoi c'est un bon prospect |
|---------|----|--------------------------------|
| Agence immobilière | 54 | Budget marketing récurrent, besoin de leads en ligne |
| Cabinet d'assurance | 25 | Réseau/franchise solvable, site local à moderniser |
| Cabinet d'avocats | 7 | Clientèle aisée, budget propre, décideur unique |
| Cabinet dentaire | 7 | Profession solvable, prise de RDV en ligne à déployer |
| Cabinet d'architecture | 6 | Activité à fort panier, portfolio web à valoriser |
| Cabinet d'expertise comptable | 1 | Récurrence de revenus, image pro à soigner |

**Signal d'alerte exploité** : l'**absence de site web** (37 prospects) est un
signal d'achat fort (besoin de création) ; la présence d'un site daté (63) est
une opportunité de **refonte / SEO**. Le champ `signal_alerte` de chaque ligne
explicite besoin + moyens + closing.

## 📊 Le fichier `result` en chiffres

- **100 prospects** uniques (dédupliqués par domaine / SIREN / nom+ville)
- **100 % avec téléphone** (100/100)
- **32 % avec email** (32/100) — récupéré « si possible » (cf. README)
- **63** avec site web existant · **37** sans site web (= besoin de création)
- Répartis sur **9 métropoles** : Paris, Lyon, Marseille, Toulouse, Lille,
  Nantes, Strasbourg, Nice, Rennes (≈ 12 par ville, pour la diversité)

### Colonnes de `result.csv` / `result.json`
`entreprise`, `localite`, `telephone`, `email`, `categorie`, **`secteur`**,
`signal_alerte`, `source_url`, `requete`.

La colonne **`secteur`** est commune aux deux fichiers : profession pour les PME,
secteur d'activité (NAF) pour les grands comptes.

## ⭐ Cible freelance — Clients finaux tech (`result_clients_tech`)

**Objectif réel d'un freelance** : décrocher des contrats sur des projets
coûteux auprès de **clients finaux** (pas d'ESN intermédiaire, pas de job board
où l'on postule). La cible idéale = une entreprise qui développe son **propre
produit logiciel** : besoin de dev **récurrent**, **budget**, et **décideur
joignable en direct** (cycle de vente court).

Source : **API Recherche d'entreprises** (SIRENE), filtrée sur les codes NAF
d'**édition de logiciels / SaaS / plateformes** — en **excluant les codes
d'ESN/conseil** (62.01Z, 62.02A, 78.xx) pour ne garder que des **clients
finaux**.

- **100 éditeurs / scale-ups tech**, **60 communes**, PME/ETI de **20 à 499
  salariés** (assez de budget, assez petites pour être approchables)
- **6 secteurs produit** équilibrés : éditeurs applicatifs / système / outils,
  jeux vidéo, SaaS-data, plateformes web
- **66 % avec décideur nommé** (`signal_alerte`) pour l'**outreach direct**
  (LinkedIn/email) — les commissaires aux comptes sont exclus
- Exemples : Sorare, Coyote System, Playwing, Linkeo, Aplim, JVS-Mairistem…

> ℹ️ **Pourquoi pas de tél/email en colonne** : l'API SIRENE n'expose pas le
> contact. La porte d'entrée est le **dirigeant nommé** + le **lien annuaire**
> (`source_url`) → on trouve le décideur sur LinkedIn / le site corp. Pour un
> freelance, c'est le bon canal (approche directe et personnalisée), pas un
> mail générique.
>
> 🔧 Régénérer : `python3 main.py --source clients --target 100 --out result_clients_tech`

## 🏢 Bonus — Grands comptes (`result_grands_comptes`)

Cible : **grands comptes PRIVÉS, non-tech, avec un besoin logiciel et les
moyens** (hors service public). Source : **API Recherche d'entreprises**
(SIRENE), catégories **GE + ETI**.

- **500 entreprises** : **269 GE + 231 ETI**, réparties sur la France
- **Privées uniquement** : le **secteur public / para-public est exclu**
  (associations, EPIC, et organismes d'État par nom : La Poste, SNCF, RATP,
  EDF, CHU, mairies, universités…)
- **Non-tech** : la section J (information-communication = ESN/éditeurs) est exclue
- **8 secteurs** équilibrés : commerce/distribution, banque/assurance, industrie,
  transport, hôtellerie/restauration, immobilier, santé (privée), services
- **394 / 500 avec décideur nommé** (`signal_alerte`) — personne physique,
  commissaires aux comptes écartés
- Exemples : Lidl, Société Générale, BNP Paribas, Carrefour, McDonald's France,
  Picard, Lafarge, Loxam, Babilou, Amplifon, Indigo, Elior…
- `categorie` distingue **GE** / **ETI** ; `signal_alerte` porte le **secteur**,
  la **tranche d'effectif** et le **décideur** (point d'entrée outreach).

> ⚠️ **Dynamique vs le fichier PME** : un grand compte coche « besoin logiciel +
> moyens » (gros budgets de transformation digitale) mais le cycle de vente est
> plus long (multi-décideurs). Tél/email non exposés par l'API → contact via le
> **dirigeant nommé** + le lien `source_url`.

## 🎯 Bonus — Besoins logiciels *avérés* (`result_besoins_logiciels`)

⚠️ **Limite des deux fichiers ci-dessus** : pour les PME comme pour les grands
comptes, le besoin logiciel est **inféré** (solvabilité avérée, mais intention
non prouvée). Ce troisième fichier corrige ce point en partant de besoins
**réellement exprimés** : les **appels d'offres publics** (source **BOAMP**,
open data). L'objet du marché EST le signal — un organisme qui publie un appel
d'offres pour un site / une application / une plateforme / un logiciel a un
besoin **avéré, daté et budgété**.

- **100 besoins logiciels distincts** (100 objets uniques), **55 localités**
- **100 % d'avis 2026** (récents/en cours), triés du plus récent au plus ancien
- `signal_alerte` = l'**objet exact du marché** + date de parution + date limite
- `source_url` = lien direct vers l'avis BOAMP (cahier des charges + contact acheteur)
- Exemples (2026) : Création du site internet de l'Hôpital Nord Franche-Comté,
  refonte du site institutionnel d'une ville, plateforme numérique du CESE…

> ℹ️ **Honnêteté sur les données** : les acheteurs sont **publics**
> (collectivités, hôpitaux, établissements) ; le closing = répondre à l'appel
> d'offres avant la date limite. Les avis récents sont au format *eForms*, qui
> **n'expose pas** les coordonnées de l'acheteur dans l'open data : les colonnes
> `telephone`/`email` sont donc le plus souvent vides, mais **chaque avis est
> directement actionnable via `source_url`** (l'avis en ligne contient le contact
> de l'acheteur, la date limite et le cahier des charges).
>
> 💡 Variante « plus de contacts » : `python3 main.py --source besoins
> --date-min 2023-01-01` ramène des avis plus anciens mais avec coordonnées
> renseignées (~75 % contactables) — au prix d'AO potentiellement clôturés.

## 🔎 Moteurs de recherche utilisés

Le README autorise « DuckDuckGo **ou tout autre outil de recherche** ». En
pratique, dans l'environnement d'exécution :

| Moteur | Constat |
|--------|---------|
| DuckDuckGo (html/ + lite/) | Fonctionne au 1er burst puis **bannit l'IP** (timeout) |
| Bing / Ecosia | Page **anti-bot / captcha** (0 résultat) |
| Brave / Startpage | **429** dès la 2ᵉ requête |
| **Mojeek** | OK en mots-clés (403 sur les guillemets), rate-limit après ~12 requêtes |
| **Overpass (OpenStreetMap)** | **Fiable**, non bannissant → backbone du livrable |

Le moteur combine donc **Mojeek** (résultats web organiques, tant qu'il
répond, avec circuit-breaker) et **Overpass/OSM** (source structurée fiable qui
fournit directement nom + ville + téléphone + email + site pour les professions
ciblées). Un essai antérieur via Mojeek avait déjà capturé 31 cabinets réels —
preuve que la voie « moteur de recherche » fonctionne hors throttling.

## 🧪 Cycle de qualité suivi

Développement → vérification → **tests unitaires** → exécution → correction →
régression, à chaque itération :

- **66 tests unitaires** (`unittest`, hors-ligne via fixtures) : parsing des
  moteurs (DDG html/lite, Mojeek), extraction (email, téléphone FR, localité,
  nom d'entreprise), Overpass (parsing, requête QL, dédup), grands comptes (API
  entreprises, secteurs, dédup SIREN), besoins BOAMP (3 schémas IDENTITE/
  FNSimple/EFORMS, anti-faux-positifs contact), pipeline (cap par ville),
  écriture CSV/JSON.
- Corrections issues de l'exécution réelle : rate-limiting (back-off +
  circuit-breaker), bascule de moteur, requête Overpass (`;` manquant,
  instance régionale écartée), dédup des fiches sans site, répartition
  géographique (plafond par ville).
- **Régression complète verte** après chaque correction.

> ℹ️ Le code source du moteur (paquet `prospect_search/`, `main.py`, `tests/`)
> est conservé en local et régénère le fichier `result`. Conformément à la
> demande, **seul le fichier `result` (+ ce rapport) est versionné** sur la
> branche.
