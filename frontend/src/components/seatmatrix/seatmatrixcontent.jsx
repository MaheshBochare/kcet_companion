import { useEffect, useMemo, useState } from "react";
import { fetchSeatmatrix } from "../../api/seatmatrixapi";
import Filters from "@/components/common/filters";
import DataTable from "@/components/common/Datatables";
import Pagination from "@/components/common/pagination";


export default function Seatmatrixcontent() {
  // -----------------------------
  // Data
  // -----------------------------
  const [rows, setRows] = useState([]);
  const [columns, setColumns] = useState([]);

  // -----------------------------
  // Pagination
  // -----------------------------
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  // -----------------------------
  // Filters
  // -----------------------------
  const [college, setCollege] = useState("");
  const [branch, setBranch] = useState("");
  const [category, setCategory] = useState("");
  const [round, setRound] = useState("");
  const [year, setYear] = useState("");

  // -----------------------------
  // Sorting
  // -----------------------------
  const [sort, setSort] = useState({ key: "", dir: "asc" });

  // -----------------------------
  // Fetch cutoff data
  // -----------------------------
  useEffect(() => {
    fetchSeatmatrix({
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

        console.log("✅ Seatmatrix API rows:", resultRows.length);

        setRows(resultRows);

        // Dynamic columns from API
        setColumns(resultRows.length ? Object.keys(resultRows[0]) : []);

        setTotalPages(data.pagination?.total_pages || 1);
      })
      .catch((err) => {
        console.error("❌Seatmatrix API error:", err);
        setRows([]);
        setColumns([]);
        setTotalPages(1);
      });
  }, [page, college, branch, category, round, year]);

  // -----------------------------
  // Sorting logic
  // -----------------------------
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

  // -----------------------------
  // Render
  // -----------------------------
  return (
    <div>
      <h2>seatmatrix analyzer</h2>

      <Filters
        college={college}
        setCollege={setCollege}
        branch={branch}
        setBranch={setBranch}
        category={category}
        setCategory={setCategory}
        round={round}
        setRound={setRound}
        year={year}
        setYear={setYear}
        setPage={setPage}
      />

      <p className="text-muted">Rows loaded: {sortedRows.length}</p>

      <DataTable
        rows={sortedRows}
        columns={columns}
        sort={sort}
        setSort={setSort}
      />

      <Pagination
        page={page}
        totalPages={totalPages}
        setPage={setPage}
      />
    </div>
  );
}
