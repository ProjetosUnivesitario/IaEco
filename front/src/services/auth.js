import axios from "axios";
import { signOut } from "../hooks/Auth";
import { cleanToken } from "../utils/cleanToken";

export const getAccessToken = async () => {
  const rawAccessToken = localStorage.getItem("access");
  if (!rawAccessToken) {
    console.error("Access token não encontrado!");
    signOut();
    throw new Error("Access token não encontrado!");
  }

  const accessToken = cleanToken(rawAccessToken);
  const verifyToken = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
  });

  try {
    const response = await verifyToken.post("/api/v1/token/verify/", {
      token: accessToken,
    });
    if (response.status === 200) {
      return accessToken;
    }
  } catch (error) {
    if (error.response && error.response.status === 401) {
      try {
        const newAccessToken = await refreshAccessToken();
        return newAccessToken;
      } catch (refreshError) {
        console.error("Falha ao renovar o token:", refreshError);
        signOut();
        throw new Error("Não foi possível renovar o token de acesso.");
      }
    } else {
      console.error("Erro ao verificar o token:", error);
      throw error;
    }
  }
};

export const refreshAccessToken = async () => {
  const rawRefreshToken = localStorage.getItem("refresh");

  if (!rawRefreshToken) {
    console.error("Refresh token não encontrado!");
    signOut();
    throw new Error("Refresh token não encontrado!");
  }

  const refreshToken = cleanToken(rawRefreshToken);
  const refreshApi = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
  });

  try {
    const response = await refreshApi.post("/api/v1/token/refresh/", {
      refresh: refreshToken,
    });
    if (response.data && response.data.access) {
      const newAccessToken = response.data.access;
      localStorage.setItem("access", newAccessToken);
      return newAccessToken;
    }
  } catch (error) {
    if (error.response && [401, 403].includes(error.response.status)) {
      signOut();
      throw new Error("Access token inválido!");
    }
  }
};
