import { Gauge, Images, Layers3, Search } from "lucide-react";
import { useEffect, useState } from "react";
import { fetchDashboardAnalytics } from "../api/imageLensApi";
import DashboardCharts from "../components/DashboardCharts";

const statCards = [
  { key: "totalImages", label: "Total images", icon: Images, suffix: "" },
  { key: "searches", label: "Searches", icon: Search, suffix: "" },
  { key: "categories", label: "Categories", icon: Layers3, suffix: "" },
  { key: "avgLatency", label: "Avg latency", icon: Gauge, suffix: "ms" },
];

function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchDashboardAnalytics().then(setData);
  }, []);

  const metrics = data?.metrics || {};

  return (
    <main className="container-page py-8">
      <div className="mb-8">
        <p className="text-sm font-bold uppercase tracking-wider text-brand-600 dark:text-brand-300">
          Dashboard
        </p>
        <h1 className="text-3xl font-black tracking-tight text-slate-950 dark:text-white">
          ImageLens analytics
        </h1>
        <p className="mt-2 text-slate-600 dark:text-slate-300">
          Track indexed images, search volume, categories, and response latency.
        </p>
      </div>

      <div className="mb-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {statCards.map(({ key, label, icon: Icon, suffix }) => (
          <article key={key} className="glass-panel p-5">
            <div className="mb-4 grid h-12 w-12 place-items-center rounded-2xl bg-brand-100 text-brand-700 dark:bg-brand-500/15 dark:text-brand-200">
              <Icon size={22} />
            </div>
            <p className="text-sm font-semibold text-slate-500 dark:text-slate-400">
              {label}
            </p>
            <p className="mt-1 text-3xl font-black text-slate-950 dark:text-white">
              {(metrics[key] ?? 0).toLocaleString()}
              {suffix}
            </p>
          </article>
        ))}
      </div>

      <DashboardCharts
        searchesOverTime={data?.searchesOverTime}
        topCategories={data?.topCategories}
      />
    </main>
  );
}

export default Dashboard;
