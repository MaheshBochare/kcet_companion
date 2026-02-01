import { useEffect, useState } from "react";
import { api } from "../api/client";

export function useSmartSearch(query) {
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);

  useEffect(() => {
    if (!query || query.trim().length < 2) {
      setSuggestions([]);
      setLoading(false);
      setActiveIndex(-1);
      return;
    }

    const controller = new AbortController();
    setLoading(true);

    const delay = setTimeout(() => {
      api
        .get(`/search/?q=${encodeURIComponent(query)}`, {
          signal: controller.signal,
        })
        .then(res => {
          setSuggestions(res.data?.results || []);
          setLoading(false);
        })
        .catch(err => {
          if (err.name !== "CanceledError") {
            setSuggestions([]);
            setLoading(false);
          }
        });
    }, 300);

    return () => {
      controller.abort();
      clearTimeout(delay);
    };
  }, [query]);

  return {
    suggestions,
    loading,
    activeIndex,
    setActiveIndex,
    setSuggestions,
  };
}
