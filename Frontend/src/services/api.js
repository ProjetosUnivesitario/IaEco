import axios from "axios";
import { getAccessToken } from "./auth";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

const excludedRoutes = [
  "/",
  "/auth_reset",
  "/api/v1/token/",
  "/api/v1/token/refresh/",
  "/api/v1/api/captcha/",
];

const isExcludedRoute = () => {
  const currentPath = window.location.pathname;
  return excludedRoutes.some((route) => currentPath.includes(route));
};

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (isExcludedRoute()) {
      return Promise.reject(error);
    }
    if (error.response.status === 401) {
      originalRequest._retry = true;
      try {
        const newAccessToken = await getAccessToken();
        if (!newAccessToken) {
          console.error("Erro ao renovar token: Nenhum novo token recebido.");
          return Promise.reject(error);
        }
        localStorage.setItem("access", newAccessToken);
        api.defaults.headers["Authorization"] = `Bearer ${newAccessToken}`;
        originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;

        return api(originalRequest);
      } catch (refreshError) {
        console.error("Falha ao renovar token:", refreshError);
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

api.interceptors.request.use(
  (config) => {
    if (isExcludedRoute()) {
      return config;
    }
    const token = localStorage.getItem("access");
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
