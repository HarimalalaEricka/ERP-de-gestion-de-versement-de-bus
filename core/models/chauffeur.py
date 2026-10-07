import uuid

from django.db import models

from .organisation import Organisation
from .utilisateur import Utilisateur


class Chauffeur(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name="chauffeurs"
    )

    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="chauffeur"
    )

    numero_chauffeur = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "chauffeurs"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organisation",
                    "numero_chauffeur"
                ],
                name="chauffeurs_numero_unique"
            )
        ]

    def __str__(self):
        return self.numero_chauffeur or str(self.id)