import uuid

from django.db import models

from .journee_service import JourneeService
from .ligne import Ligne


class JourneeServiceLigne(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    journee_service = models.ForeignKey(
        JourneeService,
        on_delete=models.CASCADE,
        related_name="lignes_service"
    )

    ligne = models.ForeignKey(
        Ligne,
        on_delete=models.RESTRICT,
        related_name="journees_service"
    )

    heure_debut = models.DateTimeField(
        blank=True,
        null=True
    )

    heure_fin = models.DateTimeField(
        blank=True,
        null=True
    )

    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "journees_service_lignes"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "journee_service",
                    "ligne"
                ],
                name="journee_ligne_unique"
            )
        ]