import { useMemo, useState } from "react";
import { Navigate, Route, Routes, useNavigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Results from "./pages/Results";
import ImageDetail from "./pages/ImageDetail";
import Dashboard from "./pages/Dashboard";
import AdminUpload from "./pages/AdminUpload";
import NotFound from "./pages/NotFound";
import { searchByImage, searchByText } from "./api/imageLensApi";

const defaultFilters = {
  category: "all",
  source: "all",
  minSimilarity: 0.6,
  sortBy: "relevance",
  maxResults: 6,
};

function App() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState("upload");
  const [selectedImage, setSelectedImage] = useState(null);
  const [textQuery, setTextQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedResult, setSelectedResult] = useState(null);
  const [filters, setFilters] = useState(defaultFilters);
  const [stats, setStats] = useState({ count: 0, latencyMs: 0, mocked: false });

  const handleSearch = async (override) => {
    const searchMode = override?.type || activeTab;
    setLoading(true);
    setError("");

    try {
      const response =
        searchMode === "upload"
          ? await searchByImage(override?.file || selectedImage)
          : await searchByText(override?.query ?? textQuery);

      setResults(response.results);
      setStats({
        count: response.results.length,
        latencyMs: response.latencyMs,
        mocked: response.mocked,
      });

      navigate("/results");
    } catch (err) {
      setError(err.message || "Search failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const filteredResults = useMemo(() => {
    return results
      .filter(
        (item) =>
          filters.category === "all" || item.category === filters.category,
      )
      .filter(
        (item) => filters.source === "all" || item.source === filters.source,
      )
      .filter(
        (item) =>
          (item.score > 1 ? item.score / 100 : item.score) >=
          filters.minSimilarity,
      )
      .sort((a, b) => {
        if (filters.sortBy === "newest")
          return new Date(b.created_at || 0) - new Date(a.created_at || 0);
        if (filters.sortBy === "name")
          return a.filename.localeCompare(b.filename);
        return (b.score || 0) - (a.score || 0);
      })
      .slice(0, filters.maxResults);
  }, [filters, results]);

  const appState = {
    activeTab,
    setActiveTab,
    selectedImage,
    setSelectedImage,
    textQuery,
    setTextQuery,
    results,
    filteredResults,
    loading,
    error,
    setError,
    selectedResult,
    setSelectedResult,
    filters,
    setFilters,
    handleSearch,
    stats,
  };

  return (
    <div className="min-h-screen">
      <Navbar />
      <Routes>
        <Route path="/" element={<Home {...appState} />} />
        <Route path="/search" element={<Navigate to="/" replace />} />
        <Route path="/results" element={<Results {...appState} />} />
        <Route path="/image/:id" element={<ImageDetail />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/admin/upload" element={<AdminUpload />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </div>
  );
}

export default App;
