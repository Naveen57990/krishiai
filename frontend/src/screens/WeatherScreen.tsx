import React, { useState, useEffect } from "react";
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ScrollView, ActivityIndicator } from "react-native";
import { useAuth } from "../context/AuthContext";
import { useTranslation } from "../context/LanguageContext";
import { weather as weatherApi } from "../services/api";

export default function WeatherScreen() {
  const { user } = useAuth();
  const { t } = useTranslation();
  const [location, setLocation] = useState(user?.location || "");
  const [weather, setWeather] = useState<any>(null);
  const [forecast, setForecast] = useState<any[]>([]);
  const [advice, setAdvice] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const fetchWeather = async () => {
    if (!location) return;
    setLoading(true);
    try {
      const [wRes, fRes, aRes] = await Promise.all([
        weatherApi.current(location),
        weatherApi.forecast(location),
        weatherApi.farmingAdvice(location),
      ]);
      setWeather(wRes.data);
      setForecast(fRes.data.forecast || []);
      setAdvice(aRes.data);
    } catch {} finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>🌤️ {t("weather")}</Text>
      <View style={styles.searchRow}>
        <TextInput style={styles.input} placeholder={t("location")} value={location} onChangeText={setLocation} />
        <TouchableOpacity style={styles.searchBtn} onPress={fetchWeather} disabled={loading}>
          <Text style={styles.searchBtnText}>Search</Text>
        </TouchableOpacity>
      </View>

      {loading && <ActivityIndicator style={{ marginTop: 20 }} color="#2D6A4F" />}

      {weather && (
        <View style={styles.card}>
          <Text style={styles.temp}>{Math.round(weather.temperature)}°C</Text>
          <Text style={styles.desc}>{weather.weather_description}</Text>
          <View style={styles.details}>
            <Text>💧 {weather.humidity}% Humidity</Text>
            <Text>🌬️ {weather.wind_speed} m/s Wind</Text>
            {weather.rainfall_mm && <Text>🌧️ {weather.rainfall_mm}mm Rain</Text>}
          </View>
        </View>
      )}

      {forecast.length > 0 && (
        <>
          <Text style={styles.sectionTitle}>5-Day Forecast</Text>
          <ScrollView horizontal showsHorizontalScrollIndicator={false}>
            {forecast.map((day: any, i: number) => (
              <View key={i} style={styles.forecastCard}>
                <Text style={styles.forecastDate}>{day.date?.slice(5)}</Text>
                <Text style={styles.forecastTemp}>{Math.round(day.temp_max)}°/{Math.round(day.temp_min)}°</Text>
                <Text style={styles.forecastCondition}>{day.condition}</Text>
                <Text style={styles.forecastDetail}>💧 {day.humidity}%</Text>
              </View>
            ))}
          </ScrollView>
        </>
      )}

      {advice && (
        <View style={styles.adviceCard}>
          <Text style={styles.adviceTitle}>🌾 Farming Advice</Text>
          <Text style={styles.adviceText}>{advice.farming_advice}</Text>
          {advice.irrigation_advice && <Text style={styles.adviceItem}>💧 {advice.irrigation_advice}</Text>}
          {advice.pesticide_advice && <Text style={styles.adviceItem}>🧪 {advice.pesticide_advice}</Text>}
          {advice.alerts?.map((alert: string, i: number) => (
            <Text key={i} style={styles.alert}>⚠️ {alert}</Text>
          ))}
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F0FDF4", padding: 16 },
  title: { fontSize: 24, fontWeight: "bold", color: "#2D6A4F", marginBottom: 16 },
  searchRow: { flexDirection: "row", gap: 8, marginBottom: 20 },
  input: { flex: 1, backgroundColor: "#fff", borderRadius: 12, padding: 14, fontSize: 16 },
  searchBtn: { backgroundColor: "#2D6A4F", borderRadius: 12, paddingHorizontal: 20, justifyContent: "center" },
  searchBtnText: { color: "#fff", fontWeight: "600" },
  card: { backgroundColor: "#fff", borderRadius: 16, padding: 20, marginBottom: 16, elevation: 2 },
  temp: { fontSize: 48, fontWeight: "bold", color: "#2D6A4F" },
  desc: { fontSize: 18, color: "#6B7280", marginBottom: 12 },
  details: { gap: 4 },
  sectionTitle: { fontSize: 18, fontWeight: "600", color: "#374151", marginBottom: 12 },
  forecastCard: { backgroundColor: "#fff", borderRadius: 12, padding: 16, marginRight: 12, minWidth: 100, alignItems: "center", elevation: 1 },
  forecastDate: { fontSize: 14, color: "#6B7280", marginBottom: 4 },
  forecastTemp: { fontSize: 18, fontWeight: "600", color: "#2D6A4F" },
  forecastCondition: { fontSize: 12, color: "#9CA3AF" },
  forecastDetail: { fontSize: 12, color: "#6B7280", marginTop: 4 },
  adviceCard: { backgroundColor: "#fff", borderRadius: 16, padding: 20, marginTop: 16, elevation: 2 },
  adviceTitle: { fontSize: 18, fontWeight: "600", color: "#2D6A4F", marginBottom: 8 },
  adviceText: { fontSize: 14, color: "#374151", lineHeight: 22, marginBottom: 8 },
  adviceItem: { fontSize: 14, color: "#6B7280", marginTop: 4, lineHeight: 20 },
  alert: { fontSize: 14, color: "#EF4444", marginTop: 4, fontWeight: "500" },
});
