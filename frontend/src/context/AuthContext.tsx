import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { User, AuthTokens } from "../types";
import { auth as authApi } from "../services/api";

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (data: any) => Promise<void>;
  logout: () => Promise<void>;
  updateUser: (data: Partial<User>) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadUser();
  }, []);

  const loadUser = async () => {
    try {
      const token = await AsyncStorage.getItem("access_token");
      if (token) {
        const { data } = await authApi.getProfile();
        setUser(data);
      }
    } catch {
      await AsyncStorage.multiRemove(["access_token", "refresh_token", "user"]);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    const { data: tokens } = await authApi.login({ email, password });
    await AsyncStorage.setItem("access_token", tokens.access_token);
    await AsyncStorage.setItem("refresh_token", tokens.refresh_token);
    const { data: userData } = await authApi.getProfile();
    setUser(userData);
  };

  const signup = async (signupData: any) => {
    await authApi.signup(signupData);
  };

  const logout = async () => {
    await AsyncStorage.multiRemove(["access_token", "refresh_token", "user"]);
    setUser(null);
  };

  const updateUser = (data: Partial<User>) => {
    if (user) setUser({ ...user, ...data });
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: !!user,
        login,
        signup,
        logout,
        updateUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
};
