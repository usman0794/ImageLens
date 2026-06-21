import { Download, Eye } from "lucide-react";
import { Link } from "react-router-dom";
import { formatSimilarity, getImageId } from "../utils/formatters";

function ResultCard({ result, onPreview }) {
  const id = getImageId(result);

  return (
    <article className="group overflow-hidden rounded-3xl border border-white/70 bg-white shadow-sm transition hover:-translate-y-1 hover:shadow-soft dark:border-slate-800 dark:bg-slate-900">
      <div className="relative aspect-[4/3] overflow-hidden bg-slate-100 dark:bg-slate-800">
        <img
          src={result.url}
          alt={result.filename}
          className="h-full w-full object-cover transition duration-500 group-hover:scale-105"
          loading="lazy"
        />
        <div className="absolute left-3 top-3 rounded-full bg-slate-950/80 px-3 py-1 text-xs font-black text-white backdrop-blur">
          {formatSimilarity(result.score)}
        </div>
      </div>
      <div className="space-y-4 p-4">
        <div>
          <h3 className="line-clamp-2 break-all text-sm font-black text-slate-900 dark:text-white">
            {result.filename}
          </h3>
          <p className="text-sm capitalize text-slate-500 dark:text-slate-400">
            {result.category} · {result.source}
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          {(result.tags || []).slice(0, 3).map((tag) => (
            <span key={tag} className="badge">
              #{tag}
            </span>
          ))}
        </div>
        <div className="grid grid-cols-2 gap-2">
          <button
            className="btn-secondary !px-3 !py-2"
            onClick={() => onPreview(result)}
          >
            <Eye size={16} /> View
          </button>
          <a href={result.url} download className="btn-secondary !px-3 !py-2">
            <Download size={16} /> Download
          </a>
        </div>
      </div>
    </article>
  );
}

export default ResultCard;
