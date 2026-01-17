export default function Filters({
  college, setCollege,
  branch, setBranch,
  category, setCategory,
  round, setRound,
  year, setYear,
  setPage
}) {

  const resetPage = () => setPage(1);

  return (
    <div style={{ display: "flex", gap: "10px", marginBottom: "12px" }}>

      <input
        placeholder="College Code (E021)"
        value={college}
        onChange={e => { setCollege(e.target.value); resetPage(); }}
      />

      <input
        placeholder="Branch (CSE)"
        value={branch}
        onChange={e => { setBranch(e.target.value); resetPage(); }}
      />

      <select value={category} onChange={e => { setCategory(e.target.value); resetPage(); }}>
        <option value="">All Categories</option>
        <option value="GM">GM</option>
        <option value="SCG">SC</option>
        <option value="STG">ST</option>
      </select>

      <select value={round} onChange={e => { setRound(e.target.value); resetPage(); }}>
        <option value="">All Rounds</option>
        <option value="1gen">Round 1</option>
        <option value="2gen">Round 2</option>
        <option value="2ext">Extended</option>
      </select>

      <select value={year} onChange={e => { setYear(e.target.value); resetPage(); }}>
        <option value="">All Years</option>
        <option value="24">2024</option>
        <option value="23">2023</option>
        <option value="22">2022</option>
        <option value="21">2021</option>
      </select>

    </div>
  );
}
