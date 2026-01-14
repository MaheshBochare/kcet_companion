import { useEffect, useState } from "react";
import { api } from "../../api/client";

export default function QuickLinks() {
  const [links, setLinks] = useState([]);

  useEffect(() => {
    api.get("/quick-links/")
      .then(res => setLinks(res.data.quick_links))
      .catch(console.error);
  }, []);

  return (
    <div className="horizontal-card">
      <h4>Quick Links</h4>
      {links.map((l, i) => (
        <a key={i} href={l.url} className={`quick-link ${l.highlight ? "highlight" : ""}`} target="_blank">
          {l.title}
        </a>
      ))}
    </div>
  );
}
