
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date 
from django.db.models import Q
from core.models import Utilisateur, StatutUtilisateur, Organisation, Affectation, StatutAffectation, RegleVersement
from core.services.organisation_service import get_by_id

JOURS_FERIES = set()  

def get_type_jour(jour):
    if jour in JOURS_FERIES:
        return "FERIE"
    if jour.weekday() >= 5:
        return "WEEKEND"
    return "SEMAINE"

def connecter_utilisateur(telephone, password):
    utilisateur = Utilisateur.objects.filter(
        telephone=telephone.strip()
    ).first()

    if utilisateur is None or not utilisateur.check_password(password):
        raise AuthenticationFailed(
            "Numéro de téléphone ou mot de passe incorrect."
        )

    if (
        not utilisateur.is_active
        or utilisateur.statut != StatutUtilisateur.ACTIF
    ):
        raise AuthenticationFailed(
            "Ce compte est inactif ou suspendu."
        )

    organisation = get_by_id(utilisateur.organisation_id)
    refresh = RefreshToken.for_user(utilisateur)

    utilisateur.derniere_connexion_le = timezone.now()
    utilisateur.save(update_fields=["derniere_connexion_le"])

        # Rechercher le chauffeur associé au compte utilisateur
    chauffeur = getattr(utilisateur, "chauffeur", None)
    aujourdhui = date.today()

    bus_data = None
    ligne_data = None

    if chauffeur is not None:
        affectation = (
            Affectation.objects
            .filter(chauffeur=chauffeur, date_debut__lte=aujourdhui)
            .filter(Q(date_fin__isnull=True) | Q(date_fin__gte=aujourdhui))
            .select_related("bus")
            .order_by("-date_debut")
            .first()
        )

        if affectation is not None:
            bus = affectation.bus

            bus_data = {
                "id": str(bus.id),
                "organisation_id": str(bus.organisation_id),
                "immatriculation": bus.numero_immatriculation,
                "modele": bus.modele,
                "marqueModele": bus.modele,
                "annee_fabrication": bus.annee_fabrication,
                "statut": bus.statut,
                "cree_le": bus.cree_le.isoformat() if bus.cree_le else None,
                "modifie_le": bus.modifie_le.isoformat() if bus.modifie_le else None,
            }

            # Règles propres au bus (la ligne vient d'ici)
            regles_bus = list(
                RegleVersement.objects
                .filter(bus=bus)
                .select_related("ligne")
            )

            # La ligne du bus = la ligne de ses règles
            ligne = next((r.ligne for r in regles_bus if r.ligne is not None), None)

            # Montants par type_jour : règle du bus d'abord,
            # puis règle générale de la ligne (bus nul) en repli
            montants = {r.type_jour: r.montant_attendu for r in regles_bus}

            if ligne is not None:
                regles_ligne = RegleVersement.objects.filter(
                    ligne=ligne, bus__isnull=True
                )
                for r in regles_ligne:
                    montants.setdefault(r.type_jour, r.montant_attendu)

            type_jour = get_type_jour(aujourdhui)
            montant_du_jour = montants.get(type_jour)

            if ligne is not None:
                ligne_data = {
                    "id": str(ligne.id),
                    "nom": ligne.nom,
                    "couleur": ligne.couleur,
                    "tarif_reference": (
                        str(ligne.tarif_reference)
                        if ligne.tarif_reference is not None else None
                    ),
                    "type_jour": type_jour,
                    "montant_attendu": (
                        str(montant_du_jour) if montant_du_jour is not None else None
                    ),
                    "montants_par_type_jour": {
                        k: str(v) for k, v in montants.items()
                    },
                }
                bus_data["ligne"] = ligne_data
                bus_data["ligneNom"] = ligne.nom
                bus_data["montantAttenduJour"] = float(montant_du_jour) if montant_du_jour is not None else 120000.0

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": {
            "id": str(utilisateur.id),
            "telephone": utilisateur.telephone,
            "prenom": utilisateur.prenom,
            "nom": utilisateur.nom,
            "nom_complet": utilisateur.nom_complet,
            "role": utilisateur.role,
            "statut": utilisateur.statut,
            "organisation_id": str(utilisateur.organisation_id),
            "organisationNom": organisation.nom if organisation else None,
            "organisation": (
                {
                    "id": str(organisation.id),
                    "nom": organisation.nom,
                    "telephone": organisation.telephone,
                    "email": organisation.email,
                    "est_actif": organisation.est_actif,
                }
                if organisation else None
            ),
        },
        "bus": bus_data,
    }


@transaction.atomic
def inscrire_utilisateur(donnees):
    organisation = Organisation.objects.filter(
        id=donnees["organisation_id"]
    ).first()

    if organisation is None:
        raise ValidationError({
            "organisation_id": "Cette organisation n'existe pas."
        })

    utilisateur = Utilisateur(
        organisation=organisation,
        prenom=donnees["prenom"],
        nom=donnees["nom"],
        telephone=donnees["telephone"],
        email=donnees.get("email"),
        role=donnees["role"],
        statut=StatutUtilisateur.ACTIF,
    )

    utilisateur.set_password(donnees["password"])
    utilisateur.save()

    return {
        "id": str(utilisateur.id),
        "prenom": utilisateur.prenom,
        "nom": utilisateur.nom,
        "telephone": utilisateur.telephone,
        "email": utilisateur.email,
        "role": utilisateur.role,
        "statut": utilisateur.statut,
        "organisation_id": str(utilisateur.organisation_id),
    }
