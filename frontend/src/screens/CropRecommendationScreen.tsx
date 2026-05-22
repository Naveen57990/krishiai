import React, { useState } from "react";
import {
  View, Text, TextInput, TouchableOpacity, StyleSheet,
  ScrollView, ActivityIndicator, Alert,
} from "react-native";
import { useTranslation } from "../context/LanguageContext";
import { recommendations as recApi } from "../services/api";

const SOIL_TYPES = ["clay", "loam", "sandy", "black", "clay_loam", "sandy_loam"];
const SEASONS = ["kharif", "rabi", "summer"];

export default function CropRecommendationScreen() {
  const { t, language } = useTranslation();
  const [form, setForm] = useState({
    soil_type: "", ph_level: "", rainfall_mm: "", temperature: "", season: "",
    location: "", farm_size_hectares: "",
  });
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any[]>([]);

  const getRecommendations = async () => {
    if (!form.soil_type || !form.ph_level || !form.season) {
      Alert.alert(t("error"), "Please fill required fields");
      return;
    }
    setLoading(true);
    try {
      const { data } = await recApi.getCropRecommendations({
        soil_type: form.soil_type,
        ph_level: parseFloat(form.ph_level),
        rainfall_mm: parseFloat(form.rainfall_mm) || 800,
        temperature: parseFloat(form.temperature) || 25,
        season: form.season,
        location: form.location || undefined,
        farm_size_hectares: parseFloat(form.farm_size_hectares) || undefined,
      });
      setResults(data.recommendations || []);
    } catch (err: any) {
      Alert.alert(t("error"), err.response?.data?.detail || "Failed to get recommendations");
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (score: number) => {
    if (score > 0.7) return "#EF4444";
    if (score > 0.4) return "#F59E0B";
    return "#10B981";
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>🌱 {t("crop_recommendation")}</Text>

      <View style={styles.form}>
        <Text style={styles.label}>{t("soil_type")}</Text>
        <View style={styles.chipRow}>
          {SOIL_TYPES.map((st) => (
            <TouchableOpacity
              key={st}
              style={[styles.chip, form.soil_type === st && styles.chipActive]}
              onPress={() => setForm({ ...form, soil_type: st })}
            >
              <Text style={[styles.chipText, form.soil_type === st && styles.chipTextActive]}>{st}</Text>
            </TouchableOpacity>
          ))}
        </View>

        <Text style={styles.label}>{t("season")}</Text>
        <View style={styles.chipRow}>
          {SEASONS.map((s) => (
            <TouchableOpacity
              key={s}
              style={[styles.chip, form.season === s && styles.chipActive]}
              onPress={() => setForm({ ...form, season: s })}
            >
              <Text style={[styles.chipText, form.season === s && styles.chipTextActive]}>{s}</Text>
            </TouchableOpacity>
          ))}
        </View>

        <View style={styles.inputRow}>
          <View style={styles.halfInput}>
            <Text style={styles.label}>{t("ph_level")}</Text>
            <TextInput style={styles.input} value={form.ph_level} onChangeText={(v) => setForm({ ...form, ph_level: v })} keyboardType="decimal-pad" placeholder="6.5" />
          </View>
          <View style={styles.halfInput}>
            <Text style={styles.label}>Rainfall (mm)</Text>
            <TextInput style={styles.input} value={form.rainfall_mm} onChangeText={(v) => setForm({ ...form, rainfall_mm: v })} keyboardType="decimal-pad" placeholder="800" />
          </View>
        </View>

        <View style={styles.inputRow}>
          <View style={styles.halfInput}>
            <Text style={styles.label}>Temp (°C)</Text>
            <TextInput style={styles.input} value={form.temperature} onChangeText={(v) => setForm({ ...form, temperature: v })} keyboardType="decimal-pad" placeholder="25" />
          </View>
          <View style={styles.halfInput}>
            <Text style={styles.label}>{t("location")}</Text>
            <TextInput style={styles.input} value={form.location} onChangeText={(v) => setForm({ ...form, location: v })} placeholder="Hyderabad" />
          </View>
        </View>

        <TouchableOpacity style={styles.button} onPress={getRecommendations} disabled={loading}>
          {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>{t("get_recommendations")}</Text>}
        </TouchableOpacity>
      </View>

      {results.map((crop: any, i: number) => (
        <View key={i} style={styles.resultCard}>
          <View style={styles.resultHeader}>
            <Text style={styles.cropName}>{language === "te" && crop.crop_name_te ? crop.crop_name_te : language === "hi" && crop.crop_name_hi ? crop.crop_name_hi : crop.crop_name}</Text>
            <Text style={[styles.riskBadge, { backgroundColor: getRiskColor(crop.risk_score) }]}>
              Risk: {(crop.risk_score * 100).toFixed(0)}%
            </Text>
          </View>
          <View style={styles.metrics}>
            <Text style={styles.metric}>🎯 Match: {(crop.confidence_score * 100).toFixed(0)}%</Text>
            {crop.profitability_estimate && <Text style={styles.metric}>💰 ₹{crop.profitability_estimate.toLocaleString()}/ha</Text>}
            {crop.growing_period_days && <Text style={styles.metric}>📅 {crop.growing_period_days} days</Text>}
          </View>
          {crop.farming_tips?.water && <Text style={styles.tip}>💧 Water: {crop.farming_tips.water}</Text>}
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F0FDF4", padding: 16 },
  title: { fontSize: 24, fontWeight: "bold", color: "#2D6A4F", marginBottom: 20 },
  form: { backgroundColor: "#fff", borderRadius: 16, padding: 20, marginBottom: 16, elevation: 2 },
  label: { fontSize: 14, fontWeight: "500", color: "#374151", marginBottom: 6, marginTop: 8 },
  chipRow: { flexDirection: "row", flexWrap: "wrap", gap: 8, marginBottom: 8 },
  chip: { paddingHorizontal: 14, paddingVertical: 8, borderRadius: 20, backgroundColor: "#F3F4F6", borderWidth: 1, borderColor: "#D1D5DB" },
  chipActive: { backgroundColor: "#2D6A4F", borderColor: "#2D6A4F" },
  chipText: { color: "#6B7280" },
  chipTextActive: { color: "#fff" },
  inputRow: { flexDirection: "row", gap: 12 },
  halfInput: { flex: 1 },
  input: { backgroundColor: "#F9FAFB", borderRadius: 10, padding: 12, fontSize: 15, borderWidth: 1, borderColor: "#E5E7EB" },
  button: { backgroundColor: "#2D6A4F", borderRadius: 12, padding: 16, alignItems: "center", marginTop: 16 },
  buttonText: { color: "#fff", fontSize: 18, fontWeight: "600" },
  resultCard: { backgroundColor: "#fff", borderRadius: 16, padding: 20, marginBottom: 12, elevation: 2 },
  resultHeader: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginBottom: 12 },
  cropName: { fontSize: 20, fontWeight: "bold", color: "#111827", flex: 1 },
  riskBadge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 12, color: "#fff", fontSize: 12, fontWeight: "600", overflow: "hidden" },
  metrics: { gap: 4 },
  metric: { fontSize: 14, color: "#6B7280" },
  tip: { fontSize: 13, color: "#374151", marginTop: 8, fontStyle: "italic" },
});
