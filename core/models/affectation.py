import uuid

from django.db import models

from .organisation import Organisation
from .bus import Bus
from .chauffeur import Chauffeur


class StatutAffectation(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    TERMINEE = "TERMINEE", "Terminée"


class Affectation(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name="affectations"
    )

    bus = models.ForeignKey(
        Bus,
        on_delete=models.CASCADE,
        related_name="affectations"
    )

    chauffeur = models.ForeignKey(
        Chauffeur,
        on_delete=models.CASCADE,
        related_name="affectations"
    )

    date_debut = models.DateField()
    date_fin = models.DateField(
        blank=True,
        null=True
    )

    statut = models.CharField(
        max_length=20,
        choices=StatutAffectation.choices,
        default=StatutAffectation.ACTIVE
    )

    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "affectations"

        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(date_fin__isnull=True)
                    | models.Q(
                        date_fin__gte=models.F("date_debut")
                    )
                ),
                name="affectation_dates_check"
            )
        ]