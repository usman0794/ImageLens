import {
  Image as ImageIcon,
  Menu,
  Moon,
  Search,
  Sun,
  UploadCloud,
  X,
} from "lucide-react";
import { useState } from "react";
import { NavLink } from "react-router-dom";
import { useDarkMode } from "../hooks/useDarkMode";

const navItems = [
  { to: "/", label: "Search", icon: Search },
  { to: "/admin/upload", label: "Upload", icon: UploadCloud },
  { to: "/dashboard", label: "Dashboard", icon: ImageIcon },
];

function GitHubIcon({ size = 17 }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="currentColor"
      aria-hidden="true"
    >
      <path d="M12 .5C5.73.5.75 5.6.75 11.98c0 5.08 3.29 9.39 7.86 10.91.57.11.78-.25.78-.56v-2.01c-3.2.71-3.87-1.57-3.87-1.57-.52-1.36-1.28-1.72-1.28-1.72-1.05-.73.08-.72.08-.72 1.16.08 1.77 1.22 1.77 1.22 1.03 1.8 2.71 1.28 3.37.98.1-.76.4-1.28.73-1.57-2.55-.3-5.24-1.3-5.24-5.78 0-1.28.45-2.32 1.19-3.14-.12-.3-.52-1.52.11-3.1 0 0 .98-.32 3.19 1.2A10.8 10.8 0 0 1 12 5.19c.98 0 1.96.13 2.88.39 2.21-1.52 3.18-1.2 3.18-1.2.64 1.58.24 2.8.12 3.1.74.82 1.19 1.86 1.19 3.14 0 4.49-2.69 5.48-5.25 5.77.41.36.78 1.08.78 2.18v3.23c0 .31.2.68.79.56 4.56-1.53 7.84-5.83 7.84-10.9C23.25 5.6 18.27.5 12 .5Z" />
    </svg>
  );
}

function Navbar() {
  const [open, setOpen] = useState(false);
  const { isDark, setIsDark } = useDarkMode();
  const githubUrl = import.meta.env.VITE_GITHUB_URL || "https://github.com/";

  const linkClass = ({ isActive }) =>
    `inline-flex items-center gap-2 rounded-xl px-3 py-2 text-sm font-semibold transition ${
      isActive
        ? "bg-brand-50 text-brand-700 dark:bg-brand-500/15 dark:text-brand-200"
        : "text-slate-600 hover:bg-slate-100 hover:text-slate-950 dark:text-slate-300 dark:hover:bg-slate-800 dark:hover:text-white"
    }`;

  return (
    <header className="sticky top-0 z-40 border-b border-white/70 bg-white/75 backdrop-blur-2xl dark:border-slate-800/80 dark:bg-slate-950/70">
      <nav className="container-page flex h-16 items-center justify-between">
        <NavLink
          to="/"
          className="flex items-center gap-3 font-black tracking-tight text-slate-950 dark:text-white"
        >
          <span className="grid h-10 w-10 place-items-center rounded-2xl bg-brand-600 text-white shadow-glow">
            <ImageIcon size={21} />
          </span>
          <span className="text-lg">ImageLens.io</span>
        </NavLink>

        <div className="hidden items-center gap-2 md:flex">
          {navItems.map(({ to, label, icon: Icon }) => (
            <NavLink key={to} to={to} className={linkClass}>
              <Icon size={16} /> {label}
            </NavLink>
          ))}
        </div>

        <div className="hidden items-center gap-2 md:flex">
          <a
            href={githubUrl}
            target="_blank"
            rel="noreferrer"
            className="btn-secondary !px-4 !py-2"
          >
            <GitHubIcon size={17} /> GitHub
          </a>
          <button
            className="btn-secondary !px-3 !py-2"
            onClick={() => setIsDark(!isDark)}
            aria-label="Toggle dark mode"
          >
            {isDark ? <Sun size={18} /> : <Moon size={18} />}
          </button>
        </div>

        <button
          className="btn-secondary !px-3 !py-2 md:hidden"
          onClick={() => setOpen(!open)}
          aria-label="Toggle menu"
        >
          {open ? <X size={20} /> : <Menu size={20} />}
        </button>
      </nav>

      {open && (
        <div className="container-page pb-4 md:hidden">
          <div className="glass-panel flex flex-col gap-2 p-3">
            {navItems.map(({ to, label, icon: Icon }) => (
              <NavLink
                key={to}
                to={to}
                className={linkClass}
                onClick={() => setOpen(false)}
              >
                <Icon size={16} /> {label}
              </NavLink>
            ))}
            <div className="mt-2 grid grid-cols-2 gap-2">
              <a
                href={githubUrl}
                target="_blank"
                rel="noreferrer"
                className="btn-secondary !px-4 !py-2"
              >
                <GitHubIcon size={17} /> GitHub
              </a>
              <button
                className="btn-secondary !px-3 !py-2"
                onClick={() => setIsDark(!isDark)}
              >
                {isDark ? <Sun size={18} /> : <Moon size={18} />} Theme
              </button>
            </div>
          </div>
        </div>
      )}
    </header>
  );
}

export default Navbar;
