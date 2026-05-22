import React, { useState } from "react";
import {
  View, Text, TouchableOpacity, StyleSheet, Image, ActivityIndicator,
  Alert, ScrollView,
} from "react-native";
import * as ImagePicker from "expo-image-picker";
import { useTranslation } from "../context/LanguageContext";
import { disease as diseaseApi } from "../services/api";

export default function DiseaseDetectionScreen() {
  const { t, language } = useTranslation();
  const [image, setImage] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const pickImage = async (useCamera: boolean) => {
    const options: ImagePicker.ImagePickerOptions = {
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      quality: 0.8,
    };

    const result = useCamera
      ? await ImagePicker.launchCameraAsync(options)
      : await ImagePicker.launchImageLibraryAsync(options);

    if (!result.canceled) {
      setImage(result.assets[0].uri);
      setResult(null);
    }
  };

  const detectDisease = async () => {
    if (!image) return;
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("file", {
        uri: image,
        type: "image/jpeg",
        name: "plant.jpg",
      } as any);

      const { data } = await diseaseApi.detect(formData);
      setResult(data);
    } catch (err: any) {
      Alert.alert(t("error"), err.response?.data?.detail || "Detection failed");
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "high": return "#EF4444";
      case "medium": return "#F59E0B";
      case "low": return "#10B981";
      default: return "#6B7280";
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>🔬 {t("disease_detection")}</Text>

      <View style={styles.btnRow}>
        <TouchableOpacity style={styles.pickBtn} onPress={() => pickImage(true)}>
          <Text style={styles.pickBtnText}>📷 {t("camera")}</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.pickBtn} onPress={() => pickImage(false)}>
          <Text style={styles.pickBtnText}>🖼️ {t("gallery")}</Text>
        </TouchableOpacity>
      </View>

      {image && <Image source={{ uri: image }} style={styles.preview} />}

      {image && (
        <TouchableOpacity
          style={[styles.detectBtn, loading && { opacity: 0.6 }]}
          onPress={detectDisease}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.detectBtnText}>{t("detect")}</Text>
          )}
        </TouchableOpacity>
      )}

      {result && (
        <View style={styles.resultCard}>
          <View style={[styles.severityBadge, { backgroundColor: getSeverityColor(result.severity) }]}>
            <Text style={styles.severityText}>{result.severity?.toUpperCase()}</Text>
          </View>
          <Text style={styles.diseaseName}>{result.disease_name}</Text>
          {result.crop_name && <Text style={styles.cropName}>Crop: {result.crop_name}</Text>}
          <Text style={styles.confidence}>
            Confidence: {(result.confidence_score * 100).toFixed(1)}%
          </Text>
          {result.treatment_recommended && (
            <View style={styles.treatmentSection}>
              <Text style={styles.treatmentTitle}>Treatment:</Text>
              <Text style={styles.treatmentText}>{result.treatment_recommended}</Text>
            </View>
          )}
          {result.organic_treatment && (
            <View style={styles.treatmentSection}>
              <Text style={styles.treatmentTitle}>🌿 Organic:</Text>
              <Text style={styles.treatmentText}>{result.organic_treatment}</Text>
            </View>
          )}
          {result.chemical_treatment && (
            <View style={styles.treatmentSection}>
              <Text style={styles.treatmentTitle}>🧪 Chemical:</Text>
              <Text style={styles.treatmentText}>{result.chemical_treatment}</Text>
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
  btnRow: { flexDirection: "row", gap: 12, marginBottom: 16 },
  pickBtn: { flex: 1, backgroundColor: "#fff", borderRadius: 12, padding: 16, alignItems: "center", elevation: 2 },
  pickBtnText: { fontSize: 16, fontWeight: "500", color: "#374151" },
  preview: { width: "100%", height: 250, borderRadius: 12, marginBottom: 16 },
  detectBtn: { backgroundColor: "#2D6A4F", borderRadius: 12, padding: 16, alignItems: "center", marginBottom: 16 },
  detectBtnText: { color: "#fff", fontSize: 18, fontWeight: "600" },
  resultCard: { backgroundColor: "#fff", borderRadius: 16, padding: 20, elevation: 2 },
  severityBadge: { alignSelf: "flex-start", borderRadius: 8, paddingHorizontal: 12, paddingVertical: 4, marginBottom: 12 },
  severityText: { color: "#fff", fontWeight: "700", fontSize: 12 },
  diseaseName: { fontSize: 22, fontWeight: "bold", color: "#111827", marginBottom: 4 },
  cropName: { fontSize: 16, color: "#6B7280", marginBottom: 4 },
  confidence: { fontSize: 14, color: "#374151", marginBottom: 16 },
  treatmentSection: { marginTop: 12 },
  treatmentTitle: { fontSize: 16, fontWeight: "600", color: "#374151", marginBottom: 4 },
  treatmentText: { fontSize: 14, color: "#6B7280", lineHeight: 20 },
});
