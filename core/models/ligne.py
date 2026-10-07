import uuid

from django.db import models

from .organisation import Organisation


class Ligne(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name="lignes"
    )

    nom = models.CharField(max_length=100)
    couleur = models.CharField(max_length=50)

    tarif_reference = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )

    est_active = models.BooleanField(default=True)

    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "lignes"

        constraints = [
            models.UniqueConstraint(
                fields=["organisation", "nom"],
                name="lignes_nom_unique"
            )
        ]

    def __str__(self):
        return self.nom