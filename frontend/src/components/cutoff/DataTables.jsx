import "./DataTable.css";

export default function DataTable({ rows, columns, sort, setSort, page, pageSize }) {
  if (!rows.length) {
    return <p>No Data Available</p>;
  }

  const start = (page - 1) * pageSize;
  const pageData = rows.slice(start, start + pageSize);

  const toggleSort = (col) => {
    setSort(prev => ({
      key: col,
      dir: prev.key === col && prev.dir === "asc" ? "desc" : "asc"
    }));
  };

  return (
    <div className="table-wrapper">
      <table className="data-table">
        <thead>
          <tr>
            {columns.map(col => (
              <th key={col} onClick={() => toggleSort(col)}>
                {col}
                {sort.key === col && (
                  <span className="sort-arrow">
                    {sort.dir === "asc" ? "▲" : "▼"}
                  </span>
                )}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {pageData.map((row, idx) => (
            <tr key={idx}>
              {columns.map(col => (
                <td key={col}>
                  {row[col] !== null && row[col] !== "" ? row[col] : "-"}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
