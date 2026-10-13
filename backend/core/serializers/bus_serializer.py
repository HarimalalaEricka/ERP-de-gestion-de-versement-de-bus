from rest_framework import serializers

from core.models import StatutBus


class BusStatutSerializer(serializers.Serializer):
    statut = serializers.ChoiceField(choices=StatutBus.choices)
