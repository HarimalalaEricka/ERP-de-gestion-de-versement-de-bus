import uuid

from django.db import models


class Organisation(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    nom = models.CharField(max_length=150)
    telephone = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    email = models.EmailField(
        max_length=150,
        blank=True,
        null=True
    )

    est_actif = models.BooleanField(default=True)

    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "organisations"

    def __str__(self):
        return self.nom