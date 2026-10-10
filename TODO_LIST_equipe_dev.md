# PLAN DE TRAVAIL — ERP Versements de Bus
## Répartition d'équipe et todo list complet — 3 développeurs
**Version 1.0 — 09/10/2026 | Durée MVP : ~14 semaines (conception → pilote prêt)**

---

## 1. Équipe et répartition des rôles

| Dev | Rôle principal | Périmètre |
|---|---|---|
| **D1 — Backend** | API, base de données, sécurité, audit | PostgreSQL, API REST, auth/OTP, multi-tenant, journal d'audit, calculs (écarts, dettes, scores), exports |
| **D2 — Mobile Chauffeur** | PWA/app chauffeur | Saisie versements/dépenses/pannes (3 étapes max), notes vocales, mode dégradé, malgache |
| **D3 — Web Propriétaire** | Interface propriétaire + dashboard | Validation/accusés, tableaux de bord analytiques, alertes, messagerie, administration tenant |

> ⚠️ **Contrainte clé (CDC §5)** : mobile first, saisie ≤ 3 étapes, malgache dès le MVP, pages < 3s sur 3G. Chaque tâche D2/D3 doit passer ces critères en Definition of Done.

### Conventions communes (à valider en semaine 1)
- Git : `main` (protégée) + branches `feat/xxx`, PR obligatoires avec 1 review (par le dev non-auteur du module si possible)
- Definition of Done : code review ✅ + tests passent ✅ + migration BDD réversible ✅ + doc API mise à jour ✅ + critères perf/mobile respectés ✅
- Daily standup 15 min (message vocal accepté), rétro en fin de sprint
- Stack validée : **PostgreSQL + Django (Backend D1) + Ionic Vue 3 & Capacitor (Mobile Chauffeur D2)**

---

## 2. Vue d'ensemble des sprints

| Sprint | Semaines | Objectif |
|---|---|---|
| **S0** | 1 | Cadrage technique : choix stack, conventions, environnements, maquettes filaires |
| **S1** | 2–3 | Conception : modèle de données, maquettes testées, modèle de menaces |
| **S2** | 4–5 | Fondations : BDD, auth multi-tenant, CI/CD, CRUD bus/chauffeurs/lignes |
| **S3** | 6–7 | Cœur métier : versements + accusé, écarts, motifs, dettes |
| **S4** | 8–9 | Dépenses + remboursements, incidents/pannes, notifications |
| **S5** | 10–11 | Messagerie, dashboard analytique, alertes, score fiabilité, exports |
| **S6** | 12–13 | Audit, durcissement sécurité, tests, correction des retours |
| **S7** | 14 | Bugfix final, données de démo, préparation pilote |

---

## 3. TODO LIST COMPLÈTE

### 🔵 SPRINT S0 — Cadrage (semaine 1)

#### Organisation / transverse
- [ ] **[TOUS]** Réunion de kickoff : lecture du CDC validé v1.0, alignement sur les objectifs et KPI
- [x] **[D1]** Trancher la stack backend : **Django** validé (modèles créés et migrés)
- [x] **[D2]** Trancher le frontend mobile : **Ionic 9 + Vue.js 3 + Capacitor** validé (projet initialisé) + prototype de saisie en 3 étapes sur petit écran Android
- [ ] **[D3]** Choisir lib de graphiques/dashboard + maquette filaire des écrans propriétaire (papier ou Figma)
- [ ] **[TOUS]** Mettre en place : repo Git, environnements dev (local + staging), règles de protection de branche
- [ ] **[TOUS]** Définir les conventions : nommage, langue du code (anglais), messages de commit, format des PR
- [ ] **[D1]** Initialiser la CI (lint + tests auto sur chaque PR)

**Livrable S0** : stack validée, repo prêt, conventions écrites, maquettes filaires v0

---

### 🔵 SPRINT S1 — Conception (semaines 2–3)

#### D1 — Backend
- [ ] Modèle de données complet (tables du CDC §7 : tenant, user, bus, chauffeur, affectation, ligne, journée_service, versement, dette, dépense, remboursement, incident, message, notification, audit_log)
- [ ] MCD/MLD + migrations initiales (colonne `tenant_id` partout, UUID en clés externes)
- [ ] Spécification de l'API REST (endpoints, payloads, codes erreur) — document partagé
- [ ] **Modèle de menaces** (CDC §10, phase 1) : liste des menaces + parades mappées sur SEC-01 à SEC-13 — revue à 3

#### D2 — Mobile Chauffeur
- [ ] 5–8 maquettes testées auprès d'au moins 3 chauffeurs réels (même informel) : saisie versement, dépense, panne, historique, messagerie
- [ ] Version malgache des libellés clés (faire relire par un natif)
- [ ] Prototype cliquable : parcours « déclarer un versement » en 3 étapes max, boutons larges
- [ ] Spécifier la tolérance connexion instable : file d'attente locale, reprise sur erreur (pas de vrai offline, mais pas de perte de saisie)

#### D3 — Web Propriétaire
- [ ] Maquettes : tableau de bord, liste versements (avec accusé en 1 tap), validation dépenses, vue bus/chauffeurs, alertes, messagerie
- [ ] Définir les 12 indicateurs du dashboard (RF-27 à RF-32) et leur formule exacte — valider avec D1
- [ ] Spécifier le système de notifications (push FCM + fallback SMS) et les événements déclencheurs
- [ ] Recueillir et consolider les retours d'entretiens (phase 0 CDC) en fiches utilisateurs

**Livrable S1** : MCD validé, API spec v1, maquettes validées par de vrais chauffeurs, modèle de menaces signé

---

### 🔵 SPRINT S2 — Fondations (semaines 4–5)

#### D1 — Backend
- [ ] Auth téléphone + OTP (ou mot de passe robuste) + limitation de tentatives + verrouillage temporaire [SEC-03]
- [ ] Middleware multi-tenant : vérification `tenant_id` à chaque requête [SEC-01]
- [ ] Autorisation par objet : un chauffeur ne voit que ses données [SEC-02]
- [ ] Sessions courtes, révocation, déconnexion auto [SEC-04]
- [ ] CRUD Bus [RF-01], Chauffeurs [RF-02], affectations avec historique, Lignes [RF-04]
- [ ] Journal d'audit générique (who/what/when/ancienne/nouvelle valeur) [RF-39/40]
- [ ] Setup : HTTPS, en-têtes sécu, cookies HttpOnly/Secure/SameSite, CSRF [SEC-08]
- [ ] Rate limiting API + UUID non devinables [SEC-11]
- [ ] Upload fichiers sécurisé : whitelist types, taille max, renommage, hors webroot, strip EXIF [SEC-07]

#### D2 — Mobile Chauffeur
- [x] Squelette mobile Ionic / Capacitor : navigation, gestion de session, bascule FR/MG
- [x] Écrans : login OTP / mot de passe, bus assigné, profil
- [x] Déclaration journée de service : lignes effectuées (début/fin de service) [RF-05/06]
- [x] Saisie d'un versement en 3 étapes [RF-07] : bus/ligne, montant versé + calcul écart + motif, confirmation
- [x] File d'attente locale : stockage local hors-ligne en cas de réseau dégradé

#### D3 — Web Propriétaire
- [ ] Squelette web : auth, layout, gestion des rôles (propriétaire/gérant)
- [ ] CRUD Bus / Chauffeurs / Lignes (interfaces admin) [RF-01/02/04]
- [ ] Définition des versements attendus par bus/ligne/type de jour [RF-03]
- [ ] Écran liste des versements avec statuts (déclaré/accusé/validé/contesté)

**Livrable S2** : on peut créer comptes, bus, chauffeurs, lignes, attendus ; un chauffeur peut déclarer ; tout est audité et isolé par tenant

---

### 🔵 SPRINT S3 — Cœur métier : Versements (semaines 6–7)

#### D1 — Backend
- [ ] Cycle de statuts versement : déclaré → accusé → validé / contesté [RF-07a, RF-10]
- [ ] Calcul automatique écart attendu vs réel [RF-08]
- [ ] Motif obligatoire si écart négatif + liste fermée + commentaire [RF-09]
- [ ] Versements partiels → création de dette reportée avec échéance [RF-11]
- [ ] Verrouillage après validation + écritures rectificatives tracées [RF-12]
- [ ] Génération de reçu PDF/message à l'accusé/validation [RF-13]
- [ ] Endpoint accusé « 1 tap » propriétaire + relance auto à 24 h
- [ ] **Anti-fraude motifs** : stats de répartition par chauffeur, exclusion du motif « peu de passagers » du calcul d'écart [RF-09a]

#### D2 — Mobile Chauffeur
- [ ] Intégration : déclaration → statut « déclaré » + reçu reçu après accusé [RF-07/13]
- [ ] Saisie motif + commentaire quand écart négatif [RF-09]
- [ ] Écran « mes dettes » : soldes reportés et échéances [RF-11]
- [ ] Historique personnel (lecture seule) [chauffeur ne voit que ses données]

#### D3 — Web Propriétaire
- [ ] File d'accusés en attente : liste prioritaire, accusé en 1 tap, contestation avec motif [RF-07a/10]
- [ ] Écran détail versement : attendu vs réel, écart, motif, justificatifs, fil d'audit
- [ ] Gestion des dettes : échéances, rappels
- [ ] Écritures rectificatives : interface de contre-passation [RF-12]

**Livrable S3** : le cycle complet déclarer→accuser→valider fonctionne de bout en bout, dettes automatiques, reçus générés — **c'est la fonctionnalité n°1 du CDC, elle doit être impeccable**

---

### 🔵 SPRINT S4 — Dépenses, incidents, notifications (semaines 8–9)

#### D1 — Backend
- [ ] CRUD dépenses : catégories, montant, date, bus, payé par [RF-14/16]
- [ ] Justificatif photo + seuil obligatoire paramétrable (défaut 20 000 Ar) [RF-15]
- [ ] Workflow validation/refus dépense avec motif [RF-17]
- [ ] Workflow remboursement : espèces (avec accusé) ou déduction sur prochain versement [RF-16a]
- [ ] Incidents : panne/absence avec type, photos, heure, statut bus temps réel [RF-18 à RF-22]
- [ ] Notifications : événements clés → push FCM (+ fallback SMS) [RF-25]
- [ ] Annonce collective + messages liés à un objet (versement/incident) [RF-23/26]

#### D2 — Mobile Chauffeur
- [ ] Saisie dépense en 3 étapes + photo justificatif [RF-14/15]
- [ ] Écran « mes remboursements » : à rembourser / déduits / reçus [RF-16a]
- [ ] Signalement panne/absence : type, description, photos, note vocale, « rentré au garage » [RF-18/19]
- [ ] Messagerie : conversations + notes vocales + pièces jointes [RF-23/24]

#### D3 — Web Propriétaire
- [ ] File de validation dépenses (avec zoom justificatif) [RF-17]
- [ ] Gestion des remboursements : mode espèces ou déduction [RF-16a]
- [ ] Vue temps réel statut des bus (en service / panne / arrêt) [RF-21]
- [ ] Historique pannes par bus et par chauffeur [RF-22]
- [ ] Messagerie propriétaire (conversations + annonces + objets liés) [RF-23/26]
- [ ] Centre de notifications

**Livrable S4** : dépenses et remboursements bouclés, incidents temps réel, messagerie fonctionnelle

---

### 🔵 SPRINT S5 — Analytique & alertes (semaines 10–11)

#### D1 — Backend
- [ ] Agrégations dashboard : dépenses par période/catégorie [RF-27], versements par période/bus/chauffeur/ligne [RF-28], rentabilité nette [RF-31], disponibilité [RF-32]
- [ ] Classement lignes rentables [RF-29], moyenne par jour de semaine [RF-30]
- [ ] Moteur d'alertes paramétrable : seuil versement (défaut 70 %), heure limite (défaut 19 h), incidents récurrents (≥ 3/7 jours) [RF-35/36/37]
- [ ] Score de fiabilité chauffeur (régularité, écarts, contestations, motifs récurrents) [RF-38]
- [ ] Vue « chauffeurs à risque » consolidée [RF-38a]
- [ ] Exports Excel/PDF + rapport auto hebdo/mensuel [RF-33/34]
- [ ] Stats d'usage anonymisées plateforme (consommation, aucune donnée métier)

#### D2 — Mobile Chauffeur
- [ ] Push/SMS : reçus, validation dépense, réponses aux incidents
- [ ] Bascule malgache complète (relecture native finale)
- [ ] Optimisations 3G : lazy loading, compression images, < 3s par page

#### D3 — Web Propriétaire
- [ ] Tableau de bord complet : KPIs, graphiques, filtres période/bus/chauffeur/ligne [RF-27 à RF-33]
- [ ] Panneau alertes avec actions rapides (appeler, contester, marquer vu)
- [ ] Vue « chauffeurs à risque » [RF-38a]
- [ ] Rapports auto hebdo/mensuel (email) [RF-34]
- [ ] Exports Excel/PDF [RF-33]

**Livrable S5** : le propriétaire a sa vision analytique complète — le 2ᵉ objectif du CDC tient

---

### 🔵 SPRINT S6 — Audit, sécurité, tests (semaines 12–13)

#### D1 — Backend
- [ ] Interface journal d'audit (consultation propriétaire, ajout seul) [RF-40]
- [ ] Vérification conformité SEC-01 à SEC-13 (checklist + preuves)
- [ ] Chiffrement données sensibles au repos + sauvegardes [SEC-09]
- [ ] Secrets hors du code, dépendances à jour [SEC-12]
- [ ] Tests de charge : dashboard < 5s sur 12 mois de données (CDC §5)
- [ ] Préparer le dossier pour le test d'intrusion externe

#### D2 — Mobile Chauffeur
- [ ] Tests sur petits Android (Android 8+) en conditions réelles 3G
- [ ] Test avec utilisateur malgache non technophile (recruter 1–2 testeurs)
- [ ] Corrider les parcours > 3 étapes

#### D3 — Web Propriétaire
- [ ] Tests cross-browser (Chrome, Firefox)
- [ ] Revue UX complète avec les maquettes S1 : tout ce qui a dérivé est corrigé
- [ ] Jeu de données de démo réaliste (20 bus, 3 mois d'historique)

#### TOUS
- [ ] Tests d'intégration bout-en-bout des 3 parcours critiques : versement, dépense→remboursement, panne
- [ ] Bugfix marathon + gel des fonctionnalités (feature freeze)
- [ ] **Test d'intrusion externe** (CDC §10) puis correction des findings

**Livrable S6** : MVP sécurisé, audit visible, tests passés, findings d'intrusion corrigés

---

### 🔵 SPRINT S7 — Pilote (semaine 14)

- [ ] **[D1]** Script de migration/seed pour un tenant pilote + monitoring erreurs (Sentry ou équivalent)
- [ ] **[D2]** Formation chauffeurs : guide illustré malgache, accompagnement premier jour
- [ ] **[D3]** Formation propriétaires : guide + session en main
- [ ] **[TOUS]** Semaine pilote encadrée : support quotidien, bugfix hot
- [ ] **[TOUS]** Tableau de suivi des KPI pilote (écarts, adoption, temps de clôture)
- [ ] **[D1]** Ajustement des seuils par défaut selon retours (annexe 12.1 CDC)
- [ ] **[TOUS]** Rétro pilote → backlog V2

---

## 4. Vue synthétique par dev

### D1 — Backend (~toutes les semaines)
S1: modèle de données + API spec + menaces → S2: auth/tenant/audit/CRUD → S3: cycle versements/dettes/anti-fraude → S4: dépenses/remboursements/incidents/notifs → S5: dashboard/alertes/score/exports → S6: audit/securité/tests/perf → S7: seed/monitoring

### D2 — Mobile Chauffeur
S1: maquettes terrain + malgache → S2: squelette/auth/lignes → S3: versements/dettes/historique → S4: dépenses/pannes/messagerie → S5: notifs/perf/malgache final → S6: tests terrain Android 8+/3G → S7: formation chauffeurs

### D3 — Web Propriétaire
S1: maquettes + indicateurs + notif spec → S2: admin CRUD/attendus → S3: accusés/détails/dettes/rectificatifs → S4: validations/remboursements/statuts bus/messagerie → S5: dashboard/alertes/rapports/exports → S6: tests UX/démo → S7: formation propriétaires

---

## 5. Points de contrôle (go/no-go)

| Quand | Gate |
|---|---|
| Fin S1 | Maquettes validées par de vrais chauffeurs + modèle de menaces signé → sinon NE PAS coder |
| Fin S3 | Cycle versement testé bout en bout → c'est le cœur, aucun raccourci |
| Fin S5 | Dashboard < 5s sur 12 mois de données (mesuré, pas estimé) |
| Fin S6 | Test d'intrusion : zéro finding critique ouvert |
| Fin S7 | KPI pilote : clôture < 2 min, adoption traquée, écarts mesurés |

---

## 6. Backlog V2 (hors MVP, à ne pas commencer)
- [ ] GPS + consentement localisation (SEC-13)
- [ ] Mobile money + webhooks signés/idempotents (SEC-10)
- [ ] Mode hors-ligne complet + sync
- [ ] Multi-propriétaires complet (flottes partagées)
- [ ] Entretien + documents avec alertes d'échéance
- [ ] Rôle Receveur
