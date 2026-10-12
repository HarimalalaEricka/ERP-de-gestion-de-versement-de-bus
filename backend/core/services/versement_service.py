import datetime
from django.db import transaction
from django.db.models import Sum
from rest_framework.exceptions import ValidationError, NotFound

from core.models import (
    Versement,
    Dette,
    JourneeService,
    Bus,
    StatutVersement,
    StatutDette,
    StatutJourneeService,
    ModePaiement,
    MotifEcart,
    JournalAudit,
)

MOTIF_MAP = {
    "traffic": MotifEcart.EMBOUTEILLAGE,
    "EMBOUTEILLAGE": MotifEcart.EMBOUTEILLAGE,
    "breakdown": MotifEcart.PANNE,
    "PANNE": MotifEcart.PANNE,
    "low_passengers": MotifEcart.PEU_DE_PASSAGERS,
    "PEU_DE_PASSAGERS": MotifEcart.PEU_DE_PASSAGERS,
    "weather": MotifEcart.AUTRE,
    "police": MotifEcart.AUTRE,
    "accident": MotifEcart.ACCIDENT,
    "ACCIDENT": MotifEcart.ACCIDENT,
    "greve": MotifEcart.GREVE,
    "GREVE": MotifEcart.GREVE,
    "route_barree": MotifEcart.ROUTE_BARREE,
    "ROUTE_BARREE": MotifEcart.ROUTE_BARREE,
    "other": MotifEcart.AUTRE,
    "AUTRE": MotifEcart.AUTRE,
}

@transaction.atomic
def enregistrer_versement(utilisateur, data):
    chauffeur = getattr(utilisateur, "chauffeur", None)
    if chauffeur is None:
        raise ValidationError({"detail": "Cet utilisateur n'a pas de profil chauffeur rattaché."})

    bus_id = data.get("bus") or data.get("busId")
    bus = Bus.objects.filter(id=bus_id, organisation=utilisateur.organisation).first()
    if bus is None:
        raise NotFound({"detail": "Le bus spécifié n'existe pas dans cette organisation."})

    date_service = data.get("date_versement") or data.get("dateVersement") or datetime.date.today()

    journee, _ = JourneeService.objects.get_or_create(
        organisation=utilisateur.organisation,
        bus=bus,
        chauffeur=chauffeur,
        date_service=date_service,
        defaults={"statut": StatutJourneeService.EN_COURS}
    )

    motif_brut = data.get("motif_ecart") or data.get("motifEcart")
    motif = MOTIF_MAP.get(motif_brut, MotifEcart.AUTRE if motif_brut else None)

    montant_attendu = data.get("montant_attendu") or data.get("montantAttendu")
    montant_verse = data.get("montant_verse") or data.get("montantVerse")
    commentaire = data.get("commentaire", "")
    mode_paiement = data.get("mode_paiement", ModePaiement.ESPECES)

    versement = Versement.objects.create(
        organisation=utilisateur.organisation,
        journee_service=journee,
        montant_attendu=montant_attendu,
        montant_verse=montant_verse,
        motif=motif,
        commentaire=commentaire,
        mode_paiement=mode_paiement,
        statut=StatutVersement.SOUMIS,
        soumis_par=utilisateur,
    )

    ecart = float(montant_verse) - float(montant_attendu)
    dette_creee = None

    if ecart < 0:
        montant_dette = abs(ecart)
        delai = utilisateur.organisation.delai_echeance_dette_jours or 7
        date_echeance = date_service + datetime.timedelta(days=delai)
        dette_creee = Dette.objects.create(
            organisation=utilisateur.organisation,
            chauffeur=chauffeur,
            versement=versement,
            montant_initial=montant_dette,
            montant_restant=montant_dette,
            statut=StatutDette.EN_ATTENTE,
            date_echeance=date_echeance
        )

    JournalAudit.objects.create(
        organisation=utilisateur.organisation,
        utilisateur=utilisateur,
        action="SOUMISSION_VERSEMENT",
        type_entite="Versement",
        entite_id=versement.id,
        nouvelles_valeurs={
            "montant_verse": str(montant_verse),
            "montant_attendu": str(montant_attendu),
            "ecart": str(ecart),
            "dette_id": str(dette_creee.id) if dette_creee else None
        }
    )

    return {
        "id": str(versement.id),
        "journee_service_id": str(journee.id),
        "bus_immatriculation": bus.numero_immatriculation,
        "montant_attendu": float(versement.montant_attendu),
        "montant_verse": float(versement.montant_verse),
        "ecart": float(ecart),
        "motif": versement.motif,
        "commentaire": versement.commentaire,
        "statut": versement.statut,
        "dette": {
            "id": str(dette_creee.id),
            "montant": float(dette_creee.montant_initial),
            "date_echeance": dette_creee.date_echeance.isoformat()
        } if dette_creee else None,
        "cree_le": versement.cree_le.isoformat()
    }


def recuperer_historique_versements(utilisateur):
    chauffeur = getattr(utilisateur, "chauffeur", None)
    if chauffeur is None:
        qs = Versement.objects.filter(organisation=utilisateur.organisation)
        total_dettes = Dette.objects.filter(
            organisation=utilisateur.organisation,
            statut__in=[StatutDette.EN_ATTENTE, StatutDette.PARTIELLEMENT_PAYEE]
        ).aggregate(total=Sum("montant_restant"))["total"] or 0
    else:
        qs = Versement.objects.filter(
            journee_service__chauffeur=chauffeur
        )
        total_dettes = Dette.objects.filter(
            chauffeur=chauffeur,
            statut__in=[StatutDette.EN_ATTENTE, StatutDette.PARTIELLEMENT_PAYEE]
        ).aggregate(total=Sum("montant_restant"))["total"] or 0

    versements = qs.select_related("journee_service__bus").order_by("-cree_le")[:50]

    liste = []
    for v in versements:
        liste.append({
            "id": str(v.id),
            "date": v.journee_service.date_service.isoformat(),
            "bus_immatriculation": v.journee_service.bus.numero_immatriculation,
            "montant_attendu": float(v.montant_attendu),
            "montant_verse": float(v.montant_verse),
            "ecart": float(v.ecart) if v.ecart is not None else float(v.montant_verse - v.montant_attendu),
            "motif": v.motif,
            "statut": v.statut,
            "mode_paiement": v.mode_paiement,
            "cree_le": v.cree_le.isoformat()
        })

    return {
        "total_dettes": float(total_dettes),
        "nombre_versements": len(liste),
        "versements": liste
    }
