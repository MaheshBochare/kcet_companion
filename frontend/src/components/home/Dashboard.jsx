import React from "react";
import HomeActions from "./HomeActions";

export default function Dashboard({ quickLinks, stats, featured }) {
  return (
    <main className="container">
      {/* ---------- DASHBOARD CARDS ---------- */}
      <div className="horizontal-cards">

        {/* Quick Links */}
        <div className="horizontal-card">
          <h4>Quick Links</h4>
          <div className="quick-links">
            {quickLinks?.map((l, i) => (
              <a key={i} href={l.url} className="quick-link-item">
                {l.title}
              </a>
            ))}
          </div>
        </div>

        {/* Statistics */}
        <div className="horizontal-card">
          <h4>Statistics</h4>
          {stats?.map((s, i) => (
            <div key={i} className="stat-item">
              <div className="stat-value">{s.value}</div>
              <div className="stat-name">{s.name}</div>
            </div>
          ))}
        </div>

        {/* Featured Colleges */}
        <div className="horizontal-card">
          <h4>Featured Colleges</h4>
          {featured?.map((c, i) => (
            <div key={i} className="featured-item">
              <h6>{c.name}</h6>
              <p>{c.location}</p>
            </div>
          ))}
        </div>

      </div>

      {/* ---------- ACTION BUTTONS BELOW ---------- */}
      <HomeActions />
    </main>
  );
}
