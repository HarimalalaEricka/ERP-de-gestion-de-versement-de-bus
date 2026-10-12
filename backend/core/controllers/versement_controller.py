from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from core.serializers.versement_serializer import (
    VersementCreateSerializer,
    VersementSyncSerializer,
)
from core.services.versement_service import (
    enregistrer_versement,
    recuperer_historique_versements,
)

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def versements_view(request):
    if request.method == "POST":
        serializer = VersementCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        resultat = enregistrer_versement(
            utilisateur=request.user,
            data=serializer.validated_data,
        )

        return Response(resultat, status=status.HTTP_201_CREATED)

    resultat = recuperer_historique_versements(request.user)
    return Response(resultat, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def sync_versements_view(request):
    serializer = VersementSyncSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    resultats = []
    for item in serializer.validated_data["versements"]:
        res = enregistrer_versement(
            utilisateur=request.user,
            data=item,
        )
        if "localId" in item:
            res["localId"] = item["localId"]
        resultats.append(res)

    return Response({
        "message": f"{len(resultats)} versement(s) synchronisé(s) avec succès.",
        "synced": resultats
    }, status=status.HTTP_201_CREATED)
