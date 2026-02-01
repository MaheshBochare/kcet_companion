import { useId } from "react";

export default function SearchBox({
  query = "",
  setQuery = () => {},
  suggestions = [],
  results = [],
  loading = false,
  activeIndex = -1,
  handleKeyDown = () => {},
  onSearch = () => {},
}) {
  const inputId = useId();

  const hasSuggestions = suggestions.length > 0;
  const hasResults = results.length > 0;

  return (
    <div className="search-wrapper">
      {/* Accessible label */}
      <label htmlFor={inputId} className="sr-only">
        Search colleges
      </label>

      {/* Search Input */}
      <input
        id={inputId}
        name="collegeSearch"
        type="text"
        className="search-input"
        placeholder="Search colleges..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => {
          handleKeyDown(e);
          if (e.key === "Enter") onSearch();
        }}
        autoComplete="off"
        aria-expanded={hasSuggestions}
        aria-controls={`${inputId}-list`}
      />

      {/* Loader */}
      {loading && <div className="search-loader">Loading...</div>}

      {/* Suggestions dropdown */}
      {!loading && hasSuggestions && (
        <div
          className="search-box"
          id={`${inputId}-list`}
          role="listbox"
        >
          {suggestions.map((s, i) => (
            <div
              key={i}
              role="option"
              aria-selected={i === activeIndex}
              className={`search-item ${
                i === activeIndex ? "active" : ""
              }`}
              onMouseDown={() => {
                setQuery(s.name);
                onSearch(s);
              }}
            >
              <div className="college-name">{s.name}</div>
              <div className="college-sub">{s.location}</div>
            </div>
          ))}
        </div>
      )}

      {/* ================= SEARCH RESULTS ================= */}
      {!loading && query && hasResults && (
        <div className="search-results">
          <h4>
            Search Results for "<span>{query}</span>"
          </h4>

          <div className="results-list">
            {results.map((r, i) => (
              <div key={i} className="result-card">
                <h5 className="result-title">{r.name}</h5>
                <p className="result-location">📍 {r.location}</p>

                <div className="result-meta">
                  <span>🏆 NAAC: {r.naac || "N/A"}</span>
                  <span>💰 Fees: ₹{r.fees?.toLocaleString() || "N/A"}</span>
                  <span>
                    💼 Highest Package:{" "}
                    {r.highest_package
                      ? `₹${r.highest_package.toLocaleString()}`
                      : "N/A"}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* No results */}
      {!loading && query && !hasResults && (
        <p className="no-data">
          No colleges found for "{query}"
        </p>
      )}
    </div>
  );
}
