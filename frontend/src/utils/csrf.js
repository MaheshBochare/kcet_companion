import api from "../api/axios";

export async function getCSRFToken() {
  const res = await api.get("csrf/");
  return res.data.csrfToken;
}
