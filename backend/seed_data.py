import os
import sys
import datetime
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from core.models import (
    Organisation,
    Utilisateur,
    Chauffeur,
    Bus,
    Ligne,
    Affectation,
    RegleVersement,
    RoleUtilisateur,
    StatutUtilisateur,
    StatutBus,
    StatutAffectation,
)

def seed():
    print("Initialisation des données de test...")

    org, _ = Organisation.objects.get_or_create(
        nom="Organisation A",
        defaults={
            "telephone": "0340000001",
            "email": "org.a@example.com",
            "est_actif": True,
        },
    )

    chauffeur_user, _ = Utilisateur.objects.get_or_create(
        telephone="0340987654",
        defaults={
            "organisation": org,
            "prenom": "Jean",
            "nom": "Rakotondrabe",
            "email": "jean.rakotondrabe@example.com",
            "role": RoleUtilisateur.CHAUFFEUR,
            "statut": StatutUtilisateur.ACTIF,
            "is_active": True,
        },
    )
    chauffeur_user.set_password("password")
    chauffeur_user.save()

    chauffeur, _ = Chauffeur.objects.get_or_create(
        organisation=org,
        utilisateur=chauffeur_user,
        defaults={"numero_chauffeur": "0340987654"},
    )

    bus, _ = Bus.objects.get_or_create(
        organisation=org,
        numero_immatriculation="1234 TAB",
        defaults={
            "modele": "Mercedes Sprinter",
            "annee_fabrication": 2020,
            "statut": StatutBus.EN_SERVICE,
        },
    )

    ligne, _ = Ligne.objects.get_or_create(
        organisation=org,
        nom="Ligne 133 (Ankatso - Analakely)",
        defaults={
            "couleur": "#3880ff",
            "tarif_reference": 1000.00,
            "est_active": True,
        },
    )

    affectation, _ = Affectation.objects.get_or_create(
        organisation=org,
        bus=bus,
        chauffeur=chauffeur,
        statut=StatutAffectation.ACTIVE,
        defaults={
            "date_debut": datetime.date.today(),
        },
    )

    for type_jour in ["SEMAINE", "WEEKEND", "FERIE"]:
        RegleVersement.objects.get_or_create(
            organisation=org,
            bus=bus,
            ligne=ligne,
            type_jour=type_jour,
            defaults={"montant_attendu": 120000.00},
        )

    admin, _ = Utilisateur.objects.get_or_create(
        email="admin@example.com",
        defaults={
            "organisation": org,
            "prenom": "Admin",
            "nom": "System",
            "telephone": "0340000000",
            "role": RoleUtilisateur.ADMIN,
            "statut": StatutUtilisateur.ACTIF,
            "is_active": True,
            "is_staff": True,
            "is_superuser": True,
        },
    )
    admin.set_password("admin123")
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()

    print("Données créées avec succès !")
    print("Chauffeur : Téléphone: 0340987654 | Mot de passe: password")
    print("Admin     : Email: admin@example.com | Mot de passe: admin123")

if __name__ == "__main__":
    seed()
