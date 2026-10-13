import uuid

from django.db import models

from .organisation import Organisation
from .utilisateur import Utilisateur


class TypeNotification(models.TextChoices):
    VERSEMENT = "VERSEMENT", "Versement"
    DEPENSE = "DEPENSE", "Dépense"
    INCIDENT = "INCIDENT", "Incident"
    MESSAGE = "MESSAGE", "Message"
    ALERTE = "ALERTE", "Alerte"
    SYSTEME = "SYSTEME", "Système"


class CanalNotification(models.TextChoices):
    PUSH = "PUSH", "Push"
    SMS = "SMS", "SMS"
    EMAIL = "EMAIL", "Email"
    DANS_APPLICATION = (
        "DANS_APPLICATION",
        "Dans l'application"
    )


class Notification(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    type = models.CharField(
        max_length=20,
        choices=TypeNotification.choices
    )

    canal = models.CharField(
        max_length=30,
        choices=CanalNotification.choices
    )

    titre = models.CharField(max_length=200)

    message = models.TextField()

    est_lue = models.BooleanField(default=False)

    envoyee_le = models.DateTimeField(
        blank=True,
        null=True
    )

    lue_le = models.DateTimeField(
        blank=True,
        null=True
    )

    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(type__in=TypeNotification.values),
                name="notification_type_check"
            ),
            models.CheckConstraint(
                condition=models.Q(canal__in=CanalNotification.values),
                name="notification_canal_check"
            ),
        ]