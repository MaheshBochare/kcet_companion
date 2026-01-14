export default function Filters({ data, setFiltered, setVisibleCols, setPage }) {
  const getAllCols = () => Object.keys(data[0] || {});
  const unique = k => [...new Set(data.map(r => r[k]))];

  const applyFilters = (filters) => {
    setPage(1);

    // ROW FILTERS
    let rows = data.filter(row => {
      if (filters.college && row.college_Namess !== filters.college) return false;
      if (filters.branch && row.branchss !== filters.branch) return false;
      return true;
    });

    // COLUMN FILTERS
    let cols = getAllCols();

    cols = cols.filter(col => {
      if (!col.startsWith("R_")) return true;

      if (filters.category && !col.includes(`_${filters.category}_`)) return false;
      if (filters.round && !col.includes(`_${filters.round}`)) return false;
      if (filters.year && !col.endsWith(filters.year.slice(-2))) return false;

      return true;
    });

    setFiltered(rows);
    setVisibleCols(cols);
  };

  return (
    <div style={{ display: "flex", gap: 10, marginBottom: 15 }}>
      <select onChange={e => applyFilters({ college: e.target.value })}>
        <option value="">College</option>
        {unique("college_Namess").map(v => <option key={v}>{v}</option>)}
      </select>

      <select onChange={e => applyFilters({ branch: e.target.value })}>
        <option value="">Branch</option>
        {unique("branchss").map(v => <option key={v}>{v}</option>)}
      </select>

      <select onChange={e => applyFilters({ category: e.target.value })}>
        <option value="">Category</option>
        {["1G","2AG","2BG","3AG","3BG","GM","SCG","STG"].map(v => <option key={v}>{v}</option>)}
      </select>

      <select onChange={e => applyFilters({ round: e.target.value })}>
        <option value="">Round</option>
        {["1gen","2gen","2ext"].map(v => <option key={v}>{v}</option>)}
      </select>

      <select onChange={e => applyFilters({ year: e.target.value })}>
        <option value="">Year</option>
        {["2021","2022","2023","2024"].map(v => <option key={v}>{v}</option>)}
      </select>
    </div>
  );
}
