import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { ActivityIndicator, View } from "react-native";
import { useAuth } from "../context/AuthContext";

import LoginScreen from "../screens/LoginScreen";
import SignupScreen from "../screens/SignupScreen";
import DashboardScreen from "../screens/DashboardScreen";
import DiseaseDetectionScreen from "../screens/DiseaseDetectionScreen";
import ChatbotScreen from "../screens/ChatbotScreen";
import VoiceAssistantScreen from "../screens/VoiceAssistantScreen";
import WeatherScreen from "../screens/WeatherScreen";
import CropRecommendationScreen from "../screens/CropRecommendationScreen";
import YieldPredictionScreen from "../screens/YieldPredictionScreen";
import ProfileScreen from "../screens/ProfileScreen";

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

function AuthStack() {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="Login" component={LoginScreen} />
      <Stack.Screen name="Signup" component={SignupScreen} />
    </Stack.Navigator>
  );
}

function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={{
        headerStyle: { backgroundColor: "#2D6A4F" },
        headerTintColor: "#fff",
        tabBarActiveTintColor: "#2D6A4F",
        tabBarInactiveTintColor: "#9CA3AF",
        tabBarStyle: { backgroundColor: "#fff", borderTopWidth: 0, elevation: 8, paddingBottom: 4, height: 60 },
        tabBarLabelStyle: { fontSize: 11, fontWeight: "500" },
      }}
    >
      <Tab.Screen name="Dashboard" component={DashboardScreen} options={{ tabBarIcon: () => null, tabBarLabel: "🏠" }} />
      <Tab.Screen name="DiseaseDetection" component={DiseaseDetectionScreen} options={{ title: "Disease Detection", tabBarLabel: "🔬" }} />
      <Tab.Screen name="Chatbot" component={ChatbotScreen} options={{ title: "AI Chatbot", tabBarLabel: "🤖" }} />
      <Tab.Screen name="Weather" component={WeatherScreen} options={{ title: "Weather", tabBarLabel: "🌤️" }} />
      <Tab.Screen name="Profile" component={ProfileScreen} options={{ tabBarLabel: "👤" }} />
    </Tab.Navigator>
  );
}

const AdditionalScreens = () => (
  <Stack.Navigator screenOptions={{ headerStyle: { backgroundColor: "#2D6A4F" }, headerTintColor: "#fff" }}>
    <Stack.Screen name="Main" component={MainTabs} options={{ headerShown: false }} />
    <Stack.Screen name="VoiceAssistant" component={VoiceAssistantScreen} options={{ title: "Voice Assistant" }} />
    <Stack.Screen name="CropRecommendation" component={CropRecommendationScreen} options={{ title: "Crop Recommendations" }} />
    <Stack.Screen name="YieldPrediction" component={YieldPredictionScreen} options={{ title: "Yield Prediction" }} />
  </Stack.Navigator>
);

export default function AppNavigator() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <View style={{ flex: 1, justifyContent: "center", alignItems: "center", backgroundColor: "#F0FDF4" }}>
        <ActivityIndicator size="large" color="#2D6A4F" />
      </View>
    );
  }

  return (
    <NavigationContainer>
      {isAuthenticated ? <AdditionalScreens /> : <AuthStack />}
    </NavigationContainer>
  );
}
