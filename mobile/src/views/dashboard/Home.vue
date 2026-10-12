<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar color="primary">
        <ion-title>{{ t('dashboard.welcome', { name: authStore.chauffeurNomComplet || 'Mpamily' }) }}</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true" class="ion-padding dashboard-content">
      <!-- Bannière hors-ligne si versements en attente -->
      <div v-if="versementStore.pendingCount > 0" class="offline-banner ion-margin-bottom">
        <ion-icon :icon="cloudOfflineOutline" />
        <span>{{ t('offline.pendingSync', { count: versementStore.pendingCount }) }}</span>
      </div>

      <!-- Carte du Bus assigné -->
      <div class="bus-card">
        <div class="bus-card-header">
          <span class="badge-service" :class="{ 'badge-active': isServiceStarted }">
            {{ isServiceStarted ? t('dashboard.inService') : t('dashboard.serviceStopped') }}
          </span>
          <span class="date-text">{{ todayFormatted }}</span>
        </div>

        <div class="bus-main-info">
          <div class="bus-plate">
            <ion-icon :icon="busOutline" class="plate-icon" />
            <h2>{{ authStore.activeBus?.immatriculation || '1234 TAB' }}</h2>
          </div>
          <p class="bus-model">{{ authStore.activeBus?.marqueModele || 'Mercedes Sprinter' }}</p>
          <div class="bus-line">
            <ion-icon :icon="navigateOutline" class="line-icon" />
            <span>{{ authStore.activeBus?.ligneNom || 'Ligne 133' }}</span>
          </div>
        </div>

        <div class="service-actions">
          <ion-button
            v-if="!isServiceStarted"
            expand="block"
            color="success"
            class="service-btn"
            @click="toggleService"
          >
            <ion-icon :icon="playOutline" slot="start" />
            {{ t('dashboard.startService') }}
          </ion-button>
          <ion-button
            v-else
            expand="block"
            fill="outline"
            color="medium"
            class="service-btn"
            @click="toggleService"
          >
            <ion-icon :icon="stopOutline" slot="start" />
            {{ t('dashboard.endService') }}
          </ion-button>
        </div>
      </div>

      <!-- Action principale : Déclarer un versement (Bouton XXL tactile) -->
      <div class="main-action-section ion-margin-top">
        <ion-button
          expand="block"
          color="primary"
          class="huge-action-btn"
          @click="startVersement"
        >
          <div class="huge-action-content">
            <ion-icon :icon="cashOutline" class="huge-action-icon" />
            <div class="huge-action-text">
              <span class="huge-action-title">{{ t('dashboard.declareVersement') }}</span>
              <span class="huge-action-sub">
                {{ t('versement.expectedAmount') }} : {{ formatMontant(authStore.activeBus?.montantAttenduJour || 120000) }}
              </span>
            </div>
          </div>
        </ion-button>
      </div>

      <!-- Actions secondaires en grille : Dépenses & Pannes -->
      <div class="secondary-grid ion-margin-top">
        <div class="secondary-card" @click="handleActionNotImplemented(t('dashboard.declareDepense'))">
          <div class="sec-icon-circle expense-circle">
            <ion-icon :icon="receiptOutline" />
          </div>
          <span class="sec-card-title">{{ t('dashboard.declareDepense') }}</span>
        </div>

        <div class="secondary-card" @click="handleActionNotImplemented(t('dashboard.declarePanne'))">
          <div class="sec-icon-circle alert-circle">
            <ion-icon :icon="warningOutline" />
          </div>
          <span class="sec-card-title">{{ t('dashboard.declarePanne') }}</span>
        </div>
      </div>

      <!-- Aperçu de la situation financière / Dettes -->
      <div class="info-card ion-margin-top">
        <div class="info-card-header">
          <ion-icon :icon="walletOutline" color="primary" />
          <h3>{{ t('dashboard.myDebts') }}</h3>
        </div>
        <div class="info-card-body">
          <span class="debt-amount">0 Ar</span>
          <span class="debt-status text-success">Aucune dette reportée</span>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonButton,
  IonIcon,
  toastController
} from '@ionic/vue';
import {
  busOutline,
  navigateOutline,
  cashOutline,
  receiptOutline,
  warningOutline,
  playOutline,
  stopOutline,
  cloudOfflineOutline,
  walletOutline
} from 'ionicons/icons';
import { useAuthStore } from '../../stores/auth';
import { useVersementStore } from '../../stores/versement';

const { t } = useI18n();
const router = useRouter();
const authStore = useAuthStore();
const versementStore = useVersementStore();

const isServiceStarted = ref(true);

const todayFormatted = computed(() => {
  const d = new Date();
  return d.toLocaleDateString('fr-FR', {
    weekday: 'short',
    day: 'numeric',
    month: 'short'
  });
});

const formatMontant = (val: number) => {
  return new Intl.NumberFormat('fr-MG').format(val) + ' Ar';
};

const toggleService = () => {
  isServiceStarted.value = !isServiceStarted.value;
};

const startVersement = () => {
  if (authStore.activeBus) {
    versementStore.initDraft(authStore.activeBus);
  }
  router.push('/tabs/versement');
};

const handleActionNotImplemented = async (titre: string) => {
  const toast = await toastController.create({
    message: `${titre} : fonction planifiée au Sprint S4`,
    duration: 2000,
    position: 'bottom'
  });
  await toast.present();
};
</script>

<style scoped>
.dashboard-content {
  --background: #f4f6f9;
}

.offline-banner {
  background: #feebc8;
  color: #7b341e;
  border-radius: 10px;
  padding: 10px 14px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  font-weight: 500;
}

.bus-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 18px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.bus-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.badge-service {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  background: #e2e8f0;
  color: #4a5568;
}

.badge-service.badge-active {
  background: #c6f6d5;
  color: #22543d;
}

.date-text {
  font-size: 0.85rem;
  color: #718096;
}

.bus-plate {
  display: flex;
  align-items: center;
  gap: 10px;
}

.bus-plate h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 800;
  color: #1a202c;
  letter-spacing: 0.5px;
}

.plate-icon {
  font-size: 28px;
  color: var(--ion-color-primary);
}

.bus-model {
  margin: 4px 0 8px 38px;
  color: #718096;
  font-size: 0.9rem;
}

.bus-line {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 10px;
  background: #ebf8ff;
  color: #2b6cb0;
  padding: 8px 12px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9rem;
}

.service-actions {
  margin-top: 14px;
}

.service-btn {
  --border-radius: 10px;
  font-weight: 600;
}

.huge-action-btn {
  --border-radius: 16px;
  min-height: 84px;
  box-shadow: 0 4px 14px rgba(56, 128, 255, 0.25);
}

.huge-action-content {
  display: flex;
  align-items: center;
  gap: 16px;
  text-align: left;
  padding: 10px 0;
  width: 100%;
}

.huge-action-icon {
  font-size: 38px;
}

.huge-action-title {
  display: block;
  font-size: 1.15rem;
  font-weight: 700;
}

.huge-action-sub {
  display: block;
  font-size: 0.85rem;
  opacity: 0.9;
  margin-top: 3px;
}

.secondary-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.secondary-card {
  background: #ffffff;
  border-radius: 14px;
  padding: 16px 12px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  cursor: pointer;
  transition: transform 0.15s;
}

.secondary-card:active {
  transform: scale(0.98);
}

.sec-icon-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  margin: 0 auto 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.expense-circle {
  background: #feebc8;
  color: #c05621;
}

.alert-circle {
  background: #fed7d7;
  color: #c53030;
}

.sec-card-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: #2d3748;
}

.info-card {
  background: #ffffff;
  border-radius: 14px;
  padding: 14px 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.info-card-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.info-card-header h3 {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 700;
  color: #2d3748;
}

.info-card-body {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}

.debt-amount {
  font-size: 1.1rem;
  font-weight: 800;
  color: #1a202c;
}

.debt-status {
  font-size: 0.85rem;
}

.text-success {
  color: #38a169;
}
</style>
