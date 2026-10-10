<template>
  <ion-page>
    <ion-tabs>
      <ion-router-outlet></ion-router-outlet>
      <ion-tab-bar slot="bottom" class="custom-tab-bar">
        <ion-tab-button tab="home" href="/tabs/home">
          <ion-icon aria-hidden="true" :icon="homeOutline" />
          <ion-label>{{ t('dashboard.today') }}</ion-label>
        </ion-tab-button>

        <ion-tab-button tab="versement" href="/tabs/versement" class="tab-highlight">
          <ion-icon aria-hidden="true" :icon="cashOutline" />
          <ion-label>{{ t('versement.title') }}</ion-label>
        </ion-tab-button>

        <ion-tab-button tab="profil" href="/tabs/profil">
          <ion-icon aria-hidden="true" :icon="personOutline" />
          <ion-label>{{ t('profil.title') }}</ion-label>
        </ion-tab-button>
      </ion-tab-bar>
    </ion-tabs>
  </ion-page>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import {
  IonTabBar,
  IonTabButton,
  IonTabs,
  IonLabel,
  IonIcon,
  IonPage,
  IonRouterOutlet
} from '@ionic/vue';
import {
  homeOutline,
  cashOutline,
  personOutline
} from 'ionicons/icons';

const { t } = useI18n();
</script>

<style scoped>
.custom-tab-bar {
  --background: #ffffff;
  border-top: 1px solid #e2e8f0;
  height: 60px;
}

.tab-highlight {
  --color-selected: var(--ion-color-primary);
}
</style>
