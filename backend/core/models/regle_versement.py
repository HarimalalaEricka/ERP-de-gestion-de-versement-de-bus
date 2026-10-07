import uuid

from django.db import models

from .organisation import Organisation
from .bus import Bus
from .ligne import Ligne


class RegleVersement(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name="regles_versement"
    )

    bus = models.ForeignKey(
        Bus,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="regles_versement"
    )

    ligne = models.ForeignKey(
        Ligne,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="regles_versement"
    )

    type_jour = models.CharField(max_length=20)

    montant_attendu = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "regles_versement"

        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    montant_attendu__gte=0
                ),
                name="regles_versement_montant_check"
            ),
            models.CheckConstraint(
                condition=models.Q(
                    type_jour__in=[
                        "SEMAINE",
                        "WEEKEND",
                        "FERIE"
                    ]
                ),
                name="regles_versement_type_jour_check"
            )
        ]