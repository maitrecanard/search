# Mémoire technique — EXEMPLE pré-rempli

**Marché** : Refonte du site internet de la Ville et application mobile
**Acheteur** : Ville d'Orange (84 — Vaucluse)
**Procédure** : MAPA (< 90 k€) · **Réf.** : idweb 26-47737
**Publié le** : 2026-05-12 · **Remise des offres** : 2026-06-03 à 12h00
**Avis** : https://www.boamp.fr/pages/avis/?q=idweb:26-47737

> ⚠️ **Exemple pédagogique** à adapter. Avant de t'en servir, **télécharge le
> DCE** sur le profil acheteur et **aligne chaque section sur le CCTP réel**.
> Les points marqués `‹CCTP›` sont à confirmer dans le cahier des charges.
> Remplace `‹TON …›` par tes infos.

---

## 0. Identification du candidat
- **Candidat** : ‹TON PRÉNOM NOM› — micro-entreprise / EURL · **SIRET** ‹…›
- Développeur web freelance, ‹X› ans d'expérience · ‹stack principale›
- Contact : ‹email› · ‹tél› · Portfolio : ‹URL›

## 1. Compréhension du besoin et du contexte
La Ville d'Orange souhaite **refondre son site internet** et se doter d'une
**application mobile** à destination de ses administrés. Au-delà de la
modernisation graphique, les enjeux d'une collectivité de cette taille sont :

- **Communication municipale** : actualités, événements, vie locale, valoriser
  le patrimoine (théâtre antique, arc — site UNESCO) et l'attractivité.
- **Services en ligne aux citoyens** : démarches/formulaires, prise de
  rendez-vous, signalements, état civil, annuaire des services. `‹CCTP›`
- **Mobilité** : une **application mobile** (alertes, agenda, démarches,
  notifications push) complémentaire au site responsive.
- **Obligations légales** : **accessibilité RGAA** (obligatoire pour le secteur
  public), **RGPD**, mentions légales, gestion des cookies.
- **Autonomie éditoriale** : les agents doivent pouvoir publier sans dépendre
  d'un prestataire (back-office simple).

> *Risques anticipés* : reprise des contenus existants, continuité de service
> pendant la bascule, niveau d'accessibilité à atteindre, interconnexions avec
> les outils métiers de la mairie `‹CCTP›`. Chacun est traité ci-dessous.

## 2. Démarche et méthodologie projet
Approche **itérative et collaborative**, jalonnée de validations formelles :

1. **Cadrage** (atelier de lancement) : arborescence, parcours utilisateurs,
   charte, périmètre exact des démarches en ligne, reprise de contenus.
2. **Conception UX/UI** : wireframes puis maquettes graphiques validées
   (accessibilité pensée dès la maquette : contrastes, tailles, navigation).
3. **Développement itératif** : sprints avec démos régulières ; environnement
   de **recette** dédié pour les valideurs municipaux.
4. **Recette & accessibilité** : tests fonctionnels, tests RGAA, corrections,
   **PV de recette**.
5. **Mise en production** : bascule planifiée (hors heures de pointe),
   redirections SEO, plan de retour arrière.
6. **Garantie & accompagnement** : formation des agents, garantie de
   correction, documentation.

Suivi : points d'avancement réguliers, dépôt **Git**, tableau de bord des
tâches, comptes rendus.

## 3. Solution technique proposée
> Choix justifié par la **maintenabilité**, l'**autonomie** de la collectivité
> et le **coût maîtrisé** (MAPA). À confirmer/adapter selon les exigences du
> `‹CCTP›` (CMS imposé éventuel, hébergement souverain, etc.).

- **Site** : CMS open-source éprouvé (‹WordPress durci / Drupal selon CCTP›),
  thème **sur-mesure responsive**, back-office simple pour les agents.
- **Application mobile** : **PWA** (installable, notifications) ou appli
  hybride (‹React Native / Flutter›) selon le besoin de présence sur stores —
  à arbitrer en cadrage selon budget et usages `‹CCTP›`.
- **Reprise de contenus** : inventaire, migration semi-automatisée + contrôle
  qualité, plan de **redirections 301** pour préserver le référencement.
- **Interfaçages** : agenda, démarches, cartographie, open data, SSO si requis
  `‹CCTP›`.
- **Performance & SEO** : optimisation des médias, cache, bonnes pratiques
  Core Web Vitals, **écoconception** (sobriété).
- **Hébergement** : offre **UE/souveraine** (RGPD), HTTPS, sauvegardes
  automatiques, supervision.

## 4. Accessibilité (RGAA), RGPD et sécurité
- **RGAA** : objectif de conformité ‹niveau visé›, tests par échantillon de
  pages, **déclaration d'accessibilité** + plan d'amélioration livrés.
- **RGPD** : minimisation des données, bandeau cookies conforme, mentions
  légales, registre, hébergement UE, durée de conservation.
- **Sécurité** : HTTPS, mises à jour de sécurité, gestion fine des rôles,
  sauvegardes restaurables, bonnes pratiques OWASP, journalisation.

## 5. Planning et délais (indicatif — à caler sur le `‹CCTP›`)
| Phase | Durée | Jalon |
|-------|-------|-------|
| Cadrage & arborescence | S+0 → S+2 | Validation arborescence/charte |
| Maquettes UX/UI | S+2 → S+5 | Validation maquettes |
| Développement | S+5 → S+11 | Démos de sprint |
| Reprise contenus & recette | S+11 → S+14 | PV de recette |
| Accessibilité & corrections | S+14 → S+16 | Déclaration RGAA |
| Mise en production & formation | S+16 → S+17 | Site en ligne + agents formés |

Engagement de **réactivité** : prise en compte des demandes sous ‹24-48 h›.

## 6. Compétences et références
- **Profil** : ‹années d'expérience›, ‹technos›, ‹certifs / RGAA si tu en as›.
- **Références comparables** : `‹2-3 projets : client, objet (site/appli),
  techno, résultat — idéalement un site institutionnel ou public›`.
- **Renforts** (si besoin) : ‹graphiste / expert RGAA en sous-traitance› pour
  sécuriser les volets design et accessibilité.

## 7. Maintenance, garantie et réversibilité
- **Garantie** : correction des anomalies pendant ‹3-12 mois› après mise en
  ligne.
- **TMA** (option) : forfait mensuel ‹…› ou au ticket — mises à jour, petites
  évolutions, supervision.
- **Réversibilité** : code source + base + documentation remis à la Ville,
  technologies standard et **non propriétaires**, transfert de compétences aux
  agents → aucune dépendance bloquante.

## 8. Engagements
Qualité (revue de code, tests), respect des délais, confidentialité,
accessibilité et RGPD by design, disponibilité et transparence sur l'avancement.

---

### Pièces à joindre à l'offre (rappel — vérifier le RC)
- Ce **mémoire technique**
- **Acte d'engagement** (AE) avec le **prix**
- **BPU / DPGF** (décomposition du prix : site, appli, reprise, formation, TMA)
- + dossier de **candidature** (DC1/DC2 ou DUME, attestations, RC pro,
  références) — voir `checklist-pieces.md`

> 💶 **Prix (MAPA < 90 k€)** : décompose clairement (conception, développement
> site, application mobile, reprise de contenus, formation, TMA en option). Un
> prix lisible + un mémoire qui colle au CCTP = meilleure note globale.
