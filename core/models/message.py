import uuid

from django.db import models

from .conversation import Conversation
from .utilisateur import Utilisateur


class Message(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    expediteur = models.ForeignKey(
        Utilisateur,
        on_delete=models.RESTRICT,
        related_name="messages_envoyes"
    )

    contenu = models.TextField(
        blank=True,
        null=True
    )

    cree_le = models.DateTimeField(auto_now_add=True)

    lu_le = models.DateTimeField(
        blank=True,
        null=True
    )

    class Meta:
        db_table = "messages"