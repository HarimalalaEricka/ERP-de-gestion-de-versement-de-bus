import uuid

from django.db import models

from .organisation import Organisation
from .bus import Bus
from .chauffeur import Chauffeur
from .journee_service import JourneeService
from .utilisateur import Utilisateur


class TypeIncident(models.TextChoices):
    PANNE_MECANIQUE = "PANNE_MECANIQUE", "Panne mécanique"
    CREVAISON = "CREVAISON", "Crevaison"
    ACCIDENT = "ACCIDENT", "Accident"
    MALADIE = "MALADIE", "Maladie"
    AUTRE = "AUTRE", "Autre"


class StatutIncident(models.TextChoices):
    SOUMIS = "SOUMIS", "Soumis"
    ACCEPTE = "ACCEPTE", "Accepté"
    INFORMATIONS_REQUISES = (
        "INFORMATIONS_REQUISES",
        "Informations requises"
    )
    CONTESTE = "CONTESTE", "Contesté"
    CLOS = "CLOS", "Clos"


class Incident(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name="incidents"
    )

    bus = models.ForeignKey(
        Bus,
        on_delete=models.PROTECT,
        related_name="incidents"
    )

    chauffeur = models.ForeignKey(
        Chauffeur,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="incidents"
    )

    journee_service = models.ForeignKey(
        JourneeService,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="incidents"
    )

    type = models.CharField(
        max_length=30,
        choices=TypeIncident.choices
    )

    description = models.TextField()

    heure_incident = models.DateTimeField()

    retourne_au_garage = models.BooleanField(default=False)

    statut = models.CharField(
        max_length=30,
        choices=StatutIncident.choices,
        default=StatutIncident.SOUMIS
    )

    soumis_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.PROTECT,
        related_name="incidents_soumis"
    )

    examine_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="incidents_examines"
    )

    examine_le = models.DateTimeField(
        blank=True,
        null=True
    )

    reponse_proprietaire = models.TextField(
        blank=True,
        null=True,
        help_text="Précisions demandées ou motif de contestation par le propriétaire (RF-20)."
    )

    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "incidents"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(type__in=TypeIncident.values),
                name="incident_type_check"
            ),
            models.CheckConstraint(
                condition=models.Q(statut__in=StatutIncident.values),
                name="incident_statut_check"
            ),
        ]