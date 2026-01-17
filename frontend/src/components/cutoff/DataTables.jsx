export default function DataTable({ rows }) {
  if (!rows || rows.length === 0) {
    return <p style={{ marginTop: "12px" }}>No data available</p>;
  }

  const columns = Object.keys(rows[0]);

  return (
    <div style={{ overflowX: "auto", maxWidth: "100%" }}>
      <table
        border="1"
        cellPadding="6"
        style={{
          borderCollapse: "collapse",
          minWidth: "1200px",
          whiteSpace: "nowrap"
        }}
      >
        <thead>
          <tr>
            {columns.map(col => (
              <th
                key={col}
                style={{
                  background: "#f5f5f5",
                  position: "sticky",
                  top: 0
                }}
              >
                {col}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {rows.map((row, i) => (
            <tr key={i}>
              {columns.map(col => (
                <td key={col}>{row[col]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
