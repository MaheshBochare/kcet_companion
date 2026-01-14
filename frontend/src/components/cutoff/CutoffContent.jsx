import { useEffect, useMemo, useState } from "react";
import { fetchCutoffData } from "../../api/cutoffApi";
import Filters from "./filters";
import DataTable from "./DataTables";
import Pagination from "./pagination";

export default function CutoffContent() {
  const [data, setData] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [visibleCols, setVisibleCols] = useState([]);
  const [sort, setSort] = useState({ key: "", dir: "asc" });
  const [page, setPage] = useState(1);

  const pageSize = 20;

  useEffect(() => {
    fetchCutoffData().then(res => {
      setData(res.data);
      setFiltered(res.data);
      setVisibleCols(Object.keys(res.data[0] || {}));
    });
  }, []);

  const sortedData = useMemo(() => {
    let temp = [...filtered];

    if (!sort.key) return temp;

    temp.sort((a, b) => {
      let x = a[sort.key] ?? "";
      let y = b[sort.key] ?? "";

      if (!isNaN(x) && !isNaN(y)) return sort.dir === "asc" ? x - y : y - x;
      return sort.dir === "asc"
        ? String(x).localeCompare(String(y))
        : String(y).localeCompare(String(x));
    });

    return temp;
  }, [filtered, sort]);

  return (
    <>
      <h2>Cutoff Analyzer</h2>

      <Filters
        data={data}
        setFiltered={setFiltered}
        setVisibleCols={setVisibleCols}
        setPage={setPage}
      />

      <DataTable
        rows={sortedData}
        columns={visibleCols}
        sort={sort}
        setSort={setSort}
        page={page}
        pageSize={pageSize}
      />

      <Pagination
        total={sortedData.length}
        pageSize={pageSize}
        page={page}
        setPage={setPage}
      />
    </>
  );
}
