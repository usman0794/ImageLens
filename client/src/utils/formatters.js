export function formatSimilarity(score = 0) {
  const normalized = score > 1 ? score / 100 : score
  return `${Math.round(normalized * 1000) / 10}%`
}

export function formatBytesFromKb(kb) {
  if (!kb) return 'Unknown'
  if (kb >= 1024) return `${(kb / 1024).toFixed(1)} MB`
  return `${Math.round(kb)} KB`
}

export function getImageId(item) {
  return item?.image_id || item?.id || item?.filename
}

export function uniqueValues(items, key) {
  return ['all', ...Array.from(new Set(items.map((item) => item[key]).filter(Boolean)))]
}
