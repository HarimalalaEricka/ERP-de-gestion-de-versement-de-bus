import uuid

from django.db import models

from .organisation import Organisation
from .utilisateur import Utilisateur


class TypeDocument(models.TextChoices):
    RECU = "RECU", "Reçu"
    FACTURE = "FACTURE", "Facture"
    PHOTO = "PHOTO", "Photo"
    AUDIO = "AUDIO", "Audio"
    AUTRE = "AUTRE", "Autre"


class Document(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    telecharge_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="documents_telecharges"
    )

    type_document = models.CharField(
        max_length=20,
        choices=TypeDocument.choices
    )

    nom_fichier = models.CharField(max_length=255)

    cle_stockage = models.TextField()

    type_mime = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    taille_fichier = models.BigIntegerField(
        blank=True,
        null=True
    )

    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "documents"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    type_document__in=TypeDocument.values
                ),
                name="document_type_check"
            ),
        ]