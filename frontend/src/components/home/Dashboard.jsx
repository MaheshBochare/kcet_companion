export default function HomeDashboard() {
  return (
    <div className="horizontal-cards">
      <div className="horizontal-card"><h4>featured_colleges</h4></div>
    <div className="horizontal-card">
    <h4><i className="fas fa-chart-pie text-primary me-2"></i>Statistics</h4>
    {stats.map((s, i) => (
        <div key={i} className="mb-2">
        <div className="fw-bold">{s.value}</div>
        <div className="text-muted small">{s.name}</div>
        </div>
    ))}
    </div>
    <div className="horizontal-card">
    <h4><i className="fas fa-link text-primary me-2"></i>Quick Links</h4>

    <div className="quick-links">
        {quickLinks.map((l, i) => (
        <a
            key={i}
            href={l.url}
            target="_blank"
            rel="noopener noreferrer"
            className={`quick-link-item ${l.highlight ? "highlight" : ""}`}
        >
            <span className="quick-link-left">
            <i className={`fas ${l.icon}`}></i>
            <span>{l.title}</span>
            </span>
            <i className="fas fa-chevron-right"></i>
        </a>
        ))}
    </div>
    </div>



    </div>
  );
}
