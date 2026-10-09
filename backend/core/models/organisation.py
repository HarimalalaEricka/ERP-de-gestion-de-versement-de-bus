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

    # Paramètres et seuils métier (CDC v1.0 §12.1)
    seuil_photo_depense = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=20000.00,
        help_text="Seuil en Ariary au-delà duquel la photo du justificatif est obligatoire (défaut : 20 000 Ar)"
    )
    seuil_alerte_versement_pct = models.PositiveIntegerField(
        default=70,
        help_text="Pourcentage de l'attendu sous lequel une alerte est levée (défaut : 70 %)"
    )
    heure_limite_versement = models.TimeField(
        default="19:00:00",
        help_text="Heure limite de versement journalier avant relance automatique (défaut : 19h)"
    )
    delai_relance_accuse_heures = models.PositiveIntegerField(
        default=24,
        help_text="Délai en heures avant relance du propriétaire pour accuser réception (défaut : 24h)"
    )
    seuil_incidents_recurrents = models.PositiveIntegerField(
        default=3,
        help_text="Nombre d'incidents sur 7 jours déclenchant une alerte véhicule anormal (défaut : 3)"
    )
    delai_echeance_dette_jours = models.PositiveIntegerField(
        default=7,
        help_text="Échéance par défaut en jours pour les dettes de versement partiel (défaut : 7 jours)"
    )

    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "organisations"

    def __str__(self):
        return self.nom