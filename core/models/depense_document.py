from django.db import models

from .depense import Depense
from .document import Document


class DepenseDocument(models.Model):
    depense = models.ForeignKey(
        Depense,
        on_delete=models.CASCADE,
        db_column="depense_id",
        related_name="documents"
    )

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        db_column="document_id",
        related_name="depenses"
    )

    pk = models.CompositePrimaryKey(
        "depense_id",
        "document_id"
    )

    class Meta:
        db_table = "depense_documents"

    def __str__(self):
        return f"{self.depense_id} - {self.document_id}"