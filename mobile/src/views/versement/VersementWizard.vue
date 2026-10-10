<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar color="primary">
        <ion-buttons slot="start">
          <ion-back-button default-href="/tabs/home" :text="t('common.back')" />
        </ion-buttons>
        <ion-title>{{ t('versement.title') }}</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true" class="ion-padding wizard-content">
      <!-- Indicateur d'étapes (1 à 3) -->
      <div class="steps-progress" v-if="!versementStore.submissionSuccess">
        <div class="step-indicator" :class="{ active: versementStore.currentStep >= 1 }">
          <span class="step-number">1</span>
          <span class="step-label">{{ t('versement.step1Title') }}</span>
        </div>
        <div class="step-line" :class="{ filled: versementStore.currentStep >= 2 }"></div>
        <div class="step-indicator" :class="{ active: versementStore.currentStep >= 2 }">
          <span class="step-number">2</span>
          <span class="step-label">{{ t('versement.step2Title') }}</span>
        </div>
        <div class="step-line" :class="{ filled: versementStore.currentStep >= 3 }"></div>
        <div class="step-indicator" :class="{ active: versementStore.currentStep >= 3 }">
          <span class="step-number">3</span>
          <span class="step-label">{{ t('versement.step3Title') }}</span>
        </div>
      </div>

      <!-- ================= ÉTAPE 1 : BUS & LIGNE ================= -->
      <div v-if="versementStore.currentStep === 1 && !versementStore.submissionSuccess" class="step-card">
        <h2 class="step-heading">{{ t('versement.step1Title') }}</h2>
        <p class="step-subheading">{{ t('versement.step1Subtitle') }}</p>

        <div class="info-block">
          <div class="info-row">
            <span class="info-label">{{ t('versement.bus') }}</span>
            <span class="info-value highlight">{{ versementStore.draft.immatriculation || '1234 TAB' }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">{{ t('versement.lineLabel') }}</span>
            <span class="info-value">{{ versementStore.draft.ligneNom || 'Ligne 133' }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">{{ t('versement.expectedAmount') }}</span>
            <span class="info-value amount-expected">{{ formatMontant(versementStore.draft.montantAttendu) }}</span>
          </div>
        </div>

        <ion-button expand="block" size="large" class="step-btn ion-margin-top" @click="versementStore.nextStep">
          {{ t('common.next') }}
          <ion-icon :icon="arrowForwardOutline" slot="end" />
        </ion-button>
      </div>

      <!-- ================= ÉTAPE 2 : MONTANT VERSÉ ================= -->
      <div v-else-if="versementStore.currentStep === 2 && !versementStore.submissionSuccess" class="step-card">
        <h2 class="step-heading">{{ t('versement.step2Title') }}</h2>
        <p class="step-subheading">{{ t('versement.step2Subtitle') }}</p>

        <div class="amount-input-box">
          <label class="input-label">{{ t('versement.actualAmount') }} (Ariary)</label>
          <ion-item lines="none" class="amount-field">
            <ion-input
              v-model.number="inputMontant"
              type="number"
              inputmode="numeric"
              placeholder="0"
              class="huge-amount-input"
              @ionInput="onMontantChange"
            />
            <span slot="end" class="currency-label">Ar</span>
          </ion-item>
        </div>

        <!-- Raccourcis de montants rapides -->
        <div class="quick-amounts">
          <ion-chip @click="setQuickMontant(versementStore.draft.montantAttendu)">
            {{ formatMontant(versementStore.draft.montantAttendu) }} (Exact)
          </ion-chip>
          <ion-chip @click="setQuickMontant(100000)">100 000 Ar</ion-chip>
          <ion-chip @click="setQuickMontant(80000)">80 000 Ar</ion-chip>
        </div>

        <!-- Calcul de l'écart automatique -->
        <div v-if="versementStore.draft.montantVerse > 0" class="ecart-card" :class="ecartClass">
          <div class="ecart-header">
            <span>{{ t('versement.difference') }} :</span>
            <strong class="ecart-value">{{ formatMontant(versementStore.draft.ecart) }}</strong>
          </div>
          <p class="ecart-desc">
            {{ versementStore.hasDeficit ? t('versement.differenceDeficit') : t('versement.differenceSurplus') }}
          </p>
        </div>

        <!-- Motif obligatoire si écart négatif -->
        <div v-if="versementStore.hasDeficit && versementStore.draft.montantVerse > 0" class="reason-section ion-margin-top">
          <label class="reason-label text-danger">
            ⚠️ {{ t('versement.reasonRequired') }}
          </label>
          <ion-item lines="inset" class="custom-select-item">
            <ion-select
              v-model="versementStore.draft.motifEcart"
              :placeholder="t('versement.selectReason')"
              interface="action-sheet"
              class="reason-select"
            >
              <ion-select-option value="traffic">{{ t('versement.reasons.traffic') }}</ion-select-option>
              <ion-select-option value="weather">{{ t('versement.reasons.weather') }}</ion-select-option>
              <ion-select-option value="breakdown">{{ t('versement.reasons.breakdown') }}</ion-select-option>
              <ion-select-option value="police">{{ t('versement.reasons.police') }}</ion-select-option>
              <ion-select-option value="low_passengers">{{ t('versement.reasons.low_passengers') }}</ion-select-option>
              <ion-select-option value="other">{{ t('versement.reasons.other') }}</ion-select-option>
            </ion-select>
          </ion-item>

          <ion-item lines="inset" class="custom-textarea-item ion-margin-top">
            <ion-textarea
              v-model="versementStore.draft.commentaire"
              :placeholder="t('versement.commentPlaceholder')"
              :rows="2"
            />
          </ion-item>
        </div>

        <div class="wizard-actions ion-margin-top">
          <ion-button fill="outline" color="medium" @click="versementStore.prevStep">
            {{ t('common.back') }}
          </ion-button>
          <ion-button
            color="primary"
            class="next-btn"
            :disabled="!versementStore.isStep2Valid"
            @click="versementStore.nextStep"
          >
            {{ t('common.next') }}
            <ion-icon :icon="arrowForwardOutline" slot="end" />
          </ion-button>
        </div>
      </div>

      <!-- ================= ÉTAPE 3 : CONFIRMATION ================= -->
      <div v-else-if="versementStore.currentStep === 3 && !versementStore.submissionSuccess" class="step-card">
        <h2 class="step-heading">{{ t('versement.step3Title') }}</h2>
        <p class="step-subheading">{{ t('versement.step3Subtitle') }}</p>

        <div class="summary-card">
          <div class="summary-row">
            <span>{{ t('versement.bus') }}</span>
            <strong>{{ versementStore.draft.immatriculation }}</strong>
          </div>
          <div class="summary-row">
            <span>{{ t('versement.lineLabel') }}</span>
            <span>{{ versementStore.draft.ligneNom }}</span>
          </div>
          <div class="summary-row">
            <span>{{ t('versement.expectedAmount') }}</span>
            <span>{{ formatMontant(versementStore.draft.montantAttendu) }}</span>
          </div>
          <div class="summary-row summary-highlight">
            <span>{{ t('versement.actualAmount') }}</span>
            <strong class="text-primary">{{ formatMontant(versementStore.draft.montantVerse) }}</strong>
          </div>
          <div class="summary-row" :class="ecartClass">
            <span>{{ t('versement.difference') }}</span>
            <strong>{{ formatMontant(versementStore.draft.ecart) }}</strong>
          </div>
          <div v-if="versementStore.draft.motifEcart" class="summary-row reason-row">
            <span>{{ t('versement.selectReason') }}</span>
            <em>{{ t(`versement.reasons.${versementStore.draft.motifEcart}`) }}</em>
          </div>
        </div>

        <div class="wizard-actions ion-margin-top">
          <ion-button fill="outline" color="medium" @click="versementStore.prevStep">
            {{ t('common.back') }}
          </ion-button>
          <ion-button
            color="success"
            class="submit-btn"
            :disabled="versementStore.isSubmitting"
            @click="handleSubmit"
          >
            <ion-spinner v-if="versementStore.isSubmitting" name="crescent" slot="start" />
            <ion-icon v-else :icon="checkmarkCircleOutline" slot="start" />
            {{ t('versement.submit') }}
          </ion-button>
        </div>
      </div>

      <!-- ================= ÉCRAN DE SUCCÈS ================= -->
      <div v-else-if="versementStore.submissionSuccess" class="success-card">
        <div class="success-icon-circle">
          <ion-icon :icon="checkmarkOutline" />
        </div>
        <h2 class="success-title">{{ t('versement.successTitle') }}</h2>
        <p class="success-desc">
          {{ versementStore.isOfflineSaved ? t('versement.offlineSaved') : t('versement.successMessage') }}
        </p>

        <ion-button expand="block" size="large" class="ion-margin-top" @click="finishVersement">
          {{ t('common.close') }}
        </ion-button>
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
  IonButtons,
  IonBackButton,
  IonContent,
  IonButton,
  IonIcon,
  IonItem,
  IonInput,
  IonSelect,
  IonSelectOption,
  IonTextarea,
  IonChip,
  IonSpinner
} from '@ionic/vue';
import {
  arrowForwardOutline,
  checkmarkCircleOutline,
  checkmarkOutline
} from 'ionicons/icons';
import { useVersementStore } from '../../stores/versement';
import { useAuthStore } from '../../stores/auth';

const { t } = useI18n();
const router = useRouter();
const versementStore = useVersementStore();
const authStore = useAuthStore();

const inputMontant = ref<number | null>(versementStore.draft.montantVerse || null);

// Initialiser avec le bus actif si non initialisé
if (!versementStore.draft.busId && authStore.activeBus) {
  versementStore.initDraft(authStore.activeBus);
}

const formatMontant = (val: number) => {
  return new Intl.NumberFormat('fr-MG').format(val) + ' Ar';
};

const ecartClass = computed(() => {
  if (versementStore.draft.ecart < 0) return 'ecart-deficit';
  if (versementStore.draft.ecart > 0) return 'ecart-surplus';
  return 'ecart-exact';
});

const onMontantChange = (e: any) => {
  const val = Number(e.detail.value) || 0;
  versementStore.setMontantVerse(val);
};

const setQuickMontant = (val: number) => {
  inputMontant.value = val;
  versementStore.setMontantVerse(val);
};

const handleSubmit = async () => {
  await versementStore.submitVersement();
};

const finishVersement = () => {
  versementStore.resetDraft();
  router.replace('/tabs/home');
};
</script>

<style scoped>
.wizard-content {
  --background: #f4f6f9;
}

.steps-progress {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 12px 0 20px 0;
  padding: 0 10px;
}

.step-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.step-number {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #cbd5e0;
  color: #fff;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
}

.step-indicator.active .step-number {
  background: var(--ion-color-primary);
  box-shadow: 0 2px 8px rgba(56, 128, 255, 0.4);
}

.step-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #718096;
}

.step-indicator.active .step-label {
  color: var(--ion-color-primary);
}

.step-line {
  flex: 1;
  height: 3px;
  background: #e2e8f0;
  margin: 0 8px;
  margin-bottom: 16px;
}

.step-line.filled {
  background: var(--ion-color-primary);
}

.step-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.step-heading {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 800;
  color: #1a202c;
}

.step-subheading {
  margin: 4px 0 18px 0;
  font-size: 0.9rem;
  color: #718096;
}

.info-block {
  background: #f8fafc;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.95rem;
}

.info-label {
  color: #718096;
}

.info-value {
  font-weight: 700;
  color: #2d3748;
}

.amount-expected {
  font-size: 1.15rem;
  color: var(--ion-color-primary);
}

.amount-input-box {
  margin: 12px 0;
}

.input-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #4a5568;
  display: block;
  margin-bottom: 6px;
}

.amount-field {
  --background: #edf2f7;
  --border-radius: 12px;
  padding: 6px 12px;
}

.huge-amount-input {
  font-size: 1.8rem;
  font-weight: 800;
  color: #1a202c;
}

.currency-label {
  font-size: 1.2rem;
  font-weight: 700;
  color: #718096;
}

.quick-amounts {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin: 12px 0;
}

.ecart-card {
  border-radius: 12px;
  padding: 14px;
  margin-top: 14px;
}

.ecart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1rem;
}

.ecart-desc {
  margin: 4px 0 0 0;
  font-size: 0.85rem;
}

.ecart-deficit {
  background: #fff5f5;
  color: #c53030;
  border: 1px solid #feb2b2;
}

.ecart-surplus {
  background: #f0fff4;
  color: #22543d;
  border: 1px solid #9ae6b4;
}

.ecart-exact {
  background: #ebf8ff;
  color: #2b6cb0;
  border: 1px solid #bee3f8;
}

.reason-label {
  font-size: 0.85rem;
  font-weight: 700;
  display: block;
  margin-bottom: 6px;
}

.text-danger {
  color: #e53e3e;
}

.custom-select-item,
.custom-textarea-item {
  --background: #f8fafc;
  --border-radius: 10px;
}

.wizard-actions {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.wizard-actions ion-button {
  flex: 1;
  height: 50px;
  --border-radius: 12px;
  font-weight: 700;
}

.summary-card {
  background: #f8fafc;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.95rem;
}

.summary-highlight {
  font-size: 1.15rem;
  border-top: 1px dashed #cbd5e0;
  padding-top: 8px;
}

.text-primary {
  color: var(--ion-color-primary);
}

.success-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 32px 20px;
  text-align: center;
  margin-top: 40px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.success-icon-circle {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: #48bb78;
  color: #ffffff;
  font-size: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

.success-title {
  margin: 0;
  font-size: 1.4rem;
  font-weight: 800;
  color: #1a202c;
}

.success-desc {
  color: #718096;
  font-size: 0.95rem;
  margin-top: 8px;
  line-height: 1.4;
}
</style>
