INSERT INTO organisations (
    id,
    nom,
    telephone,
    email,
    est_actif,
    seuil_photo_depense,
    seuil_alerte_versement_pct,
    heure_limite_versement,
    delai_relance_accuse_heures,
    seuil_incidents_recurrents,
    delai_echeance_dette_jours,
    cree_le,
    modifie_le
)
VALUES (
    gen_random_uuid(),
    'Organisation A',
    '1234567890',
    'organisationA@example.com',
    TRUE,
    20000.00,
    70,
    '19:00:00',
    24,
    3,
    7,
    NOW(),
    NOW()
);

INSERT INTO chauffeurs( 
    id,
    numero_chauffeur,
    cree_le,
    modifie_le,
    utilisateur_id,
    organisation_id
) VALUES (
    gen_random_uuid(),
    (SELECT telephone FROM utilisateurs WHERE telephone = '0340987654'),
    NOW(),
    NOW(),
    (SELECT id FROM utilisateurs WHERE telephone = '0340987654'),
    (SELECT id FROM organisations WHERE nom = 'Organisation A')
);

INSERT INTO bus(
     id,
     numero_immatriculation,
     modele,
     annee_fabrication,
     statut,
     cree_le,
     modifie_le,
     organisation_id
) VALUES (
    gen_random_uuid(),
    '1234ABCD',
    'Toyota Coaster',
    2020,
    'actif',
    NOW(),
    NOW(),
    (SELECT id FROM organisations WHERE nom = 'Organisation A')
);

INSERT INTO affectations(
    id,
    date_debut,
    date_fin,
    statut,
    cree_le,
    bus_id,
    chauffeur_id,
    organisation_id
) VALUES (
    gen_random_uuid(),
    NOW(),
    NULL,
    'active',
    NOW(),
    (SELECT id FROM bus WHERE numero_immatriculation = '1234ABCD'),
    (SELECT id FROM chauffeurs WHERE numero_chauffeur = (SELECT telephone FROM utilisateurs WHERE telephone = '0340987654')),
    (SELECT id FROM organisations WHERE nom = 'Organisation A')
);

INSERT INTO lignes (
    id,
    nom,
    couleur,
    tarif_reference,
    est_active,
    cree_le,
    modifie_le,
    organisation_id
) VALUES (
    gen_random_uuid(),
    'Ligne 1',
    '#FF5733',
    1000.00,
    TRUE,
    NOW(),
    NOW(),
    (SELECT id FROM organisations WHERE nom = 'Organisation A')
);

INSERT INTO regles_versement(
    id,
    type_jour,
    montant_attendu,
    cree_le,
    bus_id,
    ligne_id,
    organisation_id
) VALUES (
    gen_random_uuid(),
    'SEMAINE',
    100000.00,
    NOW(),
    (SELECT id FROM bus WHERE numero_immatriculation = '1234ABCD'),
    (SELECT id FROM lignes WHERE nom = 'Ligne 1'),
    (SELECT id FROM organisations WHERE nom = 'Organisation A')
);