import uuid

from django.db import models

from .organisation import Organisation
from .journee_service import JourneeService
from .utilisateur import Utilisateur


class StatutVersement(models.TextChoices):
    DECLARE = "DECLARE", "Déclaré"
    RECU = "RECU", "Reçu (Accusé)"
    VALIDE = "VALIDE", "Validé"
    CONTESTE = "CONTESTE", "Contesté"
    SOUMIS = "SOUMIS", "Soumis"
    ANNULE = "ANNULE", "Annulé"


class MotifEcart(models.TextChoices):
    PANNE = "PANNE", "Panne"
    EMBOUTEILLAGE = "EMBOUTEILLAGE", "Embouteillage"
    ROUTE_BARREE = "ROUTE_BARREE", "Route barrée"
    PEU_DE_PASSAGERS = "PEU_DE_PASSAGERS", "Peu de passagers"
    GREVE = "GREVE", "Grève"
    ACCIDENT = "ACCIDENT", "Accident"
    AUTRE = "AUTRE", "Autre"


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

    motif = models.CharField(
        max_length=30,
        choices=MotifEcart.choices,
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
        default=StatutVersement.DECLARE
    )

    # Chauffeur ayant déclaré le versement
    soumis_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.PROTECT,
        related_name="versements_soumis"
    )

    # Propriétaire ou gérant ayant accusé réception physique des espèces (RF-07a)
    accuse_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="versements_accuses"
    )

    # Validation définitive (RF-10)
    valide_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="versements_valides"
    )

    soumis_le = models.DateTimeField(auto_now_add=True)

    accuse_le = models.DateTimeField(
        blank=True,
        null=True
    )

    valide_le = models.DateTimeField(
        blank=True,
        null=True
    )

    # Verrouillage & écritures rectificatives (RF-12)
    est_verrouille = models.BooleanField(
        default=False,
        help_text="Verrouillé une fois validé. Modification interdite hors écriture rectificative."
    )

    versement_original = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="rectifications",
        help_text="Lien vers le versement d'origine si ceci est une écriture rectificative."
    )

    est_rectificatif = models.BooleanField(
        default=False
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