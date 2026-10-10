import { createI18n } from 'vue-i18n';
import fr from './locales/fr.json';
import mg from './locales/mg.json';

const savedLocale = localStorage.getItem('app_locale') || 'fr';

const i18n = createI18n({
  legacy: false,
  locale: savedLocale,
  fallbackLocale: 'fr',
  messages: {
    fr,
    mg
  }
});

export default i18n;
