import uuid

from django.db import models

from .organisation import Organisation
from .bus import Bus
from .chauffeur import Chauffeur
from .journee_service import JourneeService
from .utilisateur import Utilisateur


class CategorieDepense(models.TextChoices):
    CARBURANT = "CARBURANT", "Carburant"
    REPARATION = "REPARATION", "Réparation"
    PIECES = "PIECES", "Pièces"
    AMENDE = "AMENDE", "Amende"
    LAVAGE = "LAVAGE", "Lavage"
    AUTRE = "AUTRE", "Autre"


class DepensePayeePar(models.TextChoices):
    CHAUFFEUR = "CHAUFFEUR", "Chauffeur"
    PROPRIETAIRE = "PROPRIETAIRE", "Propriétaire"


class StatutDepense(models.TextChoices):
    SOUMISE = "SOUMISE", "Soumise"
    VALIDEE = "VALIDEE", "Validée"
    REJETEE = "REJETEE", "Rejetée"
    ANNULEE = "ANNULEE", "Annulée"


class Depense(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name="depenses"
    )

    bus = models.ForeignKey(
        Bus,
        on_delete=models.PROTECT,
        related_name="depenses"
    )

    chauffeur = models.ForeignKey(
        Chauffeur,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="depenses"
    )

    journee_service = models.ForeignKey(
        JourneeService,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="depenses"
    )

    montant = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    categorie = models.CharField(
        max_length=20,
        choices=CategorieDepense.choices
    )

    description = models.TextField()

    payee_par = models.CharField(
        max_length=20,
        choices=DepensePayeePar.choices
    )

    statut = models.CharField(
        max_length=20,
        choices=StatutDepense.choices,
        default=StatutDepense.SOUMISE
    )

    soumise_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.PROTECT,
        related_name="depenses_soumises"
    )

    validee_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="depenses_validees"
    )

    soumise_le = models.DateTimeField(auto_now_add=True)

    validee_le = models.DateTimeField(
        blank=True,
        null=True
    )

    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "depenses"

        constraints = [
            models.CheckConstraint(
                condition=models.Q(montant__gt=0),
                name="depense_montant_check"
            )
        ]