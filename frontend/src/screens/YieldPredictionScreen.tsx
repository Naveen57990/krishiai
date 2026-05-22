import React, { useState } from "react";
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ScrollView, ActivityIndicator, Alert } from "react-native";
import { useTranslation } from "../context/LanguageContext";
import { yieldPrediction as yieldApi } from "../services/api";

const CROPS = ["Rice", "Wheat", "Maize", "Sugarcane", "Cotton", "Groundnut", "Tomato", "Potato", "Chilli", "Onion"];

export default function YieldPredictionScreen() {
  const { t } = useTranslation();
  const [form, setForm] = useState({ crop_name: "", area_hectares: "", soil_type: "", ph_level: "", rainfall_mm: "", temperature: "" });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const predict = async () => {
    if (!form.crop_name || !form.area_hectares) {
      Alert.alert(t("error"), "Crop name and area are required");
      return;
    }
    setLoading(true);
    try {
      const { data } = await yieldApi.predict({
        crop_name: form.crop_name,
        area_hectares: parseFloat(form.area_hectares),
        soil_type: form.soil_type || "loam",
        ph_level: form.ph_level ? parseFloat(form.ph_level) : undefined,
        rainfall_mm: form.rainfall_mm ? parseFloat(form.rainfall_mm) : undefined,
        temperature: form.temperature ? parseFloat(form.temperature) : undefined,
      });
      setResult(data);
    } catch (err: any) {
      Alert.alert(t("error"), err.response?.data?.detail || "Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>📊 {t("yield_prediction")}</Text>

      <View style={styles.form}>
        <Text style={styles.label}>{t("crop_name")}</Text>
        <View style={styles.chipRow}>
          {CROPS.map((c) => (
            <TouchableOpacity
              key={c}
              style={[styles.chip, form.crop_name === c && styles.chipActive]}
              onPress={() => setForm({ ...form, crop_name: c })}
            >
              <Text style={[styles.chipText, form.crop_name === c && styles.chipTextActive]}>{c}</Text>
            </TouchableOpacity>
          ))}
        </View>

        <Text style={styles.label}>{t("area")}</Text>
        <TextInput style={styles.input} value={form.area_hectares} onChangeText={(v) => setForm({ ...form, area_hectares: v })} keyboardType="decimal-pad" placeholder="1.0" />

        <Text style={styles.label}>{t("soil_type")}</Text>
        <TextInput style={styles.input} value={form.soil_type} onChangeText={(v) => setForm({ ...form, soil_type: v })} placeholder="loam" />

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

        <TouchableOpacity style={styles.button} onPress={predict} disabled={loading}>
          {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>{t("predict_yield")}</Text>}
        </TouchableOpacity>
      </View>

      {result && (
        <View style={styles.resultCard}>
          <Text style={styles.resultTitle}>{result.crop_name} - Yield Prediction</Text>
          <View style={styles.resultRow}>
            <Text style={styles.resultLabel}>Predicted Yield:</Text>
            <Text style={styles.resultValue}>{result.predicted_yield_kg?.toLocaleString()} kg</Text>
          </View>
          <View style={styles.resultRow}>
            <Text style={styles.resultLabel}>Per Hectare:</Text>
            <Text style={styles.resultValue}>{result.predicted_yield_per_hectare?.toLocaleString()} kg/ha</Text>
          </View>
          <View style={styles.resultRow}>
            <Text style={styles.resultLabel}>Confidence Range:</Text>
            <Text style={styles.resultValue}>{result.confidence_interval_lower?.toLocaleString()} - {result.confidence_interval_upper?.toLocaleString()} kg</Text>
          </View>
          {result.weather_impact_score && (
            <View style={styles.resultRow}>
              <Text style={styles.resultLabel}>Weather Impact:</Text>
              <Text style={styles.resultValue}>{(result.weather_impact_score * 100).toFixed(0)}%</Text>
            </View>
          )}
          {result.recommendations && (
            <View style={styles.recSection}>
              <Text style={styles.recTitle}>Recommendations</Text>
              {Object.entries(result.recommendations).map(([key, val]: any) => (
                <Text key={key} style={styles.recText}>• {key.replace("_", " ")}: {val}</Text>
              ))}
            </View>
          )}
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F0FDF4", padding: 16 },
  title: { fontSize: 24, fontWeight: "bold", color: "#2D6A4F", marginBottom: 20 },
  form: { backgroundColor: "#fff", borderRadius: 16, padding: 20, marginBottom: 16, elevation: 2 },
  label: { fontSize: 14, fontWeight: "500", color: "#374151", marginBottom: 6, marginTop: 8 },
  chipRow: { flexDirection: "row", flexWrap: "wrap", gap: 6, marginBottom: 12 },
  chip: { paddingHorizontal: 12, paddingVertical: 6, borderRadius: 16, backgroundColor: "#F3F4F6", borderWidth: 1, borderColor: "#D1D5DB" },
  chipActive: { backgroundColor: "#2D6A4F" },
  chipText: { color: "#6B7280", fontSize: 13 },
  chipTextActive: { color: "#fff" },
  input: { backgroundColor: "#F9FAFB", borderRadius: 10, padding: 12, fontSize: 15, borderWidth: 1, borderColor: "#E5E7EB" },
  inputRow: { flexDirection: "row", gap: 12 },
  halfInput: { flex: 1 },
  button: { backgroundColor: "#2D6A4F", borderRadius: 12, padding: 16, alignItems: "center", marginTop: 16 },
  buttonText: { color: "#fff", fontSize: 18, fontWeight: "600" },
  resultCard: { backgroundColor: "#fff", borderRadius: 16, padding: 20, elevation: 2 },
  resultTitle: { fontSize: 20, fontWeight: "bold", color: "#2D6A4F", marginBottom: 16 },
  resultRow: { flexDirection: "row", justifyContent: "space-between", paddingVertical: 8, borderBottomWidth: 1, borderBottomColor: "#F3F4F6" },
  resultLabel: { fontSize: 15, color: "#6B7280" },
  resultValue: { fontSize: 15, fontWeight: "600", color: "#111827" },
  recSection: { marginTop: 16, backgroundColor: "#F0FDF4", padding: 12, borderRadius: 8 },
  recTitle: { fontSize: 16, fontWeight: "600", color: "#2D6A4F", marginBottom: 8 },
  recText: { fontSize: 13, color: "#374151", marginBottom: 4, lineHeight: 18 },
});
