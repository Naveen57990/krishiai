import axios, { AxiosInstance, InternalAxiosRequestConfig } from "axios";
import AsyncStorage from "@react-native-async-storage/async-storage";

const API_URL = process.env.EXPO_PUBLIC_API_URL || "http://localhost:8000/api/v1";

const api: AxiosInstance = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use(async (config: InternalAxiosRequestConfig) => {
  const token = await AsyncStorage.getItem("access_token");
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = await AsyncStorage.getItem("refresh_token");
        if (refreshToken) {
          const { data } = await axios.post(`${API_URL}/auth/refresh`, {
            refresh_token: refreshToken,
          });
          await AsyncStorage.setItem("access_token", data.access_token);
          await AsyncStorage.setItem("refresh_token", data.refresh_token);
          originalRequest.headers.Authorization = `Bearer ${data.access_token}`;
          return api(originalRequest);
        }
      } catch {
        await AsyncStorage.multiRemove(["access_token", "refresh_token", "user"]);
      }
    }
    return Promise.reject(error);
  }
);

export const auth = {
  signup: (data: any) => api.post("/auth/signup", data),
  login: (data: any) => api.post("/auth/login", data),
  refresh: (data: any) => api.post("/auth/refresh", data),
  getProfile: () => api.get("/auth/me"),
  updateProfile: (data: any) => api.put("/auth/me", data),
  changePassword: (data: any) => api.post("/auth/change-password", data),
};

export const disease = {
  detect: (formData: FormData) =>
    api.post("/disease/detect", formData, {
      headers: { "Content-Type": "multipart/form-data" },
      timeout: 60000,
    }),
  getReports: (skip = 0, limit = 20) =>
    api.get(`/disease/reports?skip=${skip}&limit=${limit}`),
  getReport: (id: number) => api.get(`/disease/reports/${id}`),
  updateReport: (id: number, data: any) => api.put(`/disease/reports/${id}`, data),
  deleteReport: (id: number) => api.delete(`/disease/reports/${id}`),
};

export const chatbot = {
  chat: (data: any) => api.post("/chatbot/chat", data),
  anonymousChat: (data: any) => api.post("/chatbot/anonymous", data),
  getHistory: (sessionId: string) => api.get(`/chatbot/history/${sessionId}`),
  getSessions: () => api.get("/chatbot/sessions"),
};

export const voice = {
  process: (formData: FormData) =>
    api.post("/voice/process", formData, {
      headers: { "Content-Type": "multipart/form-data" },
      timeout: 60000,
    }),
  tts: (data: any) => api.post("/voice/tts", data),
  getHistory: () => api.get("/voice/history"),
};

export const weather = {
  current: (location: string) => api.get(`/weather/current?location=${location}`),
  forecast: (location: string, days = 5) =>
    api.get(`/weather/forecast?location=${location}&days=${days}`),
  farmingAdvice: (location: string) =>
    api.get(`/weather/farming-advice?location=${location}`),
};

export const recommendations = {
  getCropRecommendations: (data: any) => api.post("/recommendations/crop", data),
  getHistory: () => api.get("/recommendations/history"),
};

export const yieldPrediction = {
  predict: (data: any) => api.post("/yield/predict", data),
  getHistory: () => api.get("/yield/history"),
  getById: (id: number) => api.get(`/yield/${id}`),
};

export const memory = {
  store: (data: any) => api.post("/memory/store", data),
  getByType: (type: string) => api.get(`/memory/type/${type}`),
  getContext: () => api.get("/memory/context"),
  delete: (id: number) => api.delete(`/memory/${id}`),
};

export default api;
