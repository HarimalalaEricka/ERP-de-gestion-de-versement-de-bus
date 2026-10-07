import uuid

from django.db import models

from .organisation import Organisation


class Conversation(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name="conversations"
    )

    titre = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "conversations"