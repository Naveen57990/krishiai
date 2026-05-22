import React, { useState } from "react";
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ScrollView, Alert, ActivityIndicator } from "react-native";
import { useAuth } from "../context/AuthContext";
import { useTranslation } from "../context/LanguageContext";
import { auth as authApi } from "../services/api";

export default function ProfileScreen() {
  const { user, logout, updateUser } = useAuth();
  const { t, language, setLanguage } = useTranslation();
  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState({
    full_name: user?.full_name || "",
    phone: user?.phone || "",
    location: user?.location || "",
    farm_size: user?.farm_size?.toString() || "",
    soil_type: user?.soil_type || "",
  });
  const [loading, setLoading] = useState(false);

  const handleSave = async () => {
    setLoading(true);
    try {
      const { data } = await authApi.updateProfile(form);
      updateUser(data);
      setEditing(false);
      Alert.alert(t("success"), "Profile updated");
    } catch (err: any) {
      Alert.alert(t("error"), err.response?.data?.detail || "Update failed");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    Alert.alert("Logout", "Are you sure?", [
      { text: "Cancel", style: "cancel" },
      { text: "Logout", style: "destructive", onPress: logout },
    ]);
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>{user?.full_name?.[0]?.toUpperCase() || "F"}</Text>
        </View>
        <Text style={styles.name}>{user?.full_name}</Text>
        <Text style={styles.email}>{user?.email}</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Language</Text>
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
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>{t("profile")}</Text>
        <TextInput style={styles.input} label="Full Name" value={form.full_name} onChangeText={(v) => setForm({ ...form, full_name: v })} editable={editing} placeholder="Full Name" />
        <TextInput style={styles.input} value={form.phone} onChangeText={(v) => setForm({ ...form, phone: v })} editable={editing} placeholder="Phone" keyboardType="phone-pad" />
        <TextInput style={styles.input} value={form.location} onChangeText={(v) => setForm({ ...form, location: v })} editable={editing} placeholder="Location" />
        <TextInput style={styles.input} value={form.farm_size} onChangeText={(v) => setForm({ ...form, farm_size: v })} editable={editing} placeholder="Farm Size (ha)" keyboardType="decimal-pad" />
        <TextInput style={styles.input} value={form.soil_type} onChangeText={(v) => setForm({ ...form, soil_type: v })} editable={editing} placeholder="Soil Type" />

        {editing ? (
          <View style={styles.editRow}>
            <TouchableOpacity style={styles.cancelBtn} onPress={() => setEditing(false)}>
              <Text style={styles.cancelText}>{t("cancel")}</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.saveBtn} onPress={handleSave} disabled={loading}>
              {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.saveText}>{t("save")}</Text>}
            </TouchableOpacity>
          </View>
        ) : (
          <TouchableOpacity style={styles.editBtn} onPress={() => setEditing(true)}>
            <Text style={styles.editBtnText}>Edit Profile</Text>
          </TouchableOpacity>
        )}
      </View>

      <TouchableOpacity style={styles.logoutBtn} onPress={handleLogout}>
        <Text style={styles.logoutText}>{t("logout")}</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F0FDF4" },
  header: { backgroundColor: "#2D6A4F", padding: 32, alignItems: "center" },
  avatar: { width: 80, height: 80, borderRadius: 40, backgroundColor: "#A7F3D0", justifyContent: "center", alignItems: "center", marginBottom: 12 },
  avatarText: { fontSize: 36, fontWeight: "bold", color: "#2D6A4F" },
  name: { fontSize: 24, fontWeight: "bold", color: "#fff" },
  email: { fontSize: 14, color: "#A7F3D0", marginTop: 4 },
  section: { backgroundColor: "#fff", margin: 16, borderRadius: 16, padding: 20, elevation: 2 },
  sectionTitle: { fontSize: 18, fontWeight: "600", color: "#374151", marginBottom: 12 },
  langRow: { flexDirection: "row", gap: 8 },
  langBtn: { paddingHorizontal: 16, paddingVertical: 8, borderRadius: 20, backgroundColor: "#F3F4F6" },
  langBtnActive: { backgroundColor: "#2D6A4F" },
  langText: { color: "#6B7280" },
  langTextActive: { color: "#fff" },
  input: { backgroundColor: "#F9FAFB", borderRadius: 10, padding: 14, fontSize: 15, marginBottom: 12, borderWidth: 1, borderColor: "#E5E7EB" },
  editRow: { flexDirection: "row", gap: 12, marginTop: 8 },
  cancelBtn: { flex: 1, padding: 14, borderRadius: 10, borderWidth: 1, borderColor: "#D1D5DB", alignItems: "center" },
  cancelText: { color: "#6B7280", fontWeight: "600" },
  saveBtn: { flex: 1, backgroundColor: "#2D6A4F", padding: 14, borderRadius: 10, alignItems: "center" },
  saveText: { color: "#fff", fontWeight: "600" },
  editBtn: { backgroundColor: "#2D6A4F", padding: 14, borderRadius: 10, alignItems: "center", marginTop: 8 },
  editBtnText: { color: "#fff", fontWeight: "600" },
  logoutBtn: { marginHorizontal: 16, marginBottom: 32, padding: 16, borderRadius: 12, borderWidth: 1, borderColor: "#EF4444", alignItems: "center" },
  logoutText: { color: "#EF4444", fontWeight: "600", fontSize: 16 },
});
