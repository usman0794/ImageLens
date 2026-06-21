import { ImagePlus, X } from 'lucide-react'
import { useMemo, useState } from 'react'

function UploadDropzone({ selectedImage, setSelectedImage, multiple = false, onFiles }) {
  const [dragActive, setDragActive] = useState(false)
  const preview = useMemo(() => (selectedImage ? URL.createObjectURL(selectedImage) : null), [selectedImage])

  const handleFiles = (files) => {
    const imageFiles = Array.from(files).filter((file) => file.type.startsWith('image/'))
    if (!imageFiles.length) return
    if (multiple && onFiles) onFiles(imageFiles)
    setSelectedImage?.(imageFiles[0])
  }

  return (
    <label
      onDragOver={(event) => {
        event.preventDefault()
        setDragActive(true)
      }}
      onDragLeave={() => setDragActive(false)}
      onDrop={(event) => {
        event.preventDefault()
        setDragActive(false)
        handleFiles(event.dataTransfer.files)
      }}
      className={`relative flex min-h-72 cursor-pointer flex-col items-center justify-center overflow-hidden rounded-3xl border-2 border-dashed p-6 text-center transition ${dragActive ? 'border-brand-500 bg-brand-50 dark:bg-brand-500/10' : 'border-slate-300 bg-slate-50/70 hover:border-brand-400 hover:bg-brand-50/60 dark:border-slate-700 dark:bg-slate-950/60 dark:hover:bg-brand-500/10'}`}
    >
      <input
        type="file"
        accept="image/*"
        multiple={multiple}
        className="sr-only"
        onChange={(event) => handleFiles(event.target.files)}
      />

      {preview ? (
        <>
          <img src={preview} alt="Selected upload preview" className="absolute inset-0 h-full w-full object-cover" />
          <div className="absolute inset-0 bg-slate-950/45" />
          <button
            type="button"
            onClick={(event) => {
              event.preventDefault()
              setSelectedImage?.(null)
            }}
            className="absolute right-4 top-4 rounded-full bg-white/90 p-2 text-slate-700 shadow-lg hover:bg-white"
          >
            <X size={18} />
          </button>
          <div className="relative z-10 rounded-2xl bg-white/90 px-4 py-3 text-left shadow-soft dark:bg-slate-900/90">
            <p className="font-bold text-slate-950 dark:text-white">{selectedImage.name}</p>
            <p className="text-sm text-slate-500 dark:text-slate-400">Click to replace or drag another image</p>
          </div>
        </>
      ) : (
        <>
          <div className="mb-4 grid h-16 w-16 place-items-center rounded-3xl bg-brand-100 text-brand-700 dark:bg-brand-500/15 dark:text-brand-200">
            <ImagePlus size={30} />
          </div>
          <p className="text-lg font-black text-slate-900 dark:text-white">Drag & drop image here</p>
          <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">or click to browse files. PNG, JPG, WEBP supported.</p>
        </>
      )}
    </label>
  )
}

export default UploadDropzone
