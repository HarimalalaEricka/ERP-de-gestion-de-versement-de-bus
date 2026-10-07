import uuid

from django.db import models

from .organisation import Organisation
from .bus import Bus
from .chauffeur import Chauffeur


class StatutJourneeService(models.TextChoices):
    PLANIFIEE = "PLANIFIEE", "Planifiée"
    EN_COURS = "EN_COURS", "En cours"
    TERMINEE = "TERMINEE", "Terminée"
    ABSENT = "ABSENT", "Absent"
    ANNULEE = "ANNULEE", "Annulée"


class JourneeService(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name="journees_service"
    )

    bus = models.ForeignKey(
        Bus,
        on_delete=models.PROTECT,
        related_name="journees_service"
    )

    chauffeur = models.ForeignKey(
        Chauffeur,
        on_delete=models.PROTECT,
        related_name="journees_service"
    )

    date_service = models.DateField()

    statut = models.CharField(
        max_length=20,
        choices=StatutJourneeService.choices,
        default=StatutJourneeService.PLANIFIEE
    )

    debute_le = models.DateTimeField(
        blank=True,
        null=True
    )

    terminee_le = models.DateTimeField(
        blank=True,
        null=True
    )

    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "journees_service"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "bus",
                    "chauffeur",
                    "date_service"
                ],
                name="journee_service_unique"
            )
        ]