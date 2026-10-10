# État d'Avancement du Projet — Application Mobile & Liaison BDD

> **Date** : 10 Octobre 2026  
> **Composant** : Mobile Chauffeur (Ionic 9 + Vue.js 3 + Capacitor) & Backend (Django REST)  
> **Auteur / Équipe** : D2 (Mobile) & D1 (Backend)

---

## 1. Réponse directe : Est-ce déjà relié à une base de données ou est-ce statique ?

L'application mobile actuelle n'est **ni un simple site statique figé**, **ni encore connectée en temps réel à la base de données du serveur**. 

Elle se situe au stade **prototype fonctionnel autonome avec persistance locale** :

```
┌────────────────────────────────┐         (Non connecté)          ┌────────────────────────────────┐
│        MOBILE CHAUFFEUR        │       ───────────────X──────>   │        SERVEUR BACKEND         │
│  - Interface interactive       │                                 │  - Django REST Framework       │
│  - Calculs dynamiques (écarts) │                                 │  - BDD PostgreSQL / SQLite     │
│  - Stockage local smartphone   │                                 │    (Modèles déjà créés : bus,  │
│    (Session, i18n, Offline)    │                                 │     chauffeurs, versements...) │
└────────────────────────────────┘                                 └────────────────────────────────┘
```

### Ce qui est dynamique & fonctionnel sur le mobile :
- **Logique métier & calculs temps réel** : calcul automatique de l'écart `Écart = Montant versé - Montant attendu`, obligation conditionnelle de saisir un motif en cas de déficit (anti-fraude [RF-09]).
- **Stockage local sur le téléphone (`localStorage`)** :
  - La session du chauffeur (token, identifiant).
  - La préférence de langue (**Français** ou **Malgache**).
  - La **file d'attente hors-ligne (`offlineQueue`)** : si vous déclarez un versement, il est conservé dans la mémoire du téléphone prêt à être synchronisé.
- **Bascule multilingue instantanée** : interface 100% traduite en Malgache (*Fandoavana*, *Elanelana*, *Fahasimbana*...) et en Français.

### Ce qui est actuellement simulé (Mock / Démo) :
- Les données initiales du chauffeur (Nom : *Jean Rakotondrabe*, Bus : *1234 TAB*, Ligne : *Ligne 133*, Attendu : *120 000 Ar*).
- La connexion accepte actuellement n'importe quel mot de passe en mode démo si le serveur backend n'est pas allumé.

---

## 2. État d'avancement détaillé du Mobile Chauffeur (D2)

| Écran / Fonctionnalité | Statut | Type de données | Détails |
|---|---|---|---|
| **Squelette & Thème Ionic** | ✅ Terminé | Natif mobile | Composants Ionic 9, navigation par onglets, responsive mobile |
| **Bilingue Français / Malgache** | ✅ Terminé | Fichiers JSON locaux | `fr.json` et `mg.json` avec vocabulaire métier transport malgache |
| **Connexion (Login)** | ✅ Terminé | Hybride (API + fallback mock) | Prêt pour l'API `/api/auth/login/` ; bascule automatique en mock en local |
| **Accueil (Dashboard)** | ✅ Terminé | Store Pinia local | Statut du véhicule, prise/fin de service, bouton XXL versement |
| **Déclaration de Versement (Wizard)** | ✅ Terminé | Dynamique local | **3 étapes conformes CDC [RF-07]** :<br>1. Véhicule/Ligne<br>2. Montant + Écart + Motif<br>3. Récapitulatif |
| **Mode Hors-ligne (Réseau 3G)** | ✅ Terminé | Stockage local téléphone | Sauvegarde automatique dans `offlineQueue` en l'absence de réseau |
| **Profil & Préférences** | ✅ Terminé | Store Pinia + LocalStorage | Changement de langue dynamique, déconnexion avec confirmation |
| **Génération Android (Capacitor)** | ✅ Terminé | Natif Android | Dossier `android/` généré, synchronisé et compilable dans Android Studio |

---

## 3. État du Backend & Base de données (D1)

Le backend possède **déjà toute la structure de la base de données**, mais les « portes d'entrée » (API REST) pour le mobile doivent être ouvertes :

### ✅ Déjà fait en BDD :
- **Tous les modèles Django du CDC** sont écrits dans `backend/core/models/` :
  - `Organisation` (Multi-tenant)
  - `Utilisateur` & `Chauffeur`
  - `Bus` & `Affectation`
  - `Ligne` & `JourneeService`
  - `Versement` & `Dette`
  - `Depense` & `Remboursement`
  - `Incident` & `JournalAudit`
- **Migrations exécutées** dans la base de données.

### ⏳ Reste à faire côté Backend pour brancher le Mobile :
1. **Activer CORS (`django-cors-headers`)** : pour permettre à l'application mobile (sur `localhost:5173` ou sur Android) de contacter le serveur Django (`localhost:8000`).
2. **Créer les Serializers DRF** pour `Versement`, `Bus`, `Chauffeur`.
3. **Créer les Endpoints d'API** :
   - `POST /api/auth/login/` : vérification téléphone/mot de passe en BDD et génération de JWT.
   - `GET /api/chauffeur/mon-bus/` : récupération du bus affecté et du montant attendu du jour.
   - `POST /api/versements/` : enregistrement du versement dans la vraie table BDD avec création automatique de la dette si déficit.

---

## 4. Comment relier le Mobile à la vraie Base de Données (Prochaines étapes)

Dès que vous le souhaitez, nous pourrons passer à l'étape de liaison :

1. **Étape 1 (Backend)** : Ajouter l'endpoint de connexion (`/api/auth/login/`) et de récupération du bus actif dans Django.
2. **Étape 2 (Backend)** : Ajouter l'endpoint de réception des versements (`/api/versements/`).
3. **Étape 3 (Mobile)** : L'application mobile appellera directement ces endpoints (le code d'appel dans [mobile/src/services/api.ts](file:///home/denver/Documents/ERP-de-gestion-de-versement-de-bus/mobile/src/services/api.ts) et [mobile/src/stores/versement.ts](file:///home/denver/Documents/ERP-de-gestion-de-versement-de-bus/mobile/src/stores/versement.ts) est déjà écrit et prêt à recevoir les vraies réponses du serveur).
