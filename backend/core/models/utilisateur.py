
import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models

from .organisation import Organisation


class RoleUtilisateur(models.TextChoices):
    PROPRIETAIRE = "PROPRIETAIRE", "Propriétaire"
    GERANT = "GERANT", "Gérant"
    COMPTABLE = "COMPTABLE", "Comptable"
    CHAUFFEUR = "CHAUFFEUR", "Chauffeur"
    ADMIN = "ADMIN", "Administrateur"


class StatutUtilisateur(models.TextChoices):
    ACTIF = "ACTIF", "Actif"
    INACTIF = "INACTIF", "Inactif"
    SUSPENDU = "SUSPENDU", "Suspendu"


class UtilisateurManager(BaseUserManager):
    """Manager personnalisé pour créer les utilisateurs Django."""

    def create_user(
        self,
        email=None,
        telephone=None,
        password=None,
        **extra_fields
    ):
        if not email and not telephone:
            raise ValueError(
                "L'adresse email ou le numéro de téléphone est obligatoire."
            )

        if email:
            email = self.normalize_email(email)

        organisation = extra_fields.get("organisation")

        if organisation is not None and not isinstance(
            organisation, Organisation
        ):
            try:
                organisation = Organisation.objects.get(pk=organisation)
            except (Organisation.DoesNotExist, ValidationError, ValueError):
                raise ValueError(
                    "L'organisation fournie n'existe pas ou son identifiant "
                    "est invalide."
                )

            extra_fields["organisation"] = organisation

        user = self.model(
            email=email,
            telephone=telephone,
            **extra_fields
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        password=None,
        **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Un superutilisateur doit avoir is_staff=True."
            )

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Un superutilisateur doit avoir is_superuser=True."
            )

        return self.create_user(
            email=email,
            password=password,
            **extra_fields
        )


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    """Utilisateur de l'application, authentifié par email et mot de passe."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name="utilisateurs"
    )

    role = models.CharField(
        max_length=20,
        choices=RoleUtilisateur.choices
    )

    statut = models.CharField(
        max_length=20,
        choices=StatutUtilisateur.choices,
        default=StatutUtilisateur.ACTIF
    )

    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)

    telephone = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        unique=True,
        db_index=True,
        help_text=(
            "Numéro de téléphone principal "
            "(utilisé pour la connexion des chauffeurs)."
        )
    )

    email = models.EmailField(
        max_length=150,
        unique=True,
        blank=True,
        null=True
    )

    derniere_connexion_le = models.DateTimeField(
        blank=True,
        null=True
    )

    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UtilisateurManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "prenom",
        "nom",
        "organisation",
        "role",
    ]

    class Meta:
        db_table = "utilisateurs"
        indexes = [
            models.Index(
                fields=["organisation", "role"],
                name="idx_utilisateur_org_role"
            ),
            models.Index(
                fields=["organisation", "statut"],
                name="idx_utilisateur_org_statut"
            ),
        ]

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.email})"

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"
