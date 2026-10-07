CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TYPE role_utilisateur AS ENUM (
    'PROPRIETAIRE',
    'GERANT',
    'COMPTABLE',
    'CHAUFFEUR',
    'ADMIN'
);

CREATE TYPE statut_utilisateur AS ENUM (
    'ACTIF',
    'INACTIF',
    'SUSPENDU'
);

CREATE TYPE statut_bus AS ENUM (
    'EN_SERVICE',
    'EN_PANNE',
    'ARRETE',
    'ARCHIVE'
);

CREATE TYPE statut_affectation AS ENUM (
    'ACTIVE',
    'TERMINEE'
);

CREATE TYPE statut_journee_service AS ENUM (
    'PLANIFIEE',
    'EN_COURS',
    'TERMINEE',
    'ABSENT',
    'ANNULEE'
);

CREATE TYPE statut_versement AS ENUM (
    'SOUMIS',
    'VALIDE',
    'CONTESTE',
    'ANNULE'
);

CREATE TYPE mode_paiement AS ENUM (
    'ESPECES',
    'MOBILE_MONEY'
);

CREATE TYPE statut_dette AS ENUM (
    'EN_ATTENTE',
    'PARTIELLEMENT_PAYEE',
    'PAYEE',
    'ANNULEE'
);

CREATE TYPE categorie_depense AS ENUM (
    'CARBURANT',
    'REPARATION',
    'PIECES',
    'AMENDE',
    'LAVAGE',
    'AUTRE'
);

CREATE TYPE depense_payee_par AS ENUM (
    'CHAUFFEUR',
    'PROPRIETAIRE'
);

CREATE TYPE statut_depense AS ENUM (
    'SOUMISE',
    'VALIDEE',
    'REJETEE',
    'ANNULEE'
);

CREATE TYPE type_incident AS ENUM (
    'PANNE_MECANIQUE',
    'CREVAISON',
    'ACCIDENT',
    'MALADIE',
    'AUTRE'
);

CREATE TYPE statut_incident AS ENUM (
    'SOUMIS',
    'ACCEPTE',
    'INFORMATIONS_REQUISES',
    'CONTESTE',
    'CLOS'
);

CREATE TYPE type_notification AS ENUM (
    'VERSEMENT',
    'DEPENSE',
    'INCIDENT',
    'MESSAGE',
    'ALERTE',
    'SYSTEME'
);

CREATE TYPE canal_notification AS ENUM (
    'PUSH',
    'SMS',
    'EMAIL',
    'DANS_APPLICATION'
);

CREATE TYPE type_document AS ENUM (
    'RECU',
    'FACTURE',
    'PHOTO',
    'AUDIO',
    'AUTRE'
);

CREATE TABLE organisations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    nom VARCHAR(150) NOT NULL,
    telephone VARCHAR(30),
    email VARCHAR(150),

    est_actif BOOLEAN NOT NULL DEFAULT TRUE,

    cree_le TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


CREATE TABLE utilisateurs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    organisation_id UUID REFERENCES organisations(id)
        ON DELETE CASCADE,

    role role_utilisateur NOT NULL,
    statut statut_utilisateur NOT NULL DEFAULT 'ACTIF',

    prenom VARCHAR(100) NOT NULL,
    nom VARCHAR(100) NOT NULL,

    telephone VARCHAR(30),
    email VARCHAR(150),

    mot_de_passe_hash TEXT,

    derniere_connexion_le TIMESTAMPTZ,

    cree_le TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT utilisateurs_email_unique
        UNIQUE (organisation_id, email)
);

CREATE TABLE bus (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    organisation_id UUID NOT NULL
        REFERENCES organisations(id)
        ON DELETE CASCADE,

    numero_immatriculation VARCHAR(30) NOT NULL,
    modele VARCHAR(100),
    annee_fabrication INTEGER,

    statut statut_bus NOT NULL DEFAULT 'EN_SERVICE',

    cree_le TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT bus_immatriculation_unique
        UNIQUE (organisation_id, numero_immatriculation),

    CONSTRAINT bus_annee_check
        CHECK (
            annee_fabrication IS NULL
            OR annee_fabrication >= 1900
        )
);


CREATE TABLE chauffeurs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    organisation_id UUID NOT NULL
        REFERENCES organisations(id)
        ON DELETE CASCADE,

    utilisateur_id UUID UNIQUE
        REFERENCES utilisateurs(id)
        ON DELETE SET NULL,

    numero_chauffeur VARCHAR(50),

    cree_le TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chauffeurs_numero_unique
        UNIQUE (organisation_id, numero_chauffeur)
);


CREATE TABLE affectations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    organisation_id UUID NOT NULL
        REFERENCES organisations(id)
        ON DELETE CASCADE,

    bus_id UUID NOT NULL
        REFERENCES bus(id)
        ON DELETE CASCADE,

    chauffeur_id UUID NOT NULL
        REFERENCES chauffeurs(id)
        ON DELETE CASCADE,

    date_debut DATE NOT NULL,
    date_fin DATE,

    statut statut_affectation NOT NULL DEFAULT 'ACTIVE',

    cree_le TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT affectation_dates_check
        CHECK (
            date_fin IS NULL
            OR date_fin >= date_debut
        )
);

CREATE TABLE lignes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    organisation_id UUID NOT NULL
        REFERENCES organisations(id)
        ON DELETE CASCADE,

    nom VARCHAR(100) NOT NULL,
    couleur VARCHAR(50) NOT NULL,

    tarif_reference NUMERIC(12,2),

    est_active BOOLEAN NOT NULL DEFAULT TRUE,

    cree_le TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT lignes_nom_unique
        UNIQUE (organisation_id, nom)
);


CREATE TABLE regles_versement (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    organisation_id UUID NOT NULL
        REFERENCES organisations(id)
        ON DELETE CASCADE,

    bus_id UUID
        REFERENCES bus(id)
        ON DELETE CASCADE,

    ligne_id UUID
        REFERENCES lignes(id)
        ON DELETE CASCADE,

    type_jour VARCHAR(20) NOT NULL,

    montant_attendu NUMERIC(12,2) NOT NULL,

    cree_le TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT regles_versement_montant_check
        CHECK (montant_attendu >= 0),

    CONSTRAINT regles_versement_type_jour_check
        CHECK (
            type_jour IN (
                'SEMAINE',
                'WEEKEND',
                'FERIE'
            )
        )
);

CREATE TABLE journees_service (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    organisation_id UUID NOT NULL
        REFERENCES organisations(id)
        ON DELETE CASCADE,

    bus_id UUID NOT NULL
        REFERENCES bus(id)
        ON DELETE RESTRICT,

    chauffeur_id UUID NOT NULL
        REFERENCES chauffeurs(id)
        ON DELETE RESTRICT,

    date_service DATE NOT NULL,

    statut statut_journee_service NOT NULL DEFAULT 'PLANIFIEE',

    debute_le TIMESTAMPTZ,
    terminee_le TIMESTAMPTZ,

    cree_le TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT journee_service_unique
        UNIQUE (bus_id, chauffeur_id, date_service)
);

CREATE TABLE journees_service_lignes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    journee_service_id UUID NOT NULL
        REFERENCES journees_service(id)
        ON DELETE CASCADE,

    ligne_id UUID NOT NULL
        REFERENCES lignes(id)
        ON DELETE RESTRICT,

    heure_debut TIMESTAMPTZ,
    heure_fin TIMESTAMPTZ,

    cree_le TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT journee_ligne_unique
        UNIQUE (journee_service_id, ligne_id)
);


CREATE TABLE versements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    organisation_id UUID NOT NULL
        REFERENCES organisations(id)
        ON DELETE CASCADE,

    journee_service_id UUID NOT NULL
        REFERENCES journees_service(id)
        ON DELETE RESTRICT,

    montant_attendu NUMERIC(12,2) NOT NULL,
    montant_verse NUMERIC(12,2) NOT NULL DEFAULT 0,

    ecart NUMERIC(12,2)
        GENERATED ALWAYS AS
        (montant_verse - montant_attendu) STORED,

    mode_paiement mode_paiement NOT NULL DEFAULT 'ESPECES',

    motif TEXT,
    commentaire TEXT,

    statut statut_versement NOT NULL DEFAULT 'SOUMIS',

    soumis_par UUID NOT NULL
        REFERENCES utilisateurs(id)
        ON DELETE RESTRICT,

    valide_par UUID
        REFERENCES utilisateurs(id)
        ON DELETE SET NULL,

    soumis_le TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    valide_le TIMESTAMPTZ,

    cree_le TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT versement_montant_check
        CHECK (
            montant_attendu >= 0
            AND montant_verse >= 0
        )
);

CREATE TABLE dettes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    organisation_id UUID NOT NULL
        REFERENCES organisations(id)
        ON DELETE CASCADE,

    versement_id UUID NOT NULL
        REFERENCES versements(id)
        ON DELETE RESTRICT,

    montant_initial NUMERIC(12,2) NOT NULL,
    montant_restant NUMERIC(12,2) NOT NULL,

    statut statut_dette NOT NULL DEFAULT 'EN_ATTENTE',

    date_echeance DATE,

    cree_le TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT dette_montant_check
        CHECK (
            montant_initial >= 0
            AND montant_restant >= 0
            AND montant_restant <= montant_initial
        )
);

CREATE TABLE depenses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    organisation_id UUID NOT NULL
        REFERENCES organisations(id)
        ON DELETE CASCADE,

    bus_id UUID NOT NULL
        REFERENCES bus(id)
        ON DELETE RESTRICT,

    chauffeur_id UUID
        REFERENCES chauffeurs(id)
        ON DELETE SET NULL,

    journee_service_id UUID
        REFERENCES journees_service(id)
        ON DELETE SET NULL,

    montant NUMERIC(12,2) NOT NULL,

    categorie categorie_depense NOT NULL,

    description TEXT NOT NULL,

    payee_par depense_payee_par NOT NULL,

    statut statut_depense NOT NULL DEFAULT 'SOUMISE',

    soumise_par UUID NOT NULL
        REFERENCES utilisateurs(id)
        ON DELETE RESTRICT,

    validee_par UUID
        REFERENCES utilisateurs(id)
        ON DELETE SET NULL,

    soumise_le TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    validee_le TIMESTAMPTZ,

    cree_le TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT depense_montant_check
        CHECK (montant > 0)
);


CREATE TABLE incidents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    organisation_id UUID NOT NULL
        REFERENCES organisations(id)
        ON DELETE CASCADE,

    bus_id UUID NOT NULL
        REFERENCES bus(id)
        ON DELETE RESTRICT,

    chauffeur_id UUID
        REFERENCES chauffeurs(id)
        ON DELETE SET NULL,

    journee_service_id UUID
        REFERENCES journees_service(id)
        ON DELETE SET NULL,

    type type_incident NOT NULL,

    description TEXT NOT NULL,

    heure_incident TIMESTAMPTZ NOT NULL,

    retourne_au_garage BOOLEAN NOT NULL DEFAULT FALSE,

    statut statut_incident NOT NULL DEFAULT 'SOUMIS',

    soumis_par UUID NOT NULL
        REFERENCES utilisateurs(id)
        ON DELETE RESTRICT,

    examine_par UUID
        REFERENCES utilisateurs(id)
        ON DELETE SET NULL,

    examine_le TIMESTAMPTZ,

    cree_le TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    organisation_id UUID NOT NULL
        REFERENCES organisations(id)
        ON DELETE CASCADE,

    telecharge_par UUID
        REFERENCES utilisateurs(id)
        ON DELETE SET NULL,

    type_document type_document NOT NULL,

    nom_fichier VARCHAR(255) NOT NULL,
    cle_stockage TEXT NOT NULL,

    type_mime VARCHAR(100),
    taille_fichier BIGINT,

    cree_le TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


CREATE TABLE depense_documents (
    depense_id UUID NOT NULL
        REFERENCES depenses(id)
        ON DELETE CASCADE,

    document_id UUID NOT NULL
        REFERENCES documents(id)
        ON DELETE CASCADE,

    PRIMARY KEY (depense_id, document_id)
);


CREATE TABLE incident_documents (
    incident_id UUID NOT NULL
        REFERENCES incidents(id)
        ON DELETE CASCADE,

    document_id UUID NOT NULL
        REFERENCES documents(id)
        ON DELETE CASCADE,

    PRIMARY KEY (incident_id, document_id)
);


CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    organisation_id UUID NOT NULL
        REFERENCES organisations(id)
        ON DELETE CASCADE,

    titre VARCHAR(200),

    cree_le TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE conversation_participants (
    conversation_id UUID NOT NULL
        REFERENCES conversations(id)
        ON DELETE CASCADE,

    utilisateur_id UUID NOT NULL
        REFERENCES utilisateurs(id)
        ON DELETE CASCADE,

    rejoint_le TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (conversation_id, utilisateur_id)
);

CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    conversation_id UUID NOT NULL
        REFERENCES conversations(id)
        ON DELETE CASCADE,

    expediteur_id UUID NOT NULL
        REFERENCES utilisateurs(id)
        ON DELETE RESTRICT,

    contenu TEXT,

    cree_le TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    lu_le TIMESTAMPTZ
);


CREATE TABLE message_documents (
    message_id UUID NOT NULL
        REFERENCES messages(id)
        ON DELETE CASCADE,

    document_id UUID NOT NULL
        REFERENCES documents(id)
        ON DELETE CASCADE,

    PRIMARY KEY (message_id, document_id)
);


CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    organisation_id UUID NOT NULL
        REFERENCES organisations(id)
        ON DELETE CASCADE,

    utilisateur_id UUID NOT NULL
        REFERENCES utilisateurs(id)
        ON DELETE CASCADE,

    type type_notification NOT NULL,

    canal canal_notification NOT NULL,

    titre VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,

    est_lue BOOLEAN NOT NULL DEFAULT FALSE,

    envoyee_le TIMESTAMPTZ,
    lue_le TIMESTAMPTZ,

    cree_le TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE journaux_audit (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    organisation_id UUID
        REFERENCES organisations(id)
        ON DELETE CASCADE,

    utilisateur_id UUID
        REFERENCES utilisateurs(id)
        ON DELETE SET NULL,

    action VARCHAR(50) NOT NULL,

    type_entite VARCHAR(100) NOT NULL,
    entite_id UUID,

    anciennes_valeurs JSONB,
    nouvelles_valeurs JSONB,

    adresse_ip INET,
    agent_utilisateur TEXT,

    cree_le TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_utilisateurs_organisation
    ON utilisateurs(organisation_id);

CREATE INDEX idx_bus_organisation
    ON bus(organisation_id);

CREATE INDEX idx_chauffeurs_organisation
    ON chauffeurs(organisation_id);

CREATE INDEX idx_affectations_bus
    ON affectations(bus_id);

CREATE INDEX idx_affectations_chauffeur
    ON affectations(chauffeur_id);

CREATE INDEX idx_lignes_organisation
    ON lignes(organisation_id);

CREATE INDEX idx_journees_service_organisation_date
    ON journees_service(organisation_id, date_service);

CREATE INDEX idx_journees_service_bus
    ON journees_service(bus_id);

CREATE INDEX idx_journees_service_chauffeur
    ON journees_service(chauffeur_id);

CREATE INDEX idx_versements_organisation
    ON versements(organisation_id);

CREATE INDEX idx_versements_journee_service
    ON versements(journee_service_id);

CREATE INDEX idx_versements_statut
    ON versements(statut);

CREATE INDEX idx_dettes_organisation_statut
    ON dettes(organisation_id, statut);

CREATE INDEX idx_depenses_organisation_date
    ON depenses(organisation_id, cree_le);

CREATE INDEX idx_depenses_bus
    ON depenses(bus_id);

CREATE INDEX idx_incidents_organisation
    ON incidents(organisation_id);

CREATE INDEX idx_incidents_bus
    ON incidents(bus_id);

CREATE INDEX idx_notifications_utilisateur
    ON notifications(utilisateur_id, est_lue);

CREATE INDEX idx_journaux_audit_organisation_date
    ON journaux_audit(organisation_id, cree_le);

CREATE INDEX idx_journaux_audit_entite
    ON journaux_audit(type_entite, entite_id);

