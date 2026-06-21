import { Link } from 'react-router-dom'

function NotFound() {
  return (
    <main className="container-page grid min-h-[70vh] place-items-center py-10 text-center">
      <div className="glass-panel max-w-lg p-8">
        <p className="text-6xl font-black text-brand-600">404</p>
        <h1 className="mt-4 text-2xl font-black text-slate-950 dark:text-white">Page not found</h1>
        <p className="mt-2 text-slate-600 dark:text-slate-300">The page you requested does not exist.</p>
        <Link to="/" className="btn-primary mt-6">Back to search</Link>
      </div>
    </main>
  )
}

export default NotFound
