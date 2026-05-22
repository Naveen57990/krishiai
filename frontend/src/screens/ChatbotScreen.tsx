import React, { useState, useRef } from "react";
import {
  View, Text, TextInput, TouchableOpacity, StyleSheet,
  FlatList, KeyboardAvoidingView, Platform, ActivityIndicator,
} from "react-native";
import { useTranslation } from "../context/LanguageContext";
import { chatbot as chatbotApi } from "../services/api";
import { useAuth } from "../context/AuthContext";

interface Message {
  id: string;
  text: string;
  isUser: boolean;
}

export default function ChatbotScreen() {
  const { t, language } = useTranslation();
  const { isAuthenticated } = useAuth();
  const [messages, setMessages] = useState<Message[]>([
    { id: "0", text: getGreeting(language), isUser: false },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState(() => Math.random().toString(36).substring(7));
  const flatListRef = useRef<FlatList>(null);

  function getGreeting(lang: string) {
    if (lang === "te") return "నమస్కారం! నేను కృషిఎఐ వ్యవసాయ సహాయకుడిని. మీరు ఏమి తెలుసుకోవాలనుకుంటున్నారు?";
    if (lang === "hi") return "नमस्ते! मैं कृशिऐ कृषि सहायक हूं। आप क्या जानना चाहते हैं?";
    return "Hello! I'm KrishiAI farming assistant. How can I help you today?";
  }

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg: Message = { id: Date.now().toString(), text: input, isUser: true };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const apiCall = isAuthenticated ? chatbotApi.chat : chatbotApi.anonymousChat;
      const { data } = await apiCall({
        message: input,
        session_id: sessionId,
        language,
        include_weather: true,
      });
      const botMsg: Message = { id: (Date.now() + 1).toString(), text: data.response, isUser: false };
      setMessages((prev) => [...prev, botMsg]);
    } catch {
      const errMsg: Message = {
        id: (Date.now() + 1).toString(),
        text: "Sorry, I couldn't process your request. Please try again.",
        isUser: false,
      };
      setMessages((prev) => [...prev, errMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
      keyboardVerticalOffset={90}
    >
      <FlatList
        ref={flatListRef}
        data={messages}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <View style={[styles.messageRow, item.isUser ? styles.userRow : styles.botRow]}>
            <View style={[styles.messageBubble, item.isUser ? styles.userBubble : styles.botBubble]}>
              <Text style={[styles.messageText, item.isUser ? styles.userText : styles.botText]}>
                {item.text}
              </Text>
            </View>
          </View>
        )}
        contentContainerStyle={styles.messageList}
        onContentSizeChange={() => flatListRef.current?.scrollToEnd()}
      />
      {loading && <ActivityIndicator style={styles.loading} color="#2D6A4F" />}
      <View style={styles.inputRow}>
        <TextInput
          style={styles.input}
          value={input}
          onChangeText={setInput}
          placeholder={t("start_chat")}
          placeholderTextColor="#9CA3AF"
          multiline
        />
        <TouchableOpacity style={styles.sendBtn} onPress={sendMessage} disabled={loading}>
          <Text style={styles.sendBtnText}>Send</Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F0FDF4" },
  messageList: { padding: 16, paddingBottom: 8 },
  messageRow: { marginBottom: 12 },
  userRow: { alignItems: "flex-end" },
  botRow: { alignItems: "flex-start" },
  messageBubble: { maxWidth: "80%", borderRadius: 16, padding: 12 },
  userBubble: { backgroundColor: "#2D6A4F", borderBottomRightRadius: 4 },
  botBubble: { backgroundColor: "#fff", borderBottomLeftRadius: 4, elevation: 1 },
  messageText: { fontSize: 15, lineHeight: 22 },
  userText: { color: "#fff" },
  botText: { color: "#374151" },
  loading: { marginBottom: 8 },
  inputRow: { flexDirection: "row", padding: 12, backgroundColor: "#fff", borderTopWidth: 1, borderTopColor: "#E5E7EB" },
  input: { flex: 1, backgroundColor: "#F9FAFB", borderRadius: 24, paddingHorizontal: 16, paddingVertical: 10, fontSize: 15, maxHeight: 80, marginRight: 8 },
  sendBtn: { backgroundColor: "#2D6A4F", borderRadius: 24, paddingHorizontal: 20, justifyContent: "center" },
  sendBtnText: { color: "#fff", fontWeight: "600" },
});
