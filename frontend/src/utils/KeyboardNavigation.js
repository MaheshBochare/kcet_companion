export function handleKeyboardNavigation(
  e,
  suggestions,
  activeIndex,
  setActiveIndex,
  setQuery,
  setSuggestions
) {
  if (!suggestions.length) return;

  if (e.key === "ArrowDown") {
    setActiveIndex(prev =>
      prev < suggestions.length - 1 ? prev + 1 : prev
    );
  }

  if (e.key === "ArrowUp") {
    setActiveIndex(prev => (prev > 0 ? prev - 1 : -1));
  }

  if (e.key === "Enter" && activeIndex >= 0) {
    const selected = suggestions[activeIndex];
    setQuery(selected.college || "");
    setSuggestions([]);
  }
}
