export default function SearchResults({ results, query }) {
  if (!results || results.length === 0) return null;

  return (
    <section className="search-results">
      <h3>
        Search Results for "<span>{query}</span>"
      </h3>

      <div className="results-list">
        {results.map((r, i) => (
          <div key={i} className="result-card">
            <h4>{r.name}</h4>
            <p>{r.location}</p>

            <div className="result-meta">
              <span>NAAC: {r.naac || "N/A"}</span>
              <span>
                Fees: ₹{r.fees ? r.fees.toLocaleString() : "N/A"}
              </span>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
