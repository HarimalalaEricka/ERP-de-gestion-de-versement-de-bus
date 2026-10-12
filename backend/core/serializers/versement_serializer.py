import datetime
from rest_framework import serializers
from core.models import Versement, ModePaiement, MotifEcart

class VersementCreateSerializer(serializers.Serializer):
    bus = serializers.UUIDField()
    montant_verse = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    montant_attendu = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    motif_ecart = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    commentaire = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    date_versement = serializers.DateField(required=False, default=datetime.date.today)
    mode_paiement = serializers.ChoiceField(
        choices=ModePaiement.choices,
        default=ModePaiement.ESPECES
    )

class VersementSyncItemSerializer(serializers.Serializer):
    busId = serializers.UUIDField()
    montantVerse = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    montantAttendu = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    motifEcart = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    commentaire = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    dateVersement = serializers.DateField(required=False, default=datetime.date.today)
    localId = serializers.CharField(required=False)

class VersementSyncSerializer(serializers.Serializer):
    versements = serializers.ListField(
        child=VersementSyncItemSerializer()
    )
