# Mémoire technique — EXEMPLE pré-rempli

**Marché** : Refonte du site internet à destination des professionnels du tourisme
**Acheteur** : Comité Régional du Tourisme (CRT) Centre-Val de Loire (Orléans — 45)
**Procédure** : MAPA (< 90 k€) · **Réf.** : idweb 26-51899
**Publié le** : 2026-05-27 · **Remise des offres** : **2026-06-24 à 12h00**
**Avis** : https://www.boamp.fr/pages/avis/?q=idweb:26-51899

> ⚠️ **Exemple à adapter.** Avant usage, **télécharge le DCE** sur le profil
> acheteur et aligne chaque section sur le **CCTP** réel. Les points `‹CCTP›`
> sont à confirmer ; remplace les `‹TON …›` par tes infos.

---

## 0. Identification du candidat
- **Candidat** : ‹TON PRÉNOM NOM› — micro-entreprise / EURL · **SIRET** ‹…›
- Développeur web freelance, ‹X› ans d'expérience · ‹stack principale›
- Contact : ‹email› · ‹tél› · Portfolio : ‹URL›

## 1. Compréhension du besoin et du contexte
Le CRT Centre-Val de Loire anime et structure la **filière touristique
régionale**. Le site, objet de la refonte, ne s'adresse **pas au grand public**
mais aux **professionnels du tourisme** : offices de tourisme, hébergeurs,
restaurateurs, prestataires d'activités, institutionnels, porteurs de projet.

Enjeux d'un **portail pro** (et non d'un site vitrine grand public) :
- **Outiller la filière** : boîte à outils marketing, kits de communication,
  médiathèque (photos/vidéos régionales), modèles, chartes. `‹CCTP›`
- **Valoriser l'observatoire** : données de **fréquentation / chiffres clés**,
  études, baromètres — idéalement en **data-visualisation** claire.
- **Donner accès aux ressources & données** : actualités de la filière,
  dispositifs d'aide, agenda (webinaires/formations), et potentiellement la
  donnée touristique (**SIT / DATAtourisme / open data**). `‹CCTP›`
- **Espace professionnel** : compte/extranet pour les adhérents (contenus
  réservés, téléchargements, mise à jour de fiches). `‹CCTP›`
- **Obligations** : **accessibilité RGAA** (organisme public), **RGPD**.
- **Autonomie éditoriale** : les chargés de mission doivent publier seuls.

> *Risques anticipés* : reprise des contenus/médias existants, périmètre exact
> de l'espace pro et des connexions données (SIT/DATAtourisme), niveau RGAA
> attendu `‹CCTP›`. Traités ci-dessous.

## 2. Démarche et méthodologie projet
Approche **itérative et concertée** avec les équipes du CRT :

1. **Cadrage** : ateliers (besoins des pros, arborescence, parcours, périmètre
   de l'espace pro et des données à intégrer), reprise de contenus/médias.
2. **Conception UX/UI** : wireframes → maquettes validées, pensées
   **accessibles** dès la conception, orientées efficacité (audience pro).
3. **Développement itératif** : sprints + **démos** régulières sur un
   environnement de **recette** ouvert aux valideurs.
4. **Recette & accessibilité** : tests fonctionnels, tests RGAA, **PV de
   recette**.
5. **Mise en production** : bascule planifiée, **redirections 301**, plan de
   retour arrière.
6. **Garantie & accompagnement** : **formation** des chargés de mission,
   documentation, garantie de correction.

Pilotage : points d'avancement réguliers, dépôt **Git**, suivi des tâches,
comptes rendus.

## 3. Solution technique proposée
> Choix guidés par la **maintenabilité**, l'**autonomie** du CRT et le **coût
> maîtrisé** (MAPA). À confirmer selon le `‹CCTP›` (CMS imposé, hébergement,
> connexions données).

- **CMS** open-source éprouvé (‹WordPress durci / Drupal selon CCTP›), **thème
  sur-mesure responsive**, back-office simple multi-rédacteurs avec **workflow
  de validation**.
- **Espace pro / extranet** : authentification, contenus & téléchargements
  réservés, gestion des rôles (adhérents, OT, admin). `‹CCTP›`
- **Observatoire** : intégration des chiffres clés en **data-viz**
  (graphiques accessibles, exports). `‹CCTP›`
- **Données touristiques** : connexion **SIT / DATAtourisme / open data** si
  requis (affichage de l'offre, flux). `‹CCTP›`
- **Médiathèque** : bibliothèque de médias filtrable (droits d'usage),
  téléchargements de kits.
- **Reprise de contenus** : inventaire, migration + contrôle qualité,
  redirections SEO.
- **Recherche** interne performante, **multilingue** si demandé `‹CCTP›`.
- **Hébergement** : offre **UE/souveraine** (RGPD), HTTPS, sauvegardes,
  supervision ; **écoconception**.

## 4. Accessibilité (RGAA), RGPD et sécurité
- **RGAA** : conformité visée ‹niveau›, tests par échantillon, **déclaration
  d'accessibilité** + plan d'amélioration livrés.
- **RGPD** : minimisation, consentement cookies, mentions légales, registre,
  hébergement UE, durées de conservation (comptes pro inclus).
- **Sécurité** : HTTPS, MAJ de sécurité, gestion des accès de l'espace pro,
  sauvegardes restaurables, OWASP, journalisation.

## 5. Planning et délais (indicatif — à caler sur le `‹CCTP›`)
| Phase | Durée | Jalon |
|-------|-------|-------|
| Cadrage & arborescence | S+0 → S+2 | Validation arborescence/charte |
| Maquettes UX/UI | S+2 → S+5 | Validation maquettes |
| Développement (dont espace pro & data) | S+5 → S+12 | Démos de sprint |
| Reprise contenus & recette | S+12 → S+15 | PV de recette |
| Accessibilité & corrections | S+15 → S+17 | Déclaration RGAA |
| Mise en production & formation | S+17 → S+18 | Site en ligne + équipes formées |

Engagement de **réactivité** : prise en compte sous ‹24-48 h›.

## 6. Compétences et références
- **Profil** : ‹années d'expérience›, ‹technos›, ‹RGAA si maîtrisé›.
- **Références comparables** : `‹2-3 projets : portail/extranet, site
  institutionnel, intégration de données — idéalement secteur public ou
  tourisme›`.
- **Renforts** (si besoin) : ‹graphiste / expert RGAA / data-viz en
  sous-traitance› pour sécuriser design, accessibilité et observatoire.

## 7. Maintenance, garantie et réversibilité
- **Garantie** : correction des anomalies pendant ‹3-12 mois› après mise en
  ligne.
- **TMA** (option) : forfait mensuel ‹…› ou au ticket (MAJ, évolutions,
  supervision de l'espace pro).
- **Réversibilité** : code + base + médias + documentation remis au CRT,
  technologies **standard non propriétaires**, transfert de compétences →
  aucune dépendance bloquante.

## 8. Engagements
Qualité (revue de code, tests), respect des délais, confidentialité,
accessibilité & RGPD by design, disponibilité et transparence sur l'avancement.

---

### Pièces à joindre (rappel — vérifier le RC)
- Ce **mémoire technique** · **Acte d'engagement** (prix) · **BPU/DPGF**
- Dossier de **candidature** (DC1/DC2 ou DUME, attestations, RC pro, références)
  — voir `checklist-pieces.md`

> 💶 **Prix (MAPA < 90 k€)** : décompose (conception, développement,
> **espace pro**, **intégration données/observatoire**, reprise de contenus,
> formation, TMA en option). Un BPU lisible + un mémoire collé au CCTP = la
> meilleure note globale.
>
> 🎯 **Différenciateur** sur ce marché : montre que tu comprends la **filière
> tourisme** (audience pro ≠ grand public) et la **donnée touristique**
> (SIT/DATAtourisme). C'est ce qui te démarque d'une réponse générique.
