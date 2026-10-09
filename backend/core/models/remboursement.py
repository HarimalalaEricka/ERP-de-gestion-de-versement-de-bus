import uuid

from django.db import models

from .organisation import Organisation
from .chauffeur import Chauffeur
from .depense import Depense
from .utilisateur import Utilisateur


class ModeReglementRemboursement(models.TextChoices):
    ESPECES = "ESPECES", "Espèces"
    DEDUCTION_VERSEMENT = "DEDUCTION_VERSEMENT", "Déduction sur prochain versement"


class StatutRemboursement(models.TextChoices):
    A_REMBOURSER = "A_REMBOURSER", "À rembourser"
    REMBOURSE = "REMBOURSE", "Remboursé"
    ANNULE = "ANNULE", "Annulé"


class Remboursement(models.Model):
    """
    Remboursement dû à un chauffeur pour une dépense avancée (CDC RF-16a).
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name="remboursements"
    )

    depense = models.OneToOneField(
        Depense,
        on_delete=models.PROTECT,
        related_name="remboursement"
    )

    chauffeur = models.ForeignKey(
        Chauffeur,
        on_delete=models.PROTECT,
        related_name="remboursements"
    )

    montant = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    mode_reglement = models.CharField(
        max_length=30,
        choices=ModeReglementRemboursement.choices,
        default=ModeReglementRemboursement.ESPECES
    )

    statut = models.CharField(
        max_length=30,
        choices=StatutRemboursement.choices,
        default=StatutRemboursement.A_REMBOURSER
    )

    # Si déduit d'un versement futur
    versement_deduit = models.ForeignKey(
        "Versement",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="remboursements_deduits"
    )

    # Double accusé de remise en espèces (RF-07a appliqué au remboursement)
    accuse_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="remboursements_accuses"
    )

    accuse_le = models.DateTimeField(
        blank=True,
        null=True
    )

    regle_le = models.DateTimeField(
        blank=True,
        null=True
    )

    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "remboursements"

        constraints = [
            models.CheckConstraint(
                condition=models.Q(montant__gt=0),
                name="remboursement_montant_check"
            )
        ]

    def __str__(self):
        return f"Remboursement {self.montant} Ar - {self.chauffeur} ({self.statut})"
