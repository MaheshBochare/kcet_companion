import { useEffect, useRef, useState, useMemo } from "react";
import "@/styles/home.css";

export default function DataTable({ rows }) {
  /* -----------------------------
     Hooks MUST be at the top
  ----------------------------- */
  const tableRef = useRef(null);
  const [sort, setSort] = useState({ key: "", dir: "asc" });

  /* -----------------------------
     Empty-safe data
  ----------------------------- */
  const safeRows = rows || [];
  const columns = safeRows.length > 0 ? Object.keys(safeRows[0]) : [];

  /* -----------------------------
     Sorting
  ----------------------------- */
  const sortedRows = useMemo(() => {
    if (!sort.key) return safeRows;

    return [...safeRows].sort((a, b) => {
      const x = a[sort.key] ?? "";
      const y = b[sort.key] ?? "";

      if (!isNaN(x) && !isNaN(y)) {
        return sort.dir === "asc" ? x - y : y - x;
      }

      return sort.dir === "asc"
        ? String(x).localeCompare(String(y))
        : String(y).localeCompare(String(x));
    });
  }, [safeRows, sort]);

  /* -----------------------------
     Keyboard scrolling (TABLE)
  ----------------------------- */
  useEffect(() => {
    const handleKeyScroll = (e) => {
      if (!tableRef.current) return;

      const step = 40;

      if (e.key === "ArrowDown") tableRef.current.scrollTop += step;
      if (e.key === "ArrowUp") tableRef.current.scrollTop -= step;
      if (e.key === "PageDown") tableRef.current.scrollTop += step * 8;
      if (e.key === "PageUp") tableRef.current.scrollTop -= step * 8;
    };

    window.addEventListener("keydown", handleKeyScroll);
    return () => window.removeEventListener("keydown", handleKeyScroll);
  }, []);

  /* -----------------------------
     Sort handler
  ----------------------------- */
  const handleSort = (col) => {
    setSort((prev) => ({
      key: col,
      dir: prev.key === col && prev.dir === "asc" ? "desc" : "asc",
    }));
  };

  /* -----------------------------
     Render
  ----------------------------- */
  if (safeRows.length === 0) {
    return <p className="no-data">No data available</p>;
  }

  return (
    <div
      className="table-wrapper"
      ref={tableRef}
      tabIndex={0}   // enables keyboard focus
    >
      <table className="table">
        <thead>
          <tr>
            {columns.map((col) => (
              <th
                key={col}
                onClick={() => handleSort(col)}
                className="sortable"
              >
                {col}
                {sort.key === col && (
                  <span className="sort-indicator">
                    {sort.dir === "asc" ? " ▲" : " ▼"}
                  </span>
                )}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {sortedRows.map((row, i) => (
            <tr key={i}>
              {columns.map((col) => (
                <td key={col}>
                  {row[col] ?? "—"}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
