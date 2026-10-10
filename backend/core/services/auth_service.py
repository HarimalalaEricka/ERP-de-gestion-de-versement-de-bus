
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import Utilisateur, StatutUtilisateur, Organisation


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

    refresh = RefreshToken.for_user(utilisateur)

    utilisateur.derniere_connexion_le = timezone.now()
    utilisateur.save(update_fields=["derniere_connexion_le"])

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
        },
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
