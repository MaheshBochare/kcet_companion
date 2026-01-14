import { api } from "./client";

export const fetchCutoffData = () => {
  return api.get("/cutoff-table/");
};
