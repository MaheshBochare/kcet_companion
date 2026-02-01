import { useEffect, useState } from "react";
import { api } from "../api/client";

export function useHomeData() {
  const [featured, setFeatured] = useState([]);
  const [stats, setStats] = useState([]);
  const [quickLinks, setQuickLinks] = useState([]);

  useEffect(() => {
    api.get("/featured-colleges/")
      .then(res => setFeatured(res.data?.featured_colleges || []))
      .catch(() => setFeatured([]));

    api.get("/key-statistics/")
      .then(res => setStats(res.data?.overview || []))
      .catch(() => setStats([]));

    api.get("/quick-links/")
      .then(res => setQuickLinks(res.data?.quick_links || []))
      .catch(() => setQuickLinks([]));
  }, []);

  return { featured, stats, quickLinks };
}
