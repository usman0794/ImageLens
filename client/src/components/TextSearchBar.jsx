import { Search } from "lucide-react";

function TextSearchBar({ value, onChange, suggestions = [] }) {
  return (
    <div className="space-y-4">
      <div className="relative">
        <Search
          className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"
          size={20}
        />
        <input
          className="input-field py-5 pl-12 text-base"
          placeholder="Search by prompt, tag, object, mood, category..."
          value={value}
          onChange={(event) => onChange(event.target.value)}
          list="search-suggestions"
        />
        <datalist id="search-suggestions">
          {suggestions.map((item) => (
            <option key={item} value={item} />
          ))}
        </datalist>
      </div>
    </div>
  );
}

export default TextSearchBar;
