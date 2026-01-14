export default function Pagination({ total, pageSize, page, setPage }) {
  const pages = Math.ceil(total / pageSize);

  return (
    <div style={{ marginTop: 15 }}>
      <button disabled={page === 1} onClick={() => setPage(p => p - 1)}>Prev</button>
      <span style={{ margin: "0 10px" }}>{page} / {pages}</span>
      <button disabled={page === pages} onClick={() => setPage(p => p + 1)}>Next</button>
    </div>
  );
}
