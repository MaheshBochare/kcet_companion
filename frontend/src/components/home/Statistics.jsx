import { useEffect, useState } from "react";
import { api } from "../../api/client";

export default function Statistics() {
  const [stats, setStats] = useState([]);

  useEffect(() => {
    api.get("/key-statistics/")
      .then(res => setStats(res.data.overview))
      .catch(console.error);
  }, []);

  return (
    <div className="horizontal-card">
      <h4>Statistics</h4>
      {stats.map((s, i) => (
        <div key={i} className="mb-2">
          <div className="fw-bold">{s.value}</div>
          <div className="text-muted small">{s.name}</div>
        </div>
      ))}
    </div>
  );
}
