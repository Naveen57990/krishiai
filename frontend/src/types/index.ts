export interface User {
  id: number;
  email: string;
  full_name: string;
  phone?: string;
  role: string;
  preferred_language: string;
  location?: string;
  farm_size?: number;
  soil_type?: string;
  is_active: boolean;
  is_verified: boolean;
  profile_image_url?: string;
  created_at: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface SignupRequest {
  email: string;
  password: string;
  full_name: string;
  phone?: string;
  preferred_language?: string;
}

export interface DiseaseReport {
  id: number;
  farmer_id: number;
  crop_name?: string;
  disease_name?: string;
  confidence_score?: number;
  image_url?: string;
  treatment_recommended?: string;
  organic_treatment?: string;
  chemical_treatment?: string;
  severity?: string;
  is_resolved: boolean;
  notes?: string;
  created_at: string;
}

export interface ChatMessage {
  id: number;
  message: string;
  response: string;
  language: string;
  created_at: string;
}

export interface ChatSession {
  session_id: string;
  message_count: number;
  last_activity: string;
}

export interface WeatherData {
  location: string;
  temperature: number;
  feels_like: number;
  humidity: number;
  wind_speed: number;
  weather_condition: string;
  weather_description: string;
  weather_icon: string;
  rainfall_mm?: number;
  uv_index?: number;
  recorded_at: string;
}

export interface WeatherForecast {
  date: string;
  temp_min: number;
  temp_max: number;
  humidity: number;
  condition: string;
  icon: string;
  wind_speed: number;
  rainfall?: number;
}

export interface CropSuggestion {
  crop_name: string;
  crop_name_te?: string;
  crop_name_hi?: string;
  confidence_score: number;
  suitability_score: number;
  expected_yield_per_hectare?: number;
  profitability_estimate?: number;
  risk_score: number;
  risk_factors?: Record<string, any>;
  farming_tips?: Record<string, any>;
  growing_period_days?: number;
}

export interface YieldPrediction {
  id: number;
  crop_name: string;
  area_hectares: number;
  predicted_yield_kg?: number;
  predicted_yield_per_hectare?: number;
  confidence_interval_lower?: number;
  confidence_interval_upper?: number;
  weather_impact_score?: number;
  recommendations?: Record<string, any>;
  created_at: string;
}

export type Language = "en" | "te" | "hi";

export interface VoiceSession {
  transcript: string;
  translated_text?: string;
  response_text: string;
  response_audio_url?: string;
  session_id: string;
}
