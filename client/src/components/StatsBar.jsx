import { Timer } from 'lucide-react'

function StatsBar({ count, latencyMs, mocked }) {
  return (
    <div className="glass-panel flex flex-col gap-3 p-4 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex items-center gap-2 text-sm font-bold text-slate-700 dark:text-slate-200">
        <Timer size={18} className="text-brand-600" />
        {count} results found in {latencyMs || 0}ms
      </div>
      {mocked && (
        <span className="badge bg-orange-100 text-orange-700 dark:bg-orange-500/10 dark:text-orange-200">
          Mock fallback shown until text-search API is connected
        </span>
      )}
    </div>
  )
}

export default StatsBar
