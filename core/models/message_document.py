from django.db import models

from .message import Message
from .document import Document


class MessageDocument(models.Model):
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        db_column="message_id",
        related_name="documents"
    )

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        db_column="document_id",
        related_name="messages"
    )

    pk = models.CompositePrimaryKey(
        "message_id",
        "document_id"
    )

    class Meta:
        db_table = "message_documents"

    def __str__(self):
        return f"{self.message_id} - {self.document_id}"
