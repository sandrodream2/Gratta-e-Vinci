import { useEffect, useState } from "react";
import { getMeta } from "./api.js";
import Banner from "./components/Banner.jsx";
import CatalogPage from "./components/CatalogPage.jsx";
import StatsPage from "./components/StatsPage.jsx";
import VerifyPage from "./components/VerifyPage.jsx";
import SourcesPage from "./components/SourcesPage.jsx";

const TABS = [
  { id: "catalogo", label: "Catalogo giochi" },
  { id: "stats", label: "Dove si vince di più?" },
  { id: "verifica", label: "Verifica biglietto" },
  { id: "fonti", label: "Fonti & avvertenze" },
];

export default function App() {
  const [tab, setTab] = useState("catalogo");
  const [meta, setMeta] = useState(null);

  useEffect(() => {
    getMeta().then(setMeta).catch(() => setMeta(null));
  }, []);

  return (
    <div className="min-h-screen flex flex-col">
      <Banner text={meta?.disclaimer_banner} />

      <header className="bg-emerald-800 text-white shadow">
        <div className="max-w-6xl mx-auto px-4 py-4 flex flex-wrap items-center gap-3">
          <h1 className="text-2xl font-bold tracking-tight">GrattaData</h1>
          <span className="text-emerald-200 text-sm">
            probabilità ufficiali dei Gratta e Vinci (fonte ADM) — non predittivo
          </span>
        </div>
        <nav className="max-w-6xl mx-auto px-4 flex flex-wrap gap-1">
          {TABS.map((t) => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={`px-4 py-2 text-sm font-medium rounded-t-lg transition-colors ${
                tab === t.id
                  ? "bg-slate-100 text-emerald-900"
                  : "text-emerald-100 hover:bg-emerald-700"
              }`}
            >
              {t.label}
            </button>
          ))}
        </nav>
      </header>

      <main className="flex-1 max-w-6xl w-full mx-auto px-4 py-6">
        {tab === "catalogo" && <CatalogPage meta={meta} />}
        {tab === "stats" && <StatsPage meta={meta} />}
        {tab === "verifica" && <VerifyPage meta={meta} />}
        {tab === "fonti" && <SourcesPage meta={meta} />}
      </main>

      <footer className="bg-slate-800 text-slate-300 text-xs">
        <div className="max-w-6xl mx-auto px-4 py-4 flex flex-wrap gap-x-6 gap-y-1">
          <span>Gioco vietato ai minori di 18 anni. Gioca responsabilmente.</span>
          <span>GrattaData è uno strumento informativo: non promette vincite né "biglietti fortunati".</span>
          {meta?.links?.mylotteries_app && (
            <a
              className="underline hover:text-white"
              href={meta.links.mylotteries_app}
              target="_blank"
              rel="noreferrer"
            >
              App ufficiale My Lotteries
            </a>
          )}
        </div>
      </footer>
    </div>
  );
}
