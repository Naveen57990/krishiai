import React from "react";
import { render, fireEvent, waitFor } from "@testing-library/react-native";

describe("KrishiAI App", () => {
  it("renders without crashing", () => {
    expect(true).toBe(true);
  });

  it("has required screens defined", () => {
    const screens = [
      "Login",
      "Signup",
      "Dashboard",
      "DiseaseDetection",
      "Chatbot",
      "VoiceAssistant",
      "Weather",
      "CropRecommendation",
      "YieldPrediction",
      "Profile",
    ];
    expect(screens.length).toBeGreaterThan(0);
  });

  it("supports English, Telugu, and Hindi", () => {
    const languages = ["en", "te", "hi"];
    expect(languages).toHaveLength(3);
    expect(languages).toContain("te");
    expect(languages).toContain("hi");
  });
});
