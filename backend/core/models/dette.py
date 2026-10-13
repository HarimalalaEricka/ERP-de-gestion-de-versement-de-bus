import uuid

from django.db import models

from .organisation import Organisation
from .versement import Versement
from .chauffeur import Chauffeur


class StatutDette(models.TextChoices):
    EN_ATTENTE = "EN_ATTENTE", "En attente"
    PARTIELLEMENT_PAYEE = (
        "PARTIELLEMENT_PAYEE",
        "Partiellement payée"
    )
    PAYEE = "PAYEE", "Payée"
    ANNULEE = "ANNULEE", "Annulée"


class Dette(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name="dettes"
    )

    chauffeur = models.ForeignKey(
        Chauffeur,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="dettes"
    )

    versement = models.ForeignKey(
        Versement,
        on_delete=models.RESTRICT,
        related_name="dettes"
    )

    montant_initial = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    montant_restant = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    statut = models.CharField(
        max_length=30,
        choices=StatutDette.choices,
        default=StatutDette.EN_ATTENTE
    )

    date_echeance = models.DateField(
        blank=True,
        null=True
    )

    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "dettes"

        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(montant_initial__gte=0)
                    & models.Q(montant_restant__gte=0)
                    & models.Q(
                        montant_restant__lte=models.F(
                            "montant_initial"
                        )
                    )
                ),
                name="dette_montant_check"
            ),
            models.CheckConstraint(
                condition=models.Q(statut__in=StatutDette.values),
                name="dette_statut_check"
            )
        ]