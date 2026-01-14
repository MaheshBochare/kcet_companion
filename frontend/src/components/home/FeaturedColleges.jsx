import { useEffect, useState } from "react";
import { api } from "../../api/client";

export default function FeaturedColleges() {
  const [colleges, setColleges] = useState([]);

  useEffect(() => {
    api.get("/featured-colleges/")
      .then(res => setColleges(res.data.featured_colleges))
      .catch(console.error);
  }, []);

  return (
    <div className="horizontal-card">
      <h4>Featured Colleges</h4>
      {colleges.map((c, i) => (
        <div key={i} className="mt-2">
          <h6 className="fw-bold">{c.name}</h6>
          <p className="text-muted small mb-1">
            {c.location} • NAAC {c.naac}
          </p>
          <p className="text-success fw-semibold">
            Highest Package: ₹{(c.highest_package / 100000).toFixed(1)} LPA
          </p>
        </div>
      ))}
    </div>
  );
}
