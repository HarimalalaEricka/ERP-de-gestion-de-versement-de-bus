from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from core.serializers.bus_serializer import BusStatutSerializer
from core.services.bus_service import recuperer_mon_bus
from core.services.bus_service import modifier_statut_mon_bus


@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def mon_bus_view(request):
    if request.method == "PATCH":
        serializer = BusStatutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bus = modifier_statut_mon_bus(
            utilisateur=request.user,
            statut=serializer.validated_data["statut"],
        )
        return Response(bus, status=status.HTTP_200_OK)

    donnees = recuperer_mon_bus(request.user)
    return Response(donnees, status=status.HTTP_200_OK)
