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
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('auth_token') as string | null,
    user: JSON.parse(localStorage.getItem('auth_user') || 'null') as User | null,
    activeBus: JSON.parse(localStorage.getItem('active_bus') || 'null') as BusSummary | null,
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
      // } catch (err: any) {
      //   // En mode dev/démo sans backend connecté : connexion mock pour tester l'application
      //   console.warn('Backend non joignable ou erreur API, bascule en mode démo chauffeur:', err.message);
        
      //   // Mock chauffeur par défaut
      //   this.token = 'demo-jwt-token-chauffeur';
      //   this.user = {
      //     id: 'usr-demo-01',
      //     nom: 'Rakotondrabe',
      //     prenom: 'Jean',
      //     telephone: telephone || '034 12 345 67',
      //     role: 'CHAUFFEUR',
      //     organisationNom: 'Coopérative Miray'
      //   };
      //   this.activeBus = {
      //     id: 'bus-demo-01',
      //     immatriculation: '1234 TAB',
      //     marqueModele: 'Mercedes Sprinter',
      //     ligneNom: 'Ligne 133 (Ankatso - Analakely)',
      //     montantAttenduJour: 120000
      //   };

      //   localStorage.setItem('auth_token', this.token);
      //   localStorage.setItem('auth_user', JSON.stringify(this.user));
      //   localStorage.setItem('active_bus', JSON.stringify(this.activeBus));
      // } finally {
      //   this.isLoading = false;
      // }
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
      localStorage.removeItem('auth_token');
      localStorage.removeItem('auth_user');
      localStorage.removeItem('active_bus');
    }
  }
});
