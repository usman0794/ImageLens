# ImageLens Frontend

Vite + React + Tailwind CSS frontend for the ImageLens visual similarity backend.

## Features

- Responsive Home/Search page with Upload Image and Text Search tabs
- Results page with filters, similarity threshold, stats, cards, and preview modal
- Image detail page with metadata, tags, source, preview, and download action
- Dashboard page with analytics cards and Recharts visualizations
- Admin upload page for batch image indexing
- Dark mode toggle, recent search history, skeleton loading states

## Backend integration

By default the app calls:

```bash
http://localhost:8000/api/v1
```

Create `.env` from `.env.example` if your backend runs elsewhere.

Supported current backend endpoints:

- `POST /api/v1/search/image` — image similarity search
- `POST /api/v1/images/upload` — image upload/indexing

Text search, dashboard stats, and image-detail fetch include graceful mock fallbacks until matching backend endpoints are added.

## Run

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
```
