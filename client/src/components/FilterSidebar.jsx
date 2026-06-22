import { SlidersHorizontal } from "lucide-react";
import { uniqueValues } from "../utils/formatters";

function FilterSidebar({ results, filters, setFilters }) {
  const categories = uniqueValues(results, "category");
  const sources = uniqueValues(results, "source");

  const update = (key, value) =>
    setFilters((current) => ({ ...current, [key]: value }));

  return (
    <aside className="glass-panel p-5 lg:sticky lg:top-24">
      <div className="mb-5 flex items-center gap-2">
        <SlidersHorizontal size={18} className="text-brand-600" />
        <h2 className="font-black">Filters</h2>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-1">
        <label className="space-y-2">
          <span className="text-sm font-semibold text-slate-600 dark:text-slate-300">
            Category
          </span>
          <select
            className="input-field"
            value={filters.category}
            onChange={(event) => update("category", event.target.value)}
          >
            {categories.map((category) => (
              <option key={category} value={category}>
                {category === "all" ? "All" : category}
              </option>
            ))}
          </select>
        </label>

        <label className="space-y-2">
          <span className="text-sm font-semibold text-slate-600 dark:text-slate-300">
            Source
          </span>
          <select
            className="input-field"
            value={filters.source}
            onChange={(event) => update("source", event.target.value)}
          >
            {sources.map((source) => (
              <option key={source} value={source}>
                {source === "all" ? "All" : source}
              </option>
            ))}
          </select>
        </label>

        <label className="space-y-2 sm:col-span-2 lg:col-span-1">
          <div className="flex items-center justify-between text-sm font-semibold text-slate-600 dark:text-slate-300">
            <span>Similarity threshold</span>
            <span>{Math.round(filters.minSimilarity * 100)}%+</span>
          </div>
          <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            value={filters.minSimilarity}
            onChange={(event) =>
              update("minSimilarity", Number(event.target.value))
            }
            className="w-full accent-brand-600"
          />
        </label>

        <label className="space-y-2">
          <span className="text-sm font-semibold text-slate-600 dark:text-slate-300">
            Sort
          </span>
          <select
            className="input-field"
            value={filters.sortBy}
            onChange={(event) => update("sortBy", event.target.value)}
          >
            <option value="relevance">Best match</option>
            <option value="newest">Newest</option>
            <option value="name">Name</option>
          </select>
        </label>

        <label className="space-y-2">
          <span className="text-sm font-semibold text-slate-600 dark:text-slate-300">
            Results to show
          </span>
          <select
            className="input-field"
            value={filters.maxResults}
            onChange={(event) =>
              update("maxResults", Number(event.target.value))
            }
          >
            <option value={6}>Top 6</option>
            <option value={12}>Top 12</option>
            <option value={24}>Top 24</option>
            <option value={1000}>All</option>
          </select>
        </label>
      </div>
    </aside>
  );
}

export default FilterSidebar;
