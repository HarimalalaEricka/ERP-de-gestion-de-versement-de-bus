from django.contrib import admin
from .models import (
    Organisation,
    Utilisateur,
    Bus,
    Chauffeur,
    Affectation,
    Ligne,
    RegleVersement,
    JourneeService,
    JourneeServiceLigne,
    Versement,
    Dette,
    Depense,
    Remboursement,
    Incident,
    JournalAudit,
    Notification,
    Document,
)


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ("nom", "telephone", "email", "seuil_photo_depense", "heure_limite_versement", "est_actif")
    search_fields = ("nom", "telephone", "email")


@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ("telephone", "email", "prenom", "nom", "role", "organisation", "statut")
    list_filter = ("role", "statut", "organisation")
    search_fields = ("telephone", "email", "prenom", "nom")


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ("numero_immatriculation", "modele", "statut", "organisation")
    list_filter = ("statut", "organisation")
    search_fields = ("numero_immatriculation", "modele")


@admin.register(Chauffeur)
class ChauffeurAdmin(admin.ModelAdmin):
    list_display = ("numero_chauffeur", "utilisateur", "organisation")
    search_fields = ("numero_chauffeur", "utilisateur__nom", "utilisateur__telephone")


@admin.register(Ligne)
class LigneAdmin(admin.ModelAdmin):
    list_display = ("nom", "couleur", "tarif_reference", "est_active", "organisation")
    list_filter = ("est_active", "organisation")


@admin.register(Affectation)
class AffectationAdmin(admin.ModelAdmin):
    list_display = ("bus", "chauffeur", "date_debut", "date_fin", "statut", "organisation")
    list_filter = ("statut", "organisation")


@admin.register(RegleVersement)
class RegleVersementAdmin(admin.ModelAdmin):
    list_display = ("bus", "ligne", "type_jour", "montant_attendu", "organisation")
    list_filter = ("type_jour", "organisation")


@admin.register(JourneeService)
class JourneeServiceAdmin(admin.ModelAdmin):
    list_display = ("date_service", "bus", "chauffeur", "statut", "organisation")
    list_filter = ("statut", "organisation", "date_service")


@admin.register(Versement)
class VersementAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "journee_service",
        "montant_attendu",
        "montant_verse",
        "ecart",
        "statut",
        "mode_paiement",
        "accuse_par",
        "est_verrouille",
        "cree_le",
    )
    list_filter = ("statut", "mode_paiement", "est_verrouille", "organisation")
    search_fields = ("id", "journee_service__bus__numero_immatriculation")


@admin.register(Dette)
class DetteAdmin(admin.ModelAdmin):
    list_display = ("versement", "chauffeur", "montant_initial", "montant_restant", "statut", "date_echeance")
    list_filter = ("statut", "organisation")


@admin.register(Depense)
class DepenseAdmin(admin.ModelAdmin):
    list_display = ("bus", "chauffeur", "categorie", "montant", "payee_par", "statut", "cree_le")
    list_filter = ("categorie", "payee_par", "statut", "organisation")


@admin.register(Remboursement)
class RemboursementAdmin(admin.ModelAdmin):
    list_display = ("depense", "chauffeur", "montant", "mode_reglement", "statut", "accuse_par")
    list_filter = ("statut", "mode_reglement", "organisation")


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ("bus", "chauffeur", "type", "statut", "retourne_au_garage", "heure_incident")
    list_filter = ("type", "statut", "organisation")


@admin.register(JournalAudit)
class JournalAuditAdmin(admin.ModelAdmin):
    list_display = ("action", "type_entite", "entite_id", "utilisateur", "cree_le")
    list_filter = ("action", "type_entite", "organisation")
    readonly_fields = [f.name for f in JournalAudit._meta.fields]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("titre", "type", "canal", "utilisateur", "est_lue", "cree_le")
    list_filter = ("type", "canal", "est_lue", "organisation")
