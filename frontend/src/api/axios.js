import axios from "axios";

// ✅ DEFINE api FIRST
const api = axios.create({
  baseURL: "http://localhost:8000/api/",
  withCredentials: true,
});

// ✅ THEN use it
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      try {
        await api.post("/token/refresh/");
        return api(error.config);
      } catch (err) {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

// ✅ EXPORT DEFAULT
export default api;
