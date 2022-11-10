import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import LOCALES_PT from "./pt/locales";
import LOCALES_EN from "./en/locales";

i18n.use(initReactI18next).init({
    resources: {
        pt: {
            translation: LOCALES_PT,
        },
        en: {
            translation: LOCALES_EN,
        },
    },
    lng: localStorage.getItem("language") || "pt",
    fallbackLng: "en",
    supportedLngs: ["pt", "en"],
});

export default i18n;
