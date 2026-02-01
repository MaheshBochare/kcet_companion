import { useEffect, useMemo, useState } from "react";
import { fetchCutoffRanks } from "../../api/cutoffApi";
import Filters from "./filters";
import DataTable from "./DataTables";
import Pagination from "./pagination";
import { useFilters } from "@/hooks/useFilters";
import "@/styles/cutoff.css";

export default function CutoffContent() {
  /* -----------------------------
     Table Data
  ----------------------------- */
  const [rows, setRows] = useState([]);
  const [columns, setColumns] = useState([]);

  /* -----------------------------
     Pagination
  ----------------------------- */
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  /* -----------------------------
     Filters (Custom Hook)
  ----------------------------- */
  const {
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
  } = useFilters(setPage);

  /* -----------------------------
     Sorting
  ----------------------------- */
  const [sort, setSort] = useState({ key: "", dir: "asc" });

  /* -----------------------------
     Fetch Cutoff Data
  ----------------------------- */
  useEffect(() => {
    fetchCutoffRanks({
      page,
      college,
      branch,
      category,
      round,
      year,
    })
      .then((res) => {
        const data = res?.data || {};
        const resultRows = data.results || [];

        setRows(resultRows);
        setColumns(resultRows.length ? Object.keys(resultRows[0]) : []);
        setTotalPages(data.pagination?.total_pages || 1);
      })
      .catch((err) => {
        console.error("❌ Cutoff API error:", err);
        setRows([]);
        setColumns([]);
        setTotalPages(1);
      });
  }, [page, college, branch, category, round, year]);

  /* -----------------------------
     Sorting Logic
  ----------------------------- */
  const sortedRows = useMemo(() => {
    if (!sort.key) return rows;

    return [...rows].sort((a, b) => {
      const x = a[sort.key] ?? "";
      const y = b[sort.key] ?? "";

      if (!isNaN(x) && !isNaN(y)) {
        return sort.dir === "asc" ? x - y : y - x;
      }

      return sort.dir === "asc"
        ? String(x).localeCompare(String(y))
        : String(y).localeCompare(String(x));
    });
  }, [rows, sort]);

  /* -----------------------------
     Render
  ----------------------------- */
  return (
    <div className="cutoff-content">
      {/* Apply Filters (Header always visible, body toggle handled inside) */}
      <Filters
        college={college}
        branch={branch}
        category={category}
        round={round}
        year={year}
        showFilters={showFilters}
        handleChange={handleChange}
        toggleFilters={toggleFilters}
        clearAllFilters={clearAllFilters}
        setCollege={setCollege}
        setBranch={setBranch}
        setCategory={setCategory}
        setRound={setRound}
        setYear={setYear}
      />

      {/* Data Table */}
      <DataTable
        rows={sortedRows}
        columns={columns}
        sort={sort}
        setSort={setSort}
      />
      {/* Pagination */}
      <Pagination
        page={page}
        totalPages={totalPages}
        setPage={setPage}
      />
    </div>
  );
}
