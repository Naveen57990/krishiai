import React, { useState } from "react";
import {
  View, Text, TextInput, TouchableOpacity, StyleSheet,
  ActivityIndicator, Alert, KeyboardAvoidingView, Platform, ScrollView,
} from "react-native";
import { useAuth } from "../context/AuthContext";
import { useTranslation } from "../context/LanguageContext";

export default function LoginScreen({ navigation }: any) {
  const { login } = useAuth();
  const { t, language, setLanguage } = useTranslation();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    if (!email || !password) {
      Alert.alert(t("error"), "Please fill all fields");
      return;
    }
    setLoading(true);
    try {
      await login(email, password);
    } catch (err: any) {
      Alert.alert(t("error"), err.response?.data?.detail || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView style={styles.container} behavior={Platform.OS === "ios" ? "padding" : "height"}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <Text style={styles.title}>🌾 {t("app_name")}</Text>
        <Text style={styles.subtitle}>AI Agriculture Assistant</Text>

        <View style={styles.langRow}>
          {(["en", "te", "hi"] as const).map((lang) => (
            <TouchableOpacity
              key={lang}
              style={[styles.langBtn, language === lang && styles.langBtnActive]}
              onPress={() => setLanguage(lang)}
            >
              <Text style={[styles.langText, language === lang && styles.langTextActive]}>
                {lang === "en" ? "English" : lang === "te" ? "తెలుగు" : "हिन्दी"}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        <TextInput
          style={styles.input}
          placeholder={t("email")}
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
        />
        <TextInput
          style={styles.input}
          placeholder={t("password")}
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />

        <TouchableOpacity
          style={[styles.button, loading && styles.buttonDisabled]}
          onPress={handleLogin}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>{t("login")}</Text>
          )}
        </TouchableOpacity>

        <TouchableOpacity onPress={() => navigation.navigate("Signup")}>
          <Text style={styles.linkText}>
            {t("signup")}
          </Text>
        </TouchableOpacity>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F0FDF4" },
  scrollContent: { flexGrow: 1, justifyContent: "center", padding: 24 },
  title: { fontSize: 36, fontWeight: "bold", color: "#2D6A4F", textAlign: "center", marginBottom: 8 },
  subtitle: { fontSize: 16, color: "#6B7280", textAlign: "center", marginBottom: 32 },
  langRow: { flexDirection: "row", justifyContent: "center", marginBottom: 24, gap: 8 },
  langBtn: { paddingHorizontal: 16, paddingVertical: 8, borderRadius: 20, backgroundColor: "#E5E7EB" },
  langBtnActive: { backgroundColor: "#2D6A4F" },
  langText: { color: "#4B5563" },
  langTextActive: { color: "#fff" },
  input: { backgroundColor: "#fff", borderRadius: 12, padding: 16, fontSize: 16, marginBottom: 16, borderWidth: 1, borderColor: "#D1D5DB" },
  button: { backgroundColor: "#2D6A4F", borderRadius: 12, padding: 16, alignItems: "center", marginTop: 8 },
  buttonDisabled: { opacity: 0.6 },
  buttonText: { color: "#fff", fontSize: 18, fontWeight: "600" },
  linkText: { color: "#2D6A4F", textAlign: "center", marginTop: 16, fontSize: 16 },
});
