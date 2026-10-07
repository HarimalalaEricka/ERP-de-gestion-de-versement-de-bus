import uuid

from django.db import models

from .organisation import Organisation


class StatutBus(models.TextChoices):
    EN_SERVICE = "EN_SERVICE", "En service"
    EN_PANNE = "EN_PANNE", "En panne"
    ARRETE = "ARRETE", "Arrêté"
    ARCHIVE = "ARCHIVE", "Archivé"


class Bus(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name="bus"
    )

    numero_immatriculation = models.CharField(max_length=30)

    modele = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    annee_fabrication = models.IntegerField(
        blank=True,
        null=True
    )

    statut = models.CharField(
        max_length=20,
        choices=StatutBus.choices,
        default=StatutBus.EN_SERVICE
    )

    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bus"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organisation",
                    "numero_immatriculation"
                ],
                name="bus_immatriculation_unique"
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(annee_fabrication__isnull=True)
                    | models.Q(annee_fabrication__gte=1900)
                ),
                name="bus_annee_check"
            )
        ]

    def __str__(self):
        return self.numero_immatriculation