import React, { useEffect, useState } from "react";
import {
  View, Text, ScrollView, TouchableOpacity, StyleSheet, RefreshControl,
} from "react-native";
import { useAuth } from "../context/AuthContext";
import { useTranslation } from "../context/LanguageContext";
import { weather as weatherApi } from "../services/api";

const quickActions = [
  { key: "disease", icon: "🔬", labelKey: "disease_detection", route: "DiseaseDetection" },
  { key: "chatbot", icon: "🤖", labelKey: "chatbot", route: "Chatbot" },
  { key: "voice", icon: "🎤", labelKey: "voice_assistant", route: "VoiceAssistant" },
  { key: "weather", icon: "🌤️", labelKey: "weather", route: "Weather" },
  { key: "crop", icon: "🌱", labelKey: "crop_recommendation", route: "CropRecommendation" },
  { key: "yield", icon: "📊", labelKey: "yield_prediction", route: "YieldPrediction" },
];

export default function DashboardScreen({ navigation }: any) {
  const { user } = useAuth();
  const { t, language } = useTranslation();
  const [weather, setWeather] = useState<any>(null);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    fetchWeather();
  }, []);

  const fetchWeather = async () => {
    try {
      const location = user?.location || "Hyderabad";
      const { data } = await weatherApi.current(location);
      setWeather(data);
    } catch {}
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchWeather();
    setRefreshing(false);
  };

  return (
    <ScrollView
      style={styles.container}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
    >
      <View style={styles.header}>
        <Text style={styles.greeting}>
          {language === "te" ? "నమస్కారం" : language === "hi" ? "नमस्ते" : "Hello"},
        </Text>
        <Text style={styles.userName}>{user?.full_name || "Farmer"}</Text>
      </View>

      {weather && (
        <View style={styles.weatherCard}>
          <Text style={styles.weatherTemp}>{Math.round(weather.temperature)}°C</Text>
          <Text style={styles.weatherDesc}>{weather.weather_description}</Text>
          <Text style={styles.weatherLocation}>{weather.location}</Text>
          <View style={styles.weatherDetails}>
            <Text>💧 {weather.humidity}%</Text>
            <Text>🌬️ {weather.wind_speed} m/s</Text>
          </View>
        </View>
      )}

      <Text style={styles.sectionTitle}>{t("dashboard")}</Text>
      <View style={styles.grid}>
        {quickActions.map((action) => (
          <TouchableOpacity
            key={action.key}
            style={styles.gridItem}
            onPress={() => navigation.navigate(action.route)}
          >
            <Text style={styles.gridIcon}>{action.icon}</Text>
            <Text style={styles.gridLabel}>{t(action.labelKey)}</Text>
          </TouchableOpacity>
        ))}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F0FDF4" },
  header: { padding: 24, paddingTop: 48, backgroundColor: "#2D6A4F" },
  greeting: { fontSize: 18, color: "#A7F3D0" },
  userName: { fontSize: 28, fontWeight: "bold", color: "#fff" },
  weatherCard: { backgroundColor: "#fff", margin: 16, borderRadius: 16, padding: 20, elevation: 2 },
  weatherTemp: { fontSize: 36, fontWeight: "bold", color: "#2D6A4F" },
  weatherDesc: { fontSize: 16, color: "#6B7280", marginTop: 4 },
  weatherLocation: { fontSize: 14, color: "#9CA3AF", marginTop: 2 },
  weatherDetails: { flexDirection: "row", gap: 24, marginTop: 12 },
  sectionTitle: { fontSize: 20, fontWeight: "600", color: "#374151", paddingHorizontal: 16, marginBottom: 12 },
  grid: { flexDirection: "row", flexWrap: "wrap", padding: 8 },
  gridItem: { width: "46%", backgroundColor: "#fff", margin: "2%", borderRadius: 16, padding: 20, alignItems: "center", elevation: 2 },
  gridIcon: { fontSize: 32, marginBottom: 8 },
  gridLabel: { fontSize: 14, color: "#374151", textAlign: "center" },
});
