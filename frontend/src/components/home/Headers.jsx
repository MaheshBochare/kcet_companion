import SearchBox from "./SearchBox";

export default function HomeHeader({
  query,
  setQuery,
  suggestions,
  results,
  loading,
  activeIndex,
  handleKeyDown,
  onSearch,
}) {
  return (
    <header className="main-header">
      <h1>Passion Meets Career!</h1>

      {/* SEARCH BOX ONLY IN HEADER */}
      <SearchBox
        query={query}
        setQuery={setQuery}
        suggestions={suggestions}
        results={results}
        loading={loading}
        activeIndex={activeIndex}
        handleKeyDown={handleKeyDown}
        onSearch={onSearch}
      />
    </header>
  );
}
