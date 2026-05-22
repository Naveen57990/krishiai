import React, { useState } from "react";
import {
  View, Text, TouchableOpacity, StyleSheet, ActivityIndicator, Alert,
} from "react-native";
import { Audio } from "expo-av";
import * as DocumentPicker from "expo-document-picker";
import { useTranslation } from "../context/LanguageContext";
import { voice as voiceApi } from "../services/api";
import * as FileSystem from "expo-file-system";

export default function VoiceAssistantScreen() {
  const { t, language } = useTranslation();
  const [recording, setRecording] = useState<Audio.Recording | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const startRecording = async () => {
    try {
      await Audio.requestPermissionsAsync();
      await Audio.setAudioModeAsync({ allowsRecordingIOS: true, playsInSilentModeIOS: true });
      const { recording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY
      );
      setRecording(recording);
      setIsRecording(true);
    } catch (err) {
      Alert.alert("Error", "Failed to start recording");
    }
  };

  const stopRecording = async () => {
    if (!recording) return;
    setIsRecording(false);
    setLoading(true);
    try {
      await recording.stopAndUnloadAsync();
      const uri = recording.getURI();
      if (!uri) throw new Error("No recording URI");

      const formData = new FormData();
      formData.append("file", { uri, type: "audio/m4a", name: "voice.m4a" } as any);
      formData.append("session_id", Date.now().toString());
      formData.append("source_language", language === "en" ? "en" : "te");
      formData.append("target_language", "en");

      const { data } = await voiceApi.process(formData);
      setResult(data);
    } catch (err: any) {
      Alert.alert(t("error"), err.response?.data?.detail || "Processing failed");
    } finally {
      setRecording(null);
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>🎤 {t("voice_assistant")}</Text>

      <TouchableOpacity
        style={[styles.recordBtn, isRecording && styles.recordingActive]}
        onPress={isRecording ? stopRecording : startRecording}
        disabled={loading}
      >
        {loading ? (
          <ActivityIndicator size="large" color="#fff" />
        ) : (
          <Text style={styles.recordIcon}>{isRecording ? "⏹️" : "🎤"}</Text>
        )}
        <Text style={styles.recordText}>
          {isRecording ? "Stop Recording" : t("record_voice")}
        </Text>
      </TouchableOpacity>

      {result && (
        <View style={styles.resultCard}>
          <Text style={styles.label}>Transcript:</Text>
          <Text style={styles.text}>{result.transcript}</Text>
          {result.translated_text && (
            <>
              <Text style={styles.label}>Translated:</Text>
              <Text style={styles.text}>{result.translated_text}</Text>
            </>
          )}
          <Text style={styles.label}>Response:</Text>
          <Text style={styles.text}>{result.response_text}</Text>
          <Text style={styles.time}>Processing: {result.processing_time_ms}ms</Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F0FDF4", padding: 16 },
  title: { fontSize: 24, fontWeight: "bold", color: "#2D6A4F", marginBottom: 32 },
  recordBtn: { width: 160, height: 160, borderRadius: 80, backgroundColor: "#2D6A4F", justifyContent: "center", alignItems: "center", alignSelf: "center", marginBottom: 32 },
  recordingActive: { backgroundColor: "#EF4444" },
  recordIcon: { fontSize: 48 },
  recordText: { color: "#fff", marginTop: 8, fontSize: 14 },
  resultCard: { backgroundColor: "#fff", borderRadius: 16, padding: 20, elevation: 2 },
  label: { fontSize: 14, fontWeight: "600", color: "#374151", marginTop: 12, marginBottom: 4 },
  text: { fontSize: 15, color: "#6B7280", lineHeight: 22 },
  time: { fontSize: 12, color: "#9CA3AF", marginTop: 12 },
});
