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