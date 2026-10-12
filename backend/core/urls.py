from django.urls import path
from core.controllers.auth_controller import login, register
from core.controllers.versement_controller import versements_view, sync_versements_view
from core.controllers.chauffeur_controller import mon_bus_view

urlpatterns = [
    # Authentification
    path("auth/login/", login, name="login"),
    path("auth/register/", register, name="register"),

    # Chauffeur & Véhicule
    path("chauffeur/mon-bus/", mon_bus_view, name="chauffeur-mon-bus"),

    # Versements
    path("versements/", versements_view, name="versements"),
    path("versements/sync/", sync_versements_view, name="versements-sync"),
]