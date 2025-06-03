import api from "../services/api";

export const transformRequest = async (
  path,
  method,
  body = null,
  token = "",
  header = "application/json"
) => {
  try {
    const config = {
      method,
      url: path,
      headers: {
        "Content-Type": header,
      },
    };
    if (token && typeof token === "string") {
      token = token.replace(/"/g, "");
      config.headers.Authorization = `Bearer ${token}`;
    }

    if (method !== "GET" && method !== "HEAD" && body !== null) {
      config.data = body;
    }
    const response = await api(config);
    return response.data;
  } catch (error) {
    console.error("Erro na requisição:", error);
    throw error;
  }
};
