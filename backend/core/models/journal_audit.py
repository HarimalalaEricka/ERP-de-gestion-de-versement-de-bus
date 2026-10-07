import uuid

from django.db import models

from .organisation import Organisation
from .utilisateur import Utilisateur


class JournalAudit(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="journaux_audit"
    )

    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="actions_audit"
    )

    action = models.CharField(max_length=50)

    type_entite = models.CharField(max_length=100)

    entite_id = models.UUIDField(
        blank=True,
        null=True
    )

    anciennes_valeurs = models.JSONField(
        blank=True,
        null=True
    )

    nouvelles_valeurs = models.JSONField(
        blank=True,
        null=True
    )

    adresse_ip = models.GenericIPAddressField(
        blank=True,
        null=True
    )

    agent_utilisateur = models.TextField(
        blank=True,
        null=True
    )

    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "journaux_audit"