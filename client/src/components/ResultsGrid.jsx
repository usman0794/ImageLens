import ResultCard from './ResultCard'

function ResultsGrid({ results, onPreview }) {
  if (!results.length) {
    return (
      <div className="glass-panel flex min-h-80 items-center justify-center p-8 text-center">
        <div>
          <p className="text-xl font-black text-slate-900 dark:text-white">No results match your filters</p>
          <p className="mt-2 text-slate-500 dark:text-slate-400">Try lowering the similarity threshold or clearing category/source filters.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 xl:grid-cols-3">
      {results.map((result) => (
        <ResultCard key={result.image_id} result={result} onPreview={onPreview} />
      ))}
    </div>
  )
}

export default ResultsGrid
