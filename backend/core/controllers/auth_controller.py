from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from core.serializers.auth_serializer import LoginSerializer
from core.services.auth_service import connecter_utilisateur
from core.serializers.auth_serializer import RegisterSerializer
from core.services.auth_service import inscrire_utilisateur


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    resultat = connecter_utilisateur(
        telephone=serializer.validated_data["telephone"],
        password=serializer.validated_data["password"],
    )

    return Response(resultat)


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    utilisateur = inscrire_utilisateur(serializer.validated_data)

    return Response(
        {
            "message": "Utilisateur créé avec succès.",
            "user": utilisateur,
        },
        status=status.HTTP_201_CREATED,
    )
