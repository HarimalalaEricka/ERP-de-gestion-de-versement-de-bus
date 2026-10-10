<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar color="primary">
        <ion-title>{{ t('profil.title') }}</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true" class="ion-padding profil-content">
      <!-- En-tête profil -->
      <div class="profile-header-card">
        <div class="avatar-circle">
          <ion-icon :icon="personCircleOutline" class="avatar-icon" />
        </div>
        <h2 class="profile-name">{{ authStore.chauffeurNomComplet || 'Jean Rakotondrabe' }}</h2>
        <span class="role-badge">{{ t('profil.driver') }}</span>
      </div>

      <!-- Informations -->
      <div class="section-card ion-margin-top">
        <h3 class="section-title">{{ t('profil.personalInfo') }}</h3>

        <ion-list lines="inset">
          <ion-item>
            <ion-icon :icon="callOutline" slot="start" color="medium" />
            <ion-label>
              <h3>{{ t('profil.phone') }}</h3>
              <p>{{ authStore.user?.telephone || '034 12 345 67' }}</p>
            </ion-label>
          </ion-item>

          <ion-item>
            <ion-icon :icon="businessOutline" slot="start" color="medium" />
            <ion-label>
              <h3>{{ t('profil.organization') }}</h3>
              <p>{{ authStore.user?.organisationNom || 'Coopérative Miray' }}</p>
            </ion-label>
          </ion-item>
        </ion-list>
      </div>

      <!-- Préférences / Bascule Malgache / Français -->
      <div class="section-card ion-margin-top">
        <h3 class="section-title">{{ t('profil.preferences') }}</h3>

        <ion-item lines="none" class="language-item">
          <ion-icon :icon="languageOutline" slot="start" color="primary" />
          <ion-select
            v-model="selectedLanguage"
            :label="t('profil.language')"
            label-placement="stacked"
            interface="action-sheet"
            @ionChange="onLanguageChange"
          >
            <ion-select-option value="mg">🇲🇬 Malagasy</ion-select-option>
            <ion-select-option value="fr">🇫🇷 Français</ion-select-option>
          </ion-select>
        </ion-item>
      </div>

      <!-- Déconnexion -->
      <div class="logout-section ion-margin-top">
        <ion-button
          expand="block"
          color="danger"
          fill="outline"
          class="logout-btn"
          @click="confirmLogout"
        >
          <ion-icon :icon="logOutOutline" slot="start" />
          {{ t('auth.logout') }}
        </ion-button>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonList,
  IonItem,
  IonLabel,
  IonIcon,
  IonSelect,
  IonSelectOption,
  IonButton,
  alertController
} from '@ionic/vue';
import {
  personCircleOutline,
  callOutline,
  businessOutline,
  languageOutline,
  logOutOutline
} from 'ionicons/icons';
import { useAuthStore } from '../../stores/auth';

const { t, locale } = useI18n();
const router = useRouter();
const authStore = useAuthStore();

const selectedLanguage = ref(locale.value);

const onLanguageChange = (e: any) => {
  const newLang = e.detail.value;
  locale.value = newLang;
  localStorage.setItem('app_locale', newLang);
};

const confirmLogout = async () => {
  const alert = await alertController.create({
    header: t('auth.logout'),
    message: t('profil.logoutConfirm'),
    buttons: [
      {
        text: t('common.cancel'),
        role: 'cancel'
      },
      {
        text: t('auth.logout'),
        role: 'destructive',
        handler: () => {
          authStore.logout();
          router.replace('/login');
        }
      }
    ]
  });
  await alert.present();
};
</script>

<style scoped>
.profil-content {
  --background: #f4f6f9;
}

.profile-header-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 24px 16px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.avatar-circle {
  width: 76px;
  height: 76px;
  margin: 0 auto 12px;
  color: var(--ion-color-primary);
}

.avatar-icon {
  font-size: 76px;
}

.profile-name {
  margin: 0;
  font-size: 1.35rem;
  font-weight: 800;
  color: #1a202c;
}

.role-badge {
  display: inline-block;
  margin-top: 6px;
  padding: 4px 12px;
  background: #ebf8ff;
  color: #2b6cb0;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 700;
}

.section-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.section-title {
  margin: 0 0 10px 4px;
  font-size: 0.95rem;
  font-weight: 700;
  color: #4a5568;
}

.language-item {
  --background: #f8fafc;
  --border-radius: 10px;
}

.logout-section {
  margin-top: 30px;
}

.logout-btn {
  --border-radius: 12px;
  font-weight: 700;
  height: 48px;
}
</style>
