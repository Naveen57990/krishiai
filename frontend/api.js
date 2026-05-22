// KrishiAI — API Client
const API_BASE = localStorage.getItem('krishi_api_base') || 'https://krishiai-backend.onrender.com/api/v1';
const REQUEST_TIMEOUT = 15000;

const api = {
  async request(endpoint, options = {}) {
    const token = localStorage.getItem('krishi_token');
    const headers = { 'Content-Type': 'application/json', ...options.headers };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT);
    try {
      var res = await fetch(`${API_BASE}${endpoint}`, { ...options, headers, signal: controller.signal });
    } catch (e) {
      clearTimeout(timeout);
      if (e.name === 'AbortError') throw new Error('Request timed out. Check your connection.');
      throw new Error('Network error. Please check your connection.');
    }
    clearTimeout(timeout);
    if (res.status === 401 && token) {
      const refresh = localStorage.getItem('krishi_refresh');
      if (refresh) {
        const r = await fetch(`${API_BASE}/auth/refresh`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ refresh_token: refresh }),
        });
        if (r.ok) {
          const d = await r.json();
          localStorage.setItem('krishi_token', d.access_token);
          localStorage.setItem('krishi_refresh', d.refresh_token);
          headers['Authorization'] = `Bearer ${d.access_token}`;
          const retry = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
          return retry.json();
        }
        localStorage.removeItem('krishi_token');
        localStorage.removeItem('krishi_refresh');
        window.location = '/auth.html';
      }
    }
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || 'Request failed');
    }
    return res.json();
  },

  // Auth
  async signup(data) {
    const res = await this.request('/auth/signup', { method: 'POST', body: JSON.stringify(data) });
    return res;
  },
  async login(data) {
    const res = await this.request('/auth/login', { method: 'POST', body: JSON.stringify(data) });
    localStorage.setItem('krishi_token', res.access_token);
    localStorage.setItem('krishi_refresh', res.refresh_token);
    localStorage.setItem('krishi_token_expiry', Date.now() + res.expires_in * 1000);
    return res;
  },
  async getProfile() { return this.request('/auth/me'); },
  async updateProfile(data) { return this.request('/auth/me', { method: 'PUT', body: JSON.stringify(data) }); },
  async changePassword(data) { return this.request('/auth/change-password', { method: 'POST', body: JSON.stringify(data) }); },
  logout() {
    localStorage.removeItem('krishi_token');
    localStorage.removeItem('krishi_refresh');
    localStorage.removeItem('krishi_token_expiry');
    localStorage.removeItem('krishi_user');
    window.location = '/auth.html';
  },

  // Disease
  async detectDisease(formData) {
    const token = localStorage.getItem('krishi_token');
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const res = await fetch(`${API_BASE}/disease/detect`, { method: 'POST', body: formData, headers });
    if (!res.ok) throw new Error((await res.json()).detail);
    return res.json();
  },
  async getDiseaseReports(skip = 0, limit = 20) { return this.request(`/disease/reports?skip=${skip}&limit=${limit}`); },
  async getDiseaseReport(id) { return this.request(`/disease/reports/${id}`); },
  async updateDiseaseReport(id, data) { return this.request(`/disease/reports/${id}`, { method: 'PUT', body: JSON.stringify(data) }); },
  async deleteDiseaseReport(id) { return this.request(`/disease/reports/${id}`, { method: 'DELETE' }); },

  // Chatbot
  async chat(data) { return this.request('/chatbot/chat', { method: 'POST', body: JSON.stringify(data) }); },
  async anonymousChat(data) { return this.request('/chatbot/anonymous', { method: 'POST', body: JSON.stringify(data) }); },
  async getChatHistory(sessionId) { return this.request(`/chatbot/history/${sessionId}`); },
  async getChatSessions() { return this.request('/chatbot/sessions'); },

  // Voice
  async processVoice(formData) {
    const token = localStorage.getItem('krishi_token');
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const res = await fetch(`${API_BASE}/voice/process`, { method: 'POST', body: formData, headers });
    if (!res.ok) throw new Error((await res.json()).detail);
    return res.json();
  },
  async tts(data) { return this.request('/voice/tts', { method: 'POST', body: JSON.stringify(data) }); },
  async getVoiceHistory() { return this.request('/voice/history'); },

  // Weather
  async getWeather(location) { return this.request(`/weather/current?location=${encodeURIComponent(location)}`); },
  async getForecast(location, days = 5) { return this.request(`/weather/forecast?location=${encodeURIComponent(location)}&days=${days}`); },
  async getFarmingAdvice(location) { return this.request(`/weather/farming-advice?location=${encodeURIComponent(location)}`); },

  // Recommendations
  async getCropRecommendations(data) { return this.request('/recommendations/crop', { method: 'POST', body: JSON.stringify(data) }); },
  async getRecommendationHistory() { return this.request('/recommendations/history'); },

  // Yield
  async predictYield(data) { return this.request('/yield/predict', { method: 'POST', body: JSON.stringify(data) }); },
  async getYieldHistory() { return this.request('/yield/history'); },
  async getYieldPrediction(id) { return this.request(`/yield/${id}`); },

  // Memory
  async storeMemory(data) { return this.request('/memory/store', { method: 'POST', body: JSON.stringify(data) }); },
  async getMemoriesByType(type) { return this.request(`/memory/type/${type}`); },
  async getUserContext() { return this.request('/memory/context'); },
  async deleteMemory(id) { return this.request(`/memory/${id}`, { method: 'DELETE' }); },

  // Health
  async health() { return this.request('/health'); },
};
