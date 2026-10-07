from django.db import models

from .conversation import Conversation
from .utilisateur import Utilisateur


class ConversationParticipant(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        db_column="conversation_id",
        related_name="participants"
    )

    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        db_column="utilisateur_id",
        related_name="conversations"
    )

    rejoint_le = models.DateTimeField(
        auto_now_add=True
    )

    pk = models.CompositePrimaryKey(
        "conversation_id",
        "utilisateur_id"
    )

    class Meta:
        db_table = "conversation_participants"

    def __str__(self):
        return f"{self.conversation_id} - {self.utilisateur_id}"
