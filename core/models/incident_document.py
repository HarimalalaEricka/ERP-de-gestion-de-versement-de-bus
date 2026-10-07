from django.db import models

from .incident import Incident
from .document import Document


class IncidentDocument(models.Model):
    incident = models.ForeignKey(
        Incident,
        on_delete=models.CASCADE,
        db_column="incident_id",
        related_name="documents"
    )

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        db_column="document_id",
        related_name="incidents"
    )

    pk = models.CompositePrimaryKey(
        "incident_id",
        "document_id"
    )

    class Meta:
        db_table = "incident_documents"

    def __str__(self):
        return f"{self.incident_id} - {self.document_id}"
