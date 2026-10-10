from rest_framework import serializers
from core.models import Utilisateur, RoleUtilisateur, StatutUtilisateur

class LoginSerializer(serializers.Serializer):
    telephone = serializers.CharField(max_length=30)
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )


class RegisterSerializer(serializers.Serializer):
    organisation_id = serializers.UUIDField()
    prenom = serializers.CharField(max_length=100)
    nom = serializers.CharField(max_length=100)
    telephone = serializers.CharField(max_length=30)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        trim_whitespace=False,
    )
    role = serializers.ChoiceField(choices=RoleUtilisateur.choices)

    def validate_telephone(self, value):
        telephone = value.strip()

        if Utilisateur.objects.filter(telephone=telephone).exists():
            raise serializers.ValidationError(
                "Ce numéro de téléphone est déjà utilisé."
            )

        return telephone

    def validate_email(self, value):
        email = value.strip() or None

        if email and Utilisateur.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Cette adresse email est déjà utilisée."
            )

        return email
