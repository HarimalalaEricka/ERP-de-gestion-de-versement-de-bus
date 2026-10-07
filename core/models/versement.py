import uuid

from django.db import models

from .organisation import Organisation
from .journee_service import JourneeService
from .utilisateur import Utilisateur


class StatutVersement(models.TextChoices):
    SOUMIS = "SOUMIS", "Soumis"
    VALIDE = "VALIDE", "Validé"
    CONTESTE = "CONTESTE", "Contesté"
    ANNULE = "ANNULE", "Annulé"


class ModePaiement(models.TextChoices):
    ESPECES = "ESPECES", "Espèces"
    MOBILE_MONEY = "MOBILE_MONEY", "Mobile Money"


class Versement(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name="versements"
    )

    journee_service = models.ForeignKey(
        JourneeService,
        on_delete=models.PROTECT,
        related_name="versements"
    )

    montant_attendu = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    montant_verse = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    ecart = models.GeneratedField(
        expression=models.F("montant_verse")
        - models.F("montant_attendu"),
        output_field=models.DecimalField(
            max_digits=12,
            decimal_places=2
        ),
        db_persist=True
    )

    mode_paiement = models.CharField(
        max_length=20,
        choices=ModePaiement.choices,
        default=ModePaiement.ESPECES
    )

    motif = models.TextField(
        blank=True,
        null=True
    )

    commentaire = models.TextField(
        blank=True,
        null=True
    )

    statut = models.CharField(
        max_length=20,
        choices=StatutVersement.choices,
        default=StatutVersement.SOUMIS
    )

    soumis_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.PROTECT,
        related_name="versements_soumis"
    )

    valide_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="versements_valides"
    )

    soumis_le = models.DateTimeField(auto_now_add=True)

    valide_le = models.DateTimeField(
        blank=True,
        null=True
    )

    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "versements"

        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(montant_attendu__gte=0)
                    & models.Q(montant_verse__gte=0)
                ),
                name="versement_montant_check"
            )
        ]