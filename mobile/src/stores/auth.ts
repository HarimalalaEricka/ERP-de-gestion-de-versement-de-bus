import { defineStore } from 'pinia';
import apiClient from '../services/api';

export interface User {
  id: string;
  nom: string;
  prenom: string;
  telephone: string;
  role: string;
  organisationId?: string;
  organisationNom?: string;
}

export interface BusSummary {
  id: string;
  immatriculation: string;
  marqueModele: string;
  ligneNom: string;
  montantAttenduJour: number;
  statut?: string;
  modifie_le?: string;
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('auth_token') as string | null,
    user: JSON.parse(localStorage.getItem('auth_user') || 'null') as User | null,
    activeBus: JSON.parse(localStorage.getItem('active_bus') || 'null') as BusSummary | null,
    totalDettes: Number(localStorage.getItem('total_dettes') || 0),
    isLoading: false,
    error: null as string | null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    chauffeurNomComplet: (state) => state.user ? `${state.user.prenom} ${state.user.nom}` : ''
  },

  actions: {
    async login(telephone: string, motDePasse: string) {
      this.isLoading = true;
      this.error = null;

      try {
        // Tentative d'appel API Django
        const response = await apiClient.post('/auth/login/', {
          telephone,
          password: motDePasse
        });

        this.token = response.data.access || response.data.token;
        this.user = response.data.user;
        this.activeBus = response.data.bus || null;
        console.log(response.data);

        localStorage.setItem('auth_token', this.token || '');
        localStorage.setItem('auth_user', JSON.stringify(this.user));
        if (this.activeBus) {
          localStorage.setItem('active_bus', JSON.stringify(this.activeBus));
        }
      } catch (err: any) {
        console.error('Erreur de connexion :', err);

        this.token = null;
        this.user = null;
        this.activeBus = null;

        localStorage.removeItem('auth_token');
        localStorage.removeItem('auth_user');
        localStorage.removeItem('active_bus');

        this.error =
          err.response?.data?.detail ||
          err.response?.data?.message ||
          'Impossible de se connecter au serveur. Vérifie tes identifiants et la connexion.';
      } finally {
        this.isLoading = false;
      }
    },

    async fetchMonBus() {
      try {
        const response = await apiClient.get('/chauffeur/mon-bus/');
        if (response.data.bus) {
          this.activeBus = response.data.bus;
          localStorage.setItem('active_bus', JSON.stringify(this.activeBus));
        }
        if (typeof response.data.total_dettes === 'number') {
          this.totalDettes = response.data.total_dettes;
          localStorage.setItem('total_dettes', String(this.totalDettes));
        }
      } catch (err) {
        console.warn('Impossible de rafraîchir le bus / dettes :', err);
      }
    },

    async updateBusStatus(statut: string) {
      const response = await apiClient.patch('/chauffeur/mon-bus/', {
        statut
      });

      if (this.activeBus) {
        this.activeBus = {
          ...this.activeBus,
          statut: response.data.statut,
          modifie_le: response.data.modifie_le
        };
        localStorage.setItem('active_bus', JSON.stringify(this.activeBus));
      }

      return response.data;
    },

    setActiveBus(bus: BusSummary | null) {
      this.activeBus = bus;
      if (bus) {
        localStorage.setItem('active_bus', JSON.stringify(bus));
      } else {
        localStorage.removeItem('active_bus');
      }
    },

    logout() {
      this.token = null;
      this.user = null;
      this.activeBus = null;
      this.totalDettes = 0;
      localStorage.removeItem('auth_token');
      localStorage.removeItem('auth_user');
      localStorage.removeItem('active_bus');
      localStorage.removeItem('total_dettes');
    }
  }
});
