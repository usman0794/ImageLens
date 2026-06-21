import { ArrowLeft, Copy, Download } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { fetchImageById } from '../api/imageLensApi'
import { formatBytesFromKb, formatSimilarity } from '../utils/formatters'

function ImageDetail() {
  const { id } = useParams()
  const [image, setImage] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchImageById(id).then(setImage).finally(() => setLoading(false))
  }, [id])

  if (loading) {
    return <main className="container-page py-10"><div className="glass-panel h-96 animate-pulse" /></main>
  }

  if (!image) return null

  return (
    <main className="container-page py-8">
      <Link to="/results" className="mb-6 inline-flex items-center gap-2 text-sm font-bold text-brand-600 hover:text-brand-700 dark:text-brand-300">
        <ArrowLeft size={17} /> Back to results
      </Link>

      <div className="grid gap-6 lg:grid-cols-[1.35fr_.75fr]">
        <section className="glass-panel overflow-hidden p-3">
          <div className="rounded-2xl bg-slate-950 p-3">
            <img src={image.url} alt={image.filename} className="mx-auto max-h-[72vh] rounded-xl object-contain" />
          </div>
        </section>

        <aside className="glass-panel p-6">
          <span className="badge mb-4">Similarity {formatSimilarity(image.score)}</span>
          <h1 className="text-3xl font-black text-slate-950 dark:text-white">{image.filename}</h1>
          <p className="mt-3 text-slate-600 dark:text-slate-300">{image.description}</p>

          <dl className="mt-8 grid gap-4 text-sm">
            <div className="flex justify-between gap-5"><dt className="text-slate-500">Image ID</dt><dd className="font-mono text-xs font-semibold">{image.image_id}</dd></div>
            <div className="flex justify-between gap-5"><dt className="text-slate-500">Category</dt><dd className="font-semibold capitalize">{image.category}</dd></div>
            <div className="flex justify-between gap-5"><dt className="text-slate-500">Source</dt><dd className="font-semibold">{image.source}</dd></div>
            <div className="flex justify-between gap-5"><dt className="text-slate-500">Dimensions</dt><dd className="font-semibold">{image.width && image.height ? `${image.width} × ${image.height}` : 'Unknown'}</dd></div>
            <div className="flex justify-between gap-5"><dt className="text-slate-500">File size</dt><dd className="font-semibold">{formatBytesFromKb(image.file_size_kb)}</dd></div>
          </dl>

          <div className="mt-7 flex flex-wrap gap-2">
            {(image.tags || []).map((tag) => <span className="badge" key={tag}>#{tag}</span>)}
          </div>

          <div className="mt-8 grid grid-cols-2 gap-3">
            <a href={image.url} download className="btn-primary"><Download size={17} /> Download</a>
            <button className="btn-secondary" onClick={() => navigator.clipboard.writeText(image.url)}><Copy size={17} /> Copy URL</button>
          </div>
        </aside>
      </div>
    </main>
  )
}

export default ImageDetail
