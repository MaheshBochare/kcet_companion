import { useState } from "react";
import Navbar from "../components/layout/navbar";
import Footer from "../components/home/Footer";
import Dashboard from "../components/home/Dashboard";
import HomeHeader from "../components/home/Headers";
import SearchResults from "../components/home/SearchResults";
import "../styles/home.css";

import { useHomeData } from "../hooks/usehomedata";
import { useSmartSearch } from "../hooks/useSmartSearch";
import { handleKeyboardNavigation } from "../utils/KeyboardNavigation";

export default function Home() {
  const { featured, stats, quickLinks } = useHomeData();

  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const {
    suggestions,
    loading,
    activeIndex,
    setActiveIndex,
    setSuggestions,
  } = useSmartSearch(query);

  /* Keyboard navigation */
  const onKeyDown = (e) =>
    handleKeyboardNavigation(
      e,
      suggestions,
      activeIndex,
      setActiveIndex,
      setQuery,
      setSuggestions
    );

  const handleSearchSubmit = (selected = null) => {
    if (!query.trim()) return;

    if (selected) {
      // ✅ user clicked one suggestion
      setResults([selected]);
    } else {
      // ✅ user pressed Enter → show all matches
      setResults(suggestions);
    }

    setSuggestions([]);
    setActiveIndex(-1);
  };


  return (
    <>
      <Navbar />

      {/* HEADER (ONLY PLACE WITH SEARCH BOX) */}
      <HomeHeader
        query={query}
        setQuery={setQuery}
        suggestions={suggestions}
        results={results}
        loading={loading}
        activeIndex={activeIndex}
        handleKeyDown={onKeyDown}
        onSearch={handleSearchSubmit}
      />

      {/* SEARCH RESULTS */}
      {results.length > 0 && (
        <SearchResults results={results} query={query} />
      )}

      {/* DASHBOARD (hide when results visible) */}
      {results.length === 0 && (
        <Dashboard
          quickLinks={quickLinks}
          stats={stats}
          featured={featured}
        />
      )}

      <Footer />
    </>
  );
}
