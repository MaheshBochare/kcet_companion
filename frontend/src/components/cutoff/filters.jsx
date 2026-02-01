export default function Filters({
  college,
  branch,
  category,
  round,
  year,
  showFilters,
  handleChange,
  toggleFilters,
  clearAllFilters,
  setCollege,
  setBranch,
  setCategory,
  setRound,
  setYear,
}) {
  return (
    <div className="filters-section">

      {/* ===== APPLY FILTERS HEADER (FULL WIDTH CLICKABLE) ===== */}
      <div
        className="filter-header clickable"
        onClick={toggleFilters}
        role="button"
        aria-expanded={showFilters}
      >
        <h4>{showFilters ? "▲" : "▼"} Apply Filters</h4>

        <div className="filter-actions" onClick={(e) => e.stopPropagation()}>
          <button
            className="filter-clear-btn"
            onClick={clearAllFilters}
            type="button"
          >
            Clear All
          </button>

          <span className="filter-toggle-indicator">
            {showFilters ? "▲" : "▼"}
          </span>
        </div>
      </div>

      {/* ===== FILTER BODY (TOGGLED) ===== */}
      {showFilters && (
        <div className="filter-container open">
          <div className="filters-row">

            <input
              className="filter-input"
              placeholder="College Code (E021)"
              value={college}
              onChange={handleChange(setCollege)}
            />

            <input
              className="filter-input"
              placeholder="Branch (CSE)"
              value={branch}
              onChange={handleChange(setBranch)}
            />

            <select
              className="filter-select"
              value={category}
              onChange={handleChange(setCategory)}
            >
              <option value="">All Categories</option>
              <option value="GM">GM</option>
              <option value="SCG">SC</option>
              <option value="STG">ST</option>
            </select>

            <select
              className="filter-select"
              value={round}
              onChange={handleChange(setRound)}
            >
              <option value="">All Rounds</option>
              <option value="1gen">Round 1</option>
              <option value="2gen">Round 2</option>
              <option value="2ext">Extended</option>
            </select>

            <select
              className="filter-select"
              value={year}
              onChange={handleChange(setYear)}
            >
              <option value="">All Years</option>
              <option value="24">2024</option>
              <option value="23">2023</option>
              <option value="22">2022</option>
              <option value="21">2021</option>
            </select>
                        {/* ===== CLEAR ALL (ALIGNED WITH FILTERS) ===== */}
            <button
              type="button"
              className="filter-clear-btn inline"
              onClick={clearAllFilters}
            >
              Clear All
            </button>

          </div>
        </div>
      )}
    </div>
  );
}
