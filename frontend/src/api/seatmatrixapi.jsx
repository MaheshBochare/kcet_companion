import { api } from "./client";

/**
 * Fetch cutoff ranks matrix
 * - Defaults to page 1
 * - Sends ONLY non-empty filters
 */
export const fetchSeatmatrix = ({
  page = 1,
  college,
  branch,
  category,
  round,
  year
} = {}) => {
  const params = { page };

  if (college?.trim()) params.college = college.trim();
  if (branch?.trim()) params.branch = branch.trim();
  if (category?.trim()) params.category = category.trim();
  if (round?.trim()) params.round = round.trim();
  if (year?.trim()) params.year = year.trim();

  // ✅ IMPORTANT: use api, NOT axios
  return api.get("/seatmatrix-table/", { params });
};
