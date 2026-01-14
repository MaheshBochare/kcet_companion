import { useEffect, useState } from "react";
import "../styles/home.css";
import { api } from "../api/client";
import Navbar from "../components/layout/navbar";

function highlight(text, query) {
  if (!query) return text;
  const regex = new RegExp(`(${query})`, "gi");
  return text.replace(regex, "<span class='highlight'>$1</span>");
}

export default function Home() {
  const [featured, setFeatured] = useState([]);
  const [stats, setStats] = useState([]);
  const [quickLinks, setQuickLinks] = useState([]);
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState([]);

  // ---------- Load Home Data ----------
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

  // ---------- Smart Search ----------
  useEffect(() => {
    if (query.length < 2) {
      setSuggestions([]);
      return;
    }

    const delay = setTimeout(() => {
      api.get(`/search/?q=${query}`)
        .then(res => setSuggestions(res.data.results || []))
        .catch(() => setSuggestions([]));
    }, 250);

    return () => clearTimeout(delay);
  }, [query]);



  return (
    <>
      <Navbar />

      <header className="main-header">
        <h1>Passion Meets Career!</h1>

        <div className="search-wrapper">
          <input
            className="form-control form-control-lg"
            placeholder="Search colleges..."
            value={query}
            onChange={e => setQuery(e.target.value)}
          />

          {suggestions.length > 0 && (
            <div className="search-box">
              {suggestions.map((s, i) => (
                <div key={i} className="search-item">
                  <div
                    className="fw-bold"
                    dangerouslySetInnerHTML={{
                      __html: highlight(s.college, query),
                    }}
                  />
                  <div className="text-muted small">{s.location}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </header>

      <main className="container">

        <div className="horizontal-cards">

          {/* Quick Links */}
          <div className="horizontal-card">
            <h4><i className="fas fa-link me-2"></i>Quick Links</h4>
            <div className="quick-links">
              {quickLinks.map((l, i) => (
                <a key={i} href={l.url} className="quick-link-item">
                  <span>{l.title}</span>
                  <i className={`fas ${l.icon || "fa-arrow-right"}`}></i>
                </a>
              ))}
            </div>
          </div>

          {/* Statistics */}
          <div className="horizontal-card">
            <h4><i className="fas fa-chart-pie me-2"></i>Statistics</h4>
            {stats.map((s, i) => (
              <div key={i} className="stat-item">
                <div className="stat-value">{s.value}</div>
                <div className="stat-name">{s.name}</div>
              </div>
            ))}
          </div>

          {/* Featured Colleges */}
          <div className="horizontal-card">
            <h4><i className="fas fa-university me-2"></i>Featured Colleges</h4>
            {featured.map((c, i) => (
              <div key={i} className="featured-item">
                <h6>{c.name}</h6>
                <p>{c.location}</p>
              </div>
            ))}
          </div>

        </div>

        <div className="action-buttons">
          <a href="/cutoff" className="btn btn-primary action-btn">
            <i className="fas fa-chart-line me-2"></i> Cutoff Analyzer
          </a>

          <a href="/seatmatrix" className="btn btn-primary action-btn">
            <i className="fas fa-chair me-2"></i> Seat Matrix
          </a>

          <a href="/predictor" className="btn btn-primary action-btn">
            <i className="fas fa-calculator me-2"></i> Predictor
          </a>
        </div>

      </main>

    </>
  );
}
