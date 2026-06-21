import { Link } from "react-router-dom";
import FilterSidebar from "../components/FilterSidebar";

import LoadingGrid from "../components/LoadingGrid";
import ResultsGrid from "../components/ResultsGrid";
import StatsBar from "../components/StatsBar";

function Results({
  results,
  filteredResults,
  loading,
  filters,
  setFilters,
  selectedResult,
  setSelectedResult,
  stats,
}) {
  return (
    <main className="container-page py-8">
      <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-sm font-bold uppercase tracking-wider text-brand-600 dark:text-brand-300">
            Results
          </p>
          <h1 className="text-3xl font-black tracking-tight text-slate-950 dark:text-white">
            Similar images
          </h1>
        </div>
        <Link to="/" className="btn-secondary">
          New search
        </Link>
      </div>

      <div className="mb-6">
        <StatsBar
          count={filteredResults.length || results.length}
          latencyMs={stats.latencyMs}
          mocked={stats.mocked}
        />
      </div>

      <div className="grid gap-6 lg:grid-cols-[280px_1fr]">
        <FilterSidebar
          results={results}
          filters={filters}
          setFilters={setFilters}
        />
        {loading ? (
          <LoadingGrid />
        ) : (
          <ResultsGrid
            results={filteredResults}
            onPreview={setSelectedResult}
          />
        )}
      </div>
    </main>
  );
}

export default Results;
