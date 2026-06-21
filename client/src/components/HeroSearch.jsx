import { AlertCircle, Search, Sparkles, UploadCloud } from "lucide-react";
import TextSearchBar from "./TextSearchBar";
import UploadDropzone from "./UploadDropzone";

const exampleQueries = [
  "mini camera",
  "projector",
  "digital clock",
  "robot vacuum",
];

function HeroSearch({
  activeTab,
  setActiveTab,
  selectedImage,
  setSelectedImage,
  textQuery,
  setTextQuery,
  loading,
  error,
  handleSearch,
}) {
  const canSearch =
    activeTab === "upload"
      ? Boolean(selectedImage)
      : textQuery.trim().length > 0;

  const submit = (event) => {
    event.preventDefault();
    if (canSearch) handleSearch();
  };

  return (
    <section className="container-page py-10 sm:py-16 lg:py-20">
      <div className="mx-auto max-w-4xl text-center">
        <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-brand-200 bg-white/80 px-4 py-2 text-sm font-semibold text-brand-700 shadow-sm dark:border-brand-500/30 dark:bg-brand-500/10 dark:text-brand-200">
          Visual similarity + natural language search
        </div>
        <h1 className="text-4xl font-black tracking-tight text-slate-950 dark:text-white sm:text-6xl">
          Find images by visual similarity or natural language
        </h1>
      </div>

      <form
        onSubmit={submit}
        className="glass-panel mx-auto mt-10 max-w-4xl overflow-hidden p-3 sm:p-4"
      >
        <div className="grid grid-cols-2 rounded-2xl bg-slate-100 p-1 dark:bg-slate-950">
          <button
            type="button"
            onClick={() => setActiveTab("upload")}
            className={`flex items-center justify-center gap-2 rounded-xl px-4 py-3 text-sm font-bold transition ${activeTab === "upload" ? "bg-white text-brand-700 shadow-sm dark:bg-slate-800 dark:text-brand-200" : "text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white"}`}
          >
            <UploadCloud size={18} /> Upload Image
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("text")}
            className={`flex items-center justify-center gap-2 rounded-xl px-4 py-3 text-sm font-bold transition ${activeTab === "text" ? "bg-white text-brand-700 shadow-sm dark:bg-slate-800 dark:text-brand-200" : "text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white"}`}
          >
            <Search size={18} /> Text Search
          </button>
        </div>

        <div className="p-2 pt-5 sm:p-5">
          {activeTab === "upload" ? (
            <UploadDropzone
              selectedImage={selectedImage}
              setSelectedImage={setSelectedImage}
            />
          ) : (
            <TextSearchBar
              value={textQuery}
              onChange={setTextQuery}
              suggestions={exampleQueries}
            />
          )}

          {error && (
            <div className="mt-5 flex items-center justify-center gap-2 rounded-2xl bg-red-50 px-4 py-3 text-sm font-medium text-red-700 dark:bg-red-500/10 dark:text-red-200">
              <AlertCircle size={18} /> {error}
            </div>
          )}

          <button
            type="submit"
            disabled={!canSearch || loading}
            className="btn-primary mx-auto mt-6 w-full sm:w-auto sm:min-w-48"
          >
            {loading ? "Searching..." : "Search"}
          </button>
        </div>
      </form>
    </section>
  );
}

export default HeroSearch;
