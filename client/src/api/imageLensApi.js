const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

const BACKEND_ORIGIN =
  import.meta.env.VITE_BACKEND_ORIGIN ||
  API_BASE_URL.replace(/\/api\/v\d+\/?$/, "");

const S3_BUCKET_URL =
  import.meta.env.VITE_S3_BUCKET_URL ||
  "https://imagelens-s3.s3.eu-north-1.amazonaws.com";

function absoluteImageUrl(input) {
  if (!input) return "";

  let url = String(input).trim().replaceAll("\\", "/");

  // Fix old wrong region URLs and malformed old URLs
  url = url
    .replace(
      "{https://imagelens-s3}.s3.eu-north-1.amazonaws.com",
      "https://imagelens-s3.s3.eu-north-1.amazonaws.com",
    )
    .replace(
      "{https://imagelens-s3}.s3.us-east-1.amazonaws.com",
      "https://imagelens-s3.s3.eu-north-1.amazonaws.com",
    )
    .replace(
      "imagelens-s3.s3.us-east-1.amazonaws.com",
      "imagelens-s3.s3.eu-north-1.amazonaws.com",
    );

  // If backend returns full URL or pre-signed S3 URL, use it directly
  if (/^https?:\/\//i.test(url)) return url;

  // If backend returns /uploads/file.jpeg
  if (url.startsWith("/uploads/")) {
    return `${S3_BUCKET_URL}${url}`;
  }

  // If backend returns uploads/file.jpeg
  if (url.startsWith("uploads/")) {
    return `${S3_BUCKET_URL}/${url}`;
  }

  // If backend returns other local path
  if (url.startsWith("/")) {
    return `${BACKEND_ORIGIN}${url}`;
  }

  // If backend returns only filename.jpeg
  return `${S3_BUCKET_URL}/uploads/${url}`;
}

function normalizeResult(item, index = 0) {
  const rawImagePath =
    item.url ||
    item.image_url ||
    item.path ||
    item.file_path ||
    item.s3_key ||
    item.key ||
    item.filename;

  return {
    image_id: item.image_id || item.id || `result_${index}`,
    vector_id: item.vector_id,
    filename:
      item.filename ||
      rawImagePath?.split("/").pop()?.split("?")[0] ||
      `image-${index + 1}.jpg`,
    url: absoluteImageUrl(rawImagePath),
    score: item.score ?? item.similarity ?? 0,
    similarity: item.similarity ?? item.score ?? 0,
    category: item.category || "uncategorized",
    source: item.source || item.storage_type || "indexed",
    tags: Array.isArray(item.tags) ? item.tags : [],
    width: item.width,
    height: item.height,
    file_size_kb: item.file_size_kb,
    description: item.description || "",
    created_at: item.created_at,
    updated_at: item.updated_at,
  };
}

async function parseJson(response) {
  const payload = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(
      payload.detail ||
        payload.message ||
        `Request failed with status ${response.status}`,
    );
  }

  return payload;
}

export async function searchByImage(file, topK = 20) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("top_k", String(topK));

  const started = performance.now();

  const payload = await fetch(`${API_BASE_URL}/search/image`, {
    method: "POST",
    body: formData,
  }).then(parseJson);

  return {
    results: (payload.results || []).map(normalizeResult),
    latencyMs: Math.round(performance.now() - started),
  };
}

export async function searchByText(query, topK = 20) {
  const started = performance.now();

  const payload = await fetch(`${API_BASE_URL}/search/text`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query,
      top_k: topK,
    }),
  }).then(parseJson);

  return {
    results: (payload.results || []).map(normalizeResult),
    latencyMs: Math.round(performance.now() - started),
  };
}

export async function uploadImage({ file, category, tags, description }) {
  const formData = new FormData();
  formData.append("file", file);

  if (category) {
    formData.append("category", category);
  }

  if (tags) {
    formData.append("tags", Array.isArray(tags) ? tags.join(",") : tags);
  }

  if (description) {
    formData.append("description", description);
  }

  const payload = await fetch(`${API_BASE_URL}/images/upload`, {
    method: "POST",
    body: formData,
  }).then(parseJson);

  return normalizeResult(payload.image);
}

export async function batchUploadImages(files, metadata = {}) {
  const uploaded = [];

  for (const file of files) {
    const result = await uploadImage({
      file,
      ...metadata,
    });

    uploaded.push(result);
  }

  return uploaded;
}

export async function fetchImageById(id) {
  const payload = await fetch(`${API_BASE_URL}/images/${id}`).then(parseJson);

  return normalizeResult(payload.image || payload);
}

export async function fetchDashboardAnalytics() {
  const payload = await fetch(`${API_BASE_URL}/analytics/summary`).then(
    parseJson,
  );

  return {
    metrics: payload.metrics || {
      totalImages: 0,
      searches: 0,
      categories: 0,
      avgLatency: 0,
    },
    searchesOverTime: payload.searchesOverTime || [],
    topCategories: payload.topCategories || [],
  };
}
