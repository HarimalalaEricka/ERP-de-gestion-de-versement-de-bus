<template>
  <ion-page>
    <ion-content class="ion-padding auth-content">
      <div class="auth-wrapper">
        <!-- Sélecteur de langue en haut -->
        <div class="language-switch">
          <ion-button
            fill="clear"
            size="small"
            :class="{ active: currentLocale === 'mg' }"
            @click="switchLocale('mg')"
          >
            Malagasy
          </ion-button>
          <span class="divider">|</span>
          <ion-button
            fill="clear"
            size="small"
            :class="{ active: currentLocale === 'fr' }"
            @click="switchLocale('fr')"
          >
            Français
          </ion-button>
        </div>

        <!-- Logo / Titre -->
        <div class="brand-section">
          <div class="bus-icon-circle">
            <ion-icon :icon="busOutline" class="bus-icon" />
          </div>
          <h1 class="app-title">Versement Bus</h1>
          <p class="app-subtitle">{{ t('auth.subtitle') }}</p>
        </div>

        <!-- Formulaire de connexion -->
        <div class="form-card">
          <ion-item lines="inset" class="custom-item">
            <ion-icon :icon="callOutline" slot="start" color="primary" />
            <ion-input
              v-model="telephone"
              type="tel"
              :label="t('auth.phone')"
              label-placement="stacked"
              :placeholder="t('auth.phonePlaceholder')"
              required
            />
          </ion-item>

          <ion-item lines="inset" class="custom-item ion-margin-top">
            <ion-icon :icon="lockClosedOutline" slot="start" color="primary" />
            <ion-input
              v-model="password"
              type="password"
              :label="t('auth.password')"
              label-placement="stacked"
              :placeholder="t('auth.passwordPlaceholder')"
              required
            />
          </ion-item>

          <ion-button
            expand="block"
            size="large"
            class="submit-button ion-margin-top"
            :disabled="authStore.isLoading || !telephone"
            @click="handleLogin"
          >
            <ion-spinner v-if="authStore.isLoading" name="crescent" slot="start" />
            <ion-icon v-else :icon="logInOutline" slot="start" />
            {{ t('auth.login') }}
          </ion-button>
        </div>

        <div class="demo-hint ion-text-center">
          <p class="hint-text">Mode démo chauffeur activé par défaut</p>
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
  IonContent,
  IonItem,
  IonInput,
  IonButton,
  IonIcon,
  IonSpinner
} from '@ionic/vue';
import {
  busOutline,
  callOutline,
  lockClosedOutline,
  logInOutline
} from 'ionicons/icons';
import { useAuthStore } from '../../stores/auth';

const { t, locale } = useI18n();
const router = useRouter();
const authStore = useAuthStore();

const telephone = ref('0340987654');
const password = ref('password');

const currentLocale = computed(() => locale.value);

const switchLocale = (lang: string) => {
  locale.value = lang;
  localStorage.setItem('app_locale', lang);
};

const handleLogin = async () => {
  await authStore.login(telephone.value, password.value);
  router.replace('/tabs/home');
};
</script>

<style scoped>
.auth-content {
  --background: #f4f6f9;
}

.auth-wrapper {
  max-width: 440px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 90vh;
}

.language-switch {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 4px;
}

.language-switch .active {
  font-weight: bold;
  --color: var(--ion-color-primary);
}

.divider {
  color: #a0aec0;
}

.brand-section {
  text-align: center;
  margin: 24px 0;
}

.bus-icon-circle {
  width: 80px;
  height: 80px;
  background: var(--ion-color-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  box-shadow: 0 4px 14px rgba(56, 128, 255, 0.3);
}

.bus-icon {
  font-size: 42px;
  color: #fff;
}

.app-title {
  font-size: 1.6rem;
  font-weight: 800;
  margin: 0;
  color: #1a202c;
}

.app-subtitle {
  font-size: 0.95rem;
  color: #718096;
  margin-top: 6px;
}

.form-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.custom-item {
  --background: #f8fafc;
  --border-radius: 10px;
  margin-bottom: 8px;
  color: #1a202c;
}

.submit-button {
  margin-top: 24px;
  height: 52px;
  --border-radius: 12px;
  font-weight: 600;
  font-size: 1.05rem;
}

.demo-hint {
  margin-top: 20px;
}

.hint-text {
  font-size: 0.85rem;
  color: #718096;
}
</style>
