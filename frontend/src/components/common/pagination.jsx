export default function DataTable({
  rows = [],
  columns = [],
  sort = {},
  setSort = () => {}
}) {
  if (!rows.length) {
    return <p className="text-muted">No data available</p>;
  }

  const handleSort = (col) => {
    setSort(prev => ({
      key: col,
      dir: prev?.key === col && prev?.dir === "asc" ? "desc" : "asc"
    }));
  };

  return (
    <div className="table-responsive">
      <table className="table table-bordered table-sm">
        <thead>
          <tr>
            {columns.map(col => (
              <th
                key={col}
                onClick={() => handleSort(col)}
                style={{ cursor: "pointer" }}
              >
                {col}
                {sort?.key === col
                  ? sort?.dir === "asc"
                    ? " ▲"
                    : " ▼"
                  : ""}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {rows.map((row, idx) => (
            <tr key={idx}>
              {columns.map(col => (
                <td key={col}>{row?.[col]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
