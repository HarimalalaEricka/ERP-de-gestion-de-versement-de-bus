import datetime
from django.db.models import Q, Sum
from core.models import (
    Affectation,
    RegleVersement,
    Dette,
    JourneeService,
    StatutDette,
    StatutJourneeService,
)

JOURS_FERIES = set()

def get_type_jour(jour):
    if jour in JOURS_FERIES:
        return "FERIE"
    if jour.weekday() >= 5:
        return "WEEKEND"
    return "SEMAINE"

def recuperer_mon_bus(utilisateur):
    chauffeur = getattr(utilisateur, "chauffeur", None)
    aujourdhui = datetime.date.today()

    bus_data = None
    total_dettes = 0.0
    journee_data = None

    if chauffeur is not None:
        total_dettes = Dette.objects.filter(
            chauffeur=chauffeur,
            statut__in=[StatutDette.EN_ATTENTE, StatutDette.PARTIELLEMENT_PAYEE]
        ).aggregate(total=Sum("montant_restant"))["total"] or 0

        journee = JourneeService.objects.filter(
            chauffeur=chauffeur,
            date_service=aujourdhui
        ).first()

        if journee:
            journee_data = {
                "id": str(journee.id),
                "date_service": journee.date_service.isoformat(),
                "statut": journee.statut,
                "debute_le": journee.debute_le.isoformat() if journee.debute_le else None,
                "terminee_le": journee.terminee_le.isoformat() if journee.terminee_le else None,
            }

        affectation = (
            Affectation.objects
            .filter(chauffeur=chauffeur, date_debut__lte=aujourdhui)
            .filter(Q(date_fin__isnull=True) | Q(date_fin__gte=aujourdhui))
            .select_related("bus")
            .order_by("-date_debut")
            .first()
        )

        if affectation is not None:
            bus = affectation.bus
            regles_bus = list(
                RegleVersement.objects
                .filter(bus=bus)
                .select_related("ligne")
            )
            ligne = next((r.ligne for r in regles_bus if r.ligne is not None), None)

            montants = {r.type_jour: r.montant_attendu for r in regles_bus}
            if ligne is not None:
                regles_ligne = RegleVersement.objects.filter(ligne=ligne, bus__isnull=True)
                for r in regles_ligne:
                    montants.setdefault(r.type_jour, r.montant_attendu)

            type_jour = get_type_jour(aujourdhui)
            montant_du_jour = montants.get(type_jour, 120000.0)

            bus_data = {
                "id": str(bus.id),
                "organisation_id": str(bus.organisation_id),
                "numero_immatriculation": bus.numero_immatriculation,
                "immatriculation": bus.numero_immatriculation,
                "modele": bus.modele,
                "marqueModele": bus.modele,
                "statut": bus.statut,
                "ligneNom": ligne.nom if ligne else "Ligne par défaut",
                "montantAttenduJour": float(montant_du_jour),
            }

    return {
        "chauffeur": {
            "id": str(chauffeur.id) if chauffeur else None,
            "nom_complet": utilisateur.nom_complet,
            "telephone": utilisateur.telephone,
            "organisation": utilisateur.organisation.nom if utilisateur.organisation else "",
        },
        "bus": bus_data,
        "total_dettes": float(total_dettes),
        "journee_service": journee_data,
    }
