export default function Pagination({ page, totalPages, setPage }) {
  return (
    <div style={{ marginTop: "12px" }}>
      <button disabled={page === 1} onClick={() => setPage(p => p - 1)}>
        Prev
      </button>

      <span style={{ margin: "0 10px" }}>
        Page {page} / {totalPages}
      </span>

      <button disabled={page === totalPages} onClick={() => setPage(p => p + 1)}>
        Next
      </button>
    </div>
  );
}
