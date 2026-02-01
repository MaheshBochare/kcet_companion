import { useState } from "react";

export function useFilters(setPage) {
  const [college, setCollege] = useState("");
  const [branch, setBranch] = useState("");
  const [category, setCategory] = useState("");
  const [round, setRound] = useState("");
  const [year, setYear] = useState("");
  const [showFilters, setShowFilters] = useState(true);

  const resetPage = () => setPage(1);

  const handleChange = (setter) => (e) => {
    setter(e.target.value);
    resetPage();
  };

  const toggleFilters = () => {
    setShowFilters((prev) => !prev);
  };

  /* ---------- NEW: Clear All Filters ---------- */
  const clearAllFilters = () => {
    setCollege("");
    setBranch("");
    setCategory("");
    setRound("");
    setYear("");
    resetPage();
  };

  return {
    /* values */
    college,
    branch,
    category,
    round,
    year,
    showFilters,

    /* setters (still exposed if needed) */
    setCollege,
    setBranch,
    setCategory,
    setRound,
    setYear,

    /* handlers */
    handleChange,
    toggleFilters,
    clearAllFilters,
  };
}
