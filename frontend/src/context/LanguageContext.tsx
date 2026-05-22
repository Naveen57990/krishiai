import React, { createContext, useContext, useState, ReactNode } from "react";
import { Language } from "../types";

const translations: Record<Language, Record<string, string>> = {
  en: {
    app_name: "KrishiAI",
    login: "Login",
    signup: "Sign Up",
    email: "Email",
    password: "Password",
    full_name: "Full Name",
    phone: "Phone",
    dashboard: "Dashboard",
    disease_detection: "Disease Detection",
    chatbot: "AI Chatbot",
    voice_assistant: "Voice Assistant",
    weather: "Weather",
    crop_recommendation: "Crop Recommendations",
    yield_prediction: "Yield Prediction",
    settings: "Settings",
    logout: "Logout",
    camera: "Camera",
    gallery: "Gallery",
    detect: "Detect Disease",
    start_chat: "Start Chat",
    record_voice: "Record Voice",
    location: "Location",
    soil_type: "Soil Type",
    ph_level: "pH Level",
    season: "Season",
    get_recommendations: "Get Recommendations",
    predict_yield: "Predict Yield",
    crop_name: "Crop Name",
    area: "Area (Hectares)",
    history: "History",
    profile: "Profile",
    save: "Save",
    cancel: "Cancel",
    loading: "Loading...",
    error: "Error",
    success: "Success",
  },
  te: {
    app_name: "కృషిఎఐ",
    login: "లాగిన్",
    signup: "సైన్ అప్",
    email: "ఇమెయిల్",
    password: "పాస్‌వర్డ్",
    full_name: "పూర్తి పేరు",
    phone: "ఫోన్",
    dashboard: "డ్యాష్‌బోర్డ్",
    disease_detection: "వ్యాధి గుర్తింపు",
    chatbot: "AI చాట్‌బాట్",
    voice_assistant: "వాయిస్ అసిస్టెంట్",
    weather: "వాతావరణం",
    crop_recommendation: "పంట సిఫార్సులు",
    yield_prediction: "దిగుబడి అంచనా",
    settings: "సెట్టింగ్స్",
    logout: "లాగ్ అవుట్",
    camera: "కెమెరా",
    gallery: "గ్యాలరీ",
    detect: "వ్యాధిని గుర్తించండి",
    start_chat: "చాట్ ప్రారంభించండి",
    record_voice: "వాయిస్ రికార్డ్ చేయండి",
    location: "ప్రదేశం",
    soil_type: "నేల రకం",
    ph_level: "pH స్థాయి",
    season: "సీజన్",
    get_recommendations: "సిఫార్సులు పొందండి",
    predict_yield: "దిగుబడి అంచనా",
    crop_name: "పంట పేరు",
    area: "విస్తీర్ణం (హెక్టార్లు)",
    history: "చరిత్ర",
    profile: "ప్రొఫైల్",
    save: "సేవ్",
    cancel: "రద్దు",
    loading: "లోడ్ అవుతోంది...",
    error: "లోపం",
    success: "విజయం",
  },
  hi: {
    app_name: "कृशिऐ",
    login: "लॉग इन",
    signup: "साइन अप",
    email: "ईमेल",
    password: "पासवर्ड",
    full_name: "पूरा नाम",
    phone: "फोन",
    dashboard: "डैशबोर्ड",
    disease_detection: "रोग का पता लगाना",
    chatbot: "AI चैटबॉट",
    voice_assistant: "वॉयस असिस्टेंट",
    weather: "मौसम",
    crop_recommendation: "फसल अनुशंसाएं",
    yield_prediction: "उपज अनुमान",
    settings: "सेटिंग्स",
    logout: "लॉग आउट",
    camera: "कैमरा",
    gallery: "गैलरी",
    detect: "रोग का पता लगाएं",
    start_chat: "चैट शुरू करें",
    record_voice: "आवाज रिकॉर्ड करें",
    location: "स्थान",
    soil_type: "मिट्टी का प्रकार",
    ph_level: "pH स्तर",
    season: "मौसम",
    get_recommendations: "अनुशंसाएं प्राप्त करें",
    predict_yield: "उपज का अनुमान लगाएं",
    crop_name: "फसल का नाम",
    area: "क्षेत्र (हेक्टेयर)",
    history: "इतिहास",
    profile: "प्रोफ़ाइल",
    save: "सहेजें",
    cancel: "रद्द करें",
    loading: "लोड हो रहा है...",
    error: "त्रुटि",
    success: "सफलता",
  },
};

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: (key: string) => string;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const LanguageProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [language, setLanguage] = useState<Language>("en");

  const t = (key: string): string => {
    return translations[language]?.[key] || translations["en"]?.[key] || key;
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useTranslation = () => {
  const context = useContext(LanguageContext);
  if (!context) throw new Error("useTranslation must be used within LanguageProvider");
  return context;
};
