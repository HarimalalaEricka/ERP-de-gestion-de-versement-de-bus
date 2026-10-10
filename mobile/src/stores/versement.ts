import { defineStore } from 'pinia';
import apiClient from '../services/api';

export interface VersementDraft {
  busId: string;
  immatriculation: string;
  ligneNom: string;
  montantAttendu: number;
  montantVerse: number;
  ecart: number;
  motifEcart: string;
  commentaire: string;
  dateVersement: string;
}

export interface OfflineVersement extends VersementDraft {
  localId: string;
  dateCreation: string;
  statut: 'EN_ATTENTE_SYNC' | 'SYNCHRONISE';
}

export const useVersementStore = defineStore('versement', {
  state: () => ({
    currentStep: 1,
    draft: {
      busId: '',
      immatriculation: '',
      ligneNom: '',
      montantAttendu: 120000,
      montantVerse: 0,
      ecart: 0,
      motifEcart: '',
      commentaire: '',
      dateVersement: new Date().toISOString().split('T')[0]
    } as VersementDraft,

    offlineQueue: JSON.parse(localStorage.getItem('offline_versements') || '[]') as OfflineVersement[],
    isSubmitting: false,
    submissionSuccess: false,
    isOfflineSaved: false
  }),

  getters: {
    hasDeficit: (state) => state.draft.ecart < 0,
    hasSurplus: (state) => state.draft.ecart > 0,
    isStep2Valid: (state) => {
      if (state.draft.montantVerse <= 0) return false;
      if (state.draft.ecart < 0 && !state.draft.motifEcart) return false;
      return true;
    },
    pendingCount: (state) => state.offlineQueue.filter(v => v.statut === 'EN_ATTENTE_SYNC').length
  },

  actions: {
    initDraft(bus: { id: string; immatriculation: string; ligneNom: string; montantAttenduJour: number }) {
      this.currentStep = 1;
      this.submissionSuccess = false;
      this.isOfflineSaved = false;
      this.draft = {
        busId: bus.id,
        immatriculation: bus.immatriculation,
        ligneNom: bus.ligneNom,
        montantAttendu: bus.montantAttenduJour || 120000,
        montantVerse: 0,
        ecart: -(bus.montantAttenduJour || 120000),
        motifEcart: '',
        commentaire: '',
        dateVersement: new Date().toISOString().split('T')[0]
      };
    },

    setMontantVerse(montant: number) {
      this.draft.montantVerse = montant;
      this.draft.ecart = montant - this.draft.montantAttendu;
      if (this.draft.ecart >= 0) {
        this.draft.motifEcart = '';
      }
    },

    nextStep() {
      if (this.currentStep < 3) {
        this.currentStep++;
      }
    },

    prevStep() {
      if (this.currentStep > 1) {
        this.currentStep--;
      }
    },

    async submitVersement() {
      this.isSubmitting = true;
      this.submissionSuccess = false;
      this.isOfflineSaved = false;

      try {
        await apiClient.post('/versements/', {
          bus: this.draft.busId,
          montant_verse: this.draft.montantVerse,
          montant_attendu: this.draft.montantAttendu,
          motif_ecart: this.draft.motifEcart,
          commentaire: this.draft.commentaire,
          date_versement: this.draft.dateVersement
        });

        this.submissionSuccess = true;
      } catch (error: any) {
        // En cas d'absence de réseau ou d'erreur serveur, sauvegarde dans la file locale
        console.warn('Enregistrement en local (mode hors-ligne):', error.message);
        
        const offlineItem: OfflineVersement = {
          ...this.draft,
          localId: `offline-${Date.now()}`,
          dateCreation: new Date().toISOString(),
          statut: 'EN_ATTENTE_SYNC'
        };

        this.offlineQueue.push(offlineItem);
        localStorage.setItem('offline_versements', JSON.stringify(this.offlineQueue));
        this.isOfflineSaved = true;
        this.submissionSuccess = true;
      } finally {
        this.isSubmitting = false;
      }
    },

    resetDraft() {
      this.currentStep = 1;
      this.submissionSuccess = false;
      this.isOfflineSaved = false;
    }
  }
});
