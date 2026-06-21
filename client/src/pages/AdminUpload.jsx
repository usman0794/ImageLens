import { CheckCircle2, ShieldCheck, UploadCloud } from "lucide-react";
import { useState } from "react";
import { batchUploadImages } from "../api/imageLensApi";
import UploadDropzone from "../components/UploadDropzone";

function AdminUpload() {
  const [files, setFiles] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null);
  const [category, setCategory] = useState("");
  const [source, setSource] = useState("user_upload");
  const [tags, setTags] = useState("");
  const [description, setDescription] = useState("");
  const [uploading, setUploading] = useState(false);
  const [uploaded, setUploaded] = useState([]);
  const [error, setError] = useState("");

  const handleFiles = (incoming) =>
    setFiles((current) => [...current, ...incoming]);

  const submit = async (event) => {
    event.preventDefault();
    if (!files.length && !selectedImage) return;
    setUploading(true);
    setError("");

    try {
      const queue = files.length ? files : [selectedImage];
      const results = await batchUploadImages(queue, {
        category,
        source,
        tags,
        description,
      });
      setUploaded(results);
      setFiles([]);
      setSelectedImage(null);
    } catch (err) {
      setError(err.message || "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  return (
    <main className="container-page py-8">
      <div className="mb-8 flex flex-col gap-3 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="flex items-center gap-2 text-sm font-bold uppercase tracking-wider text-brand-600 dark:text-brand-300">
            <ShieldCheck size={16} /> Admin-only
          </p>
          <h1 className="text-3xl font-black tracking-tight text-slate-950 dark:text-white">
            Upload and index images
          </h1>
        </div>
      </div>

      <form onSubmit={submit} className="grid gap-6 lg:grid-cols-[1fr_380px]">
        <div className="glass-panel p-4">
          <UploadDropzone
            selectedImage={selectedImage}
            setSelectedImage={setSelectedImage}
            multiple
            onFiles={handleFiles}
          />
          <div className="mt-4 flex flex-wrap gap-2">
            {files.map((file) => (
              <span className="badge" key={`${file.name}-${file.size}`}>
                {file.name}
              </span>
            ))}
          </div>
        </div>

        <aside className="glass-panel space-y-4 p-5">
          <label className="space-y-2 block">
            <span className="text-sm font-semibold text-slate-600 dark:text-slate-300">
              Category
            </span>
            <input
              className="input-field"
              value={category}
              onChange={(event) => setCategory(event.target.value)}
              placeholder="automobiles, nature, fashion..."
            />
          </label>
          <label className="space-y-2 block">
            <span className="text-sm font-semibold text-slate-600 dark:text-slate-300">
              Source
            </span>
            <input
              className="input-field"
              value={source}
              onChange={(event) => setSource(event.target.value)}
              placeholder="user_upload"
            />
          </label>
          <label className="space-y-2 block">
            <span className="text-sm font-semibold text-slate-600 dark:text-slate-300">
              Tags
            </span>
            <input
              className="input-field"
              value={tags}
              onChange={(event) => setTags(event.target.value)}
              placeholder="red, car, sports"
            />
          </label>
          <label className="space-y-2 block">
            <span className="text-sm font-semibold text-slate-600 dark:text-slate-300">
              Description
            </span>
            <textarea
              className="input-field min-h-28"
              value={description}
              onChange={(event) => setDescription(event.target.value)}
              placeholder="Optional image description"
            />
          </label>

          {error && (
            <p className="rounded-2xl bg-red-50 p-3 text-sm font-semibold text-red-700 dark:bg-red-500/10 dark:text-red-200">
              {error}
            </p>
          )}
          {!!uploaded.length && (
            <p className="flex items-center gap-2 rounded-2xl bg-green-50 p-3 text-sm font-semibold text-green-700 dark:bg-green-500/10 dark:text-green-200">
              <CheckCircle2 size={17} /> Uploaded {uploaded.length} images
            </p>
          )}

          <button
            disabled={uploading || (!files.length && !selectedImage)}
            className="btn-primary w-full"
          >
            <UploadCloud size={18} />{" "}
            {uploading ? "Indexing..." : "Upload & index batch"}
          </button>
        </aside>
      </form>
    </main>
  );
}

export default AdminUpload;
