from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from core.services.bus_service import recuperer_mon_bus

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def mon_bus_view(request):
    donnees = recuperer_mon_bus(request.user)
    return Response(donnees, status=status.HTTP_200_OK)
