import React, { useState } from "react";
import {
  View, Text, TextInput, TouchableOpacity, StyleSheet,
  ActivityIndicator, Alert, KeyboardAvoidingView, Platform, ScrollView,
} from "react-native";
import { useAuth } from "../context/AuthContext";
import { useTranslation } from "../context/LanguageContext";

export default function SignupScreen({ navigation }: any) {
  const { signup } = useAuth();
  const { t } = useTranslation();
  const [form, setForm] = useState({ email: "", password: "", full_name: "", phone: "" });
  const [loading, setLoading] = useState(false);

  const handleSignup = async () => {
    if (!form.email || !form.password || !form.full_name) {
      Alert.alert(t("error"), "Please fill all required fields");
      return;
    }
    if (form.password.length < 8) {
      Alert.alert(t("error"), "Password must be at least 8 characters");
      return;
    }
    setLoading(true);
    try {
      await signup(form);
      Alert.alert(t("success"), "Account created! Please login.", [
        { text: "OK", onPress: () => navigation.goBack() },
      ]);
    } catch (err: any) {
      Alert.alert(t("error"), err.response?.data?.detail || "Signup failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView style={styles.container} behavior={Platform.OS === "ios" ? "padding" : "height"}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <Text style={styles.title}>{t("signup")}</Text>

        <TextInput
          style={styles.input}
          placeholder={t("full_name")}
          value={form.full_name}
          onChangeText={(v) => setForm({ ...form, full_name: v })}
        />
        <TextInput
          style={styles.input}
          placeholder={t("email")}
          value={form.email}
          onChangeText={(v) => setForm({ ...form, email: v })}
          keyboardType="email-address"
          autoCapitalize="none"
        />
        <TextInput
          style={styles.input}
          placeholder={t("phone")}
          value={form.phone}
          onChangeText={(v) => setForm({ ...form, phone: v })}
          keyboardType="phone-pad"
        />
        <TextInput
          style={styles.input}
          placeholder={t("password")}
          value={form.password}
          onChangeText={(v) => setForm({ ...form, password: v })}
          secureTextEntry
        />

        <TouchableOpacity
          style={[styles.button, loading && styles.buttonDisabled]}
          onPress={handleSignup}
          disabled={loading}
        >
          {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>{t("signup")}</Text>}
        </TouchableOpacity>

        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Text style={styles.linkText}>{t("login")}</Text>
        </TouchableOpacity>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F0FDF4" },
  scrollContent: { flexGrow: 1, justifyContent: "center", padding: 24 },
  title: { fontSize: 28, fontWeight: "bold", color: "#2D6A4F", textAlign: "center", marginBottom: 32 },
  input: { backgroundColor: "#fff", borderRadius: 12, padding: 16, fontSize: 16, marginBottom: 16, borderWidth: 1, borderColor: "#D1D5DB" },
  button: { backgroundColor: "#2D6A4F", borderRadius: 12, padding: 16, alignItems: "center", marginTop: 8 },
  buttonDisabled: { opacity: 0.6 },
  buttonText: { color: "#fff", fontSize: 18, fontWeight: "600" },
  linkText: { color: "#2D6A4F", textAlign: "center", marginTop: 16, fontSize: 16 },
});
