import { useEffect, useState } from "react";
import { getGames, getPrices } from "../api.js";

const SORTS = [
  { value: "price", label: "Prezzo" },
  { value: "odds_win", label: "Probabilità di vincita" },
  { value: "odds_top", label: "Probabilità premio max" },
  { value: "top_prize", label: "Premio massimo" },
  { value: "name", label: "Nome" },
];

const COLUMNS = [
  { key: "name", label: "Gioco", sortable: true },
  { key: "price", label: "Prezzo", sortable: true },
  { key: "odds_win", label: "Prob. vincita (premi > costo)", sortable: true },
  { key: "odds_top", label: "Prob. premio max", sortable: true },
  { key: "top_prize", label: "Premio max", sortable: true },
  { key: "source", label: "Fonte ufficiale", sortable: false },
];

function formatPrice(p) {
  return p % 1 === 0 ? `${p} €` : `${p.toFixed(2).replace(".", ",")} €`;
}

export default function CatalogPage({ meta }) {
  const [games, setGames] = useState([]);
  const [prices, setPrices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [q, setQ] = useState("");
  const [priceMax, setPriceMax] = useState("");
  const [maxOdds, setMaxOdds] = useState("");
  const [sort, setSort] = useState("price");
  const [order, setOrder] = useState("asc");

  useEffect(() => {
    getPrices().then(setPrices).catch(() => setPrices([]));
  }, []);

  useEffect(() => {
    setLoading(true);
    setError(null);
    getGames({ q, price_max: priceMax, max_odds: maxOdds, sort, order })
      .then(setGames)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [q, priceMax, maxOdds, sort, order]);

  const toggleSort = (key) => {
    if (sort === key) {
      setOrder((o) => (o === "asc" ? "desc" : "asc"));
    } else {
      setSort(key);
      setOrder("asc");
    }
  };

  return (
    <section>
      <div className="mb-4">
        <h2 className="text-xl font-bold text-slate-800">Catalogo dei Gratta e Vinci attivi</h2>
        <p className="text-sm text-slate-600 mt-1">
          Probabilità ufficiali pubblicate da ADM (premi superiori al costo della giocata).{" "}
          {meta?.data_note ??
            "Verifica sempre la scheda ufficiale di ciascun gioco su adm.gov.it."}
        </p>
      </div>

      <div className="bg-white rounded-xl shadow p-4 mb-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        <label className="block">
          <span className="text-xs font-semibold text-slate-500">Cerca per nome</span>
          <input
            type="text"
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="es. Miliardario"
            className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-emerald-500 focus:outline-none"
          />
        </label>
        <label className="block">
          <span className="text-xs font-semibold text-slate-500">Prezzo massimo</span>
          <select
            value={priceMax}
            onChange={(e) => setPriceMax(e.target.value)}
            className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-emerald-500 focus:outline-none"
          >
            <option value="">Tutti i prezzi</option>
            {prices.map((p) => (
              <option key={p} value={p}>
                fino a {formatPrice(p)}
              </option>
            ))}
          </select>
        </label>
        <label className="block">
          <span className="text-xs font-semibold text-slate-500">
            Probabilità minima (1 su N, es. 8)
          </span>
          <input
            type="number"
            min="1"
            step="0.01"
            value={maxOdds}
            onChange={(e) => setMaxOdds(e.target.value)}
            placeholder="es. 8 = almeno 1 su 8"
            className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-emerald-500 focus:outline-none"
          />
        </label>
        <label className="block">
          <span className="text-xs font-semibold text-slate-500">Ordina per</span>
          <div className="mt-1 flex gap-2">
            <select
              value={sort}
              onChange={(e) => setSort(e.target.value)}
              className="flex-1 rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-emerald-500 focus:outline-none"
            >
              {SORTS.map((s) => (
                <option key={s.value} value={s.value}>
                  {s.label}
                </option>
              ))}
            </select>
            <button
              onClick={() => setOrder((o) => (o === "asc" ? "desc" : "asc"))}
              className="rounded-lg border border-slate-300 px-3 py-2 text-sm hover:bg-slate-100"
              title="Inverti ordinamento"
            >
              {order === "asc" ? "↑ cresc." : "↓ decr."}
            </button>
          </div>
        </label>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-300 text-red-800 rounded-lg px-4 py-3 mb-4 text-sm">
          {error}
        </div>
      )}

      <div className="bg-white rounded-xl shadow overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead className="bg-slate-100 text-slate-600">
            <tr>
              {COLUMNS.map((c) => (
                <th key={c.key} className="text-left px-4 py-3 font-semibold whitespace-nowrap">
                  {c.sortable ? (
                    <button onClick={() => toggleSort(c.key)} className="hover:text-emerald-700">
                      {c.label}
                      {sort === c.key && (order === "asc" ? " ▲" : " ▼")}
                    </button>
                  ) : (
                    c.label
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {loading && (
              <tr>
                <td colSpan={COLUMNS.length} className="px-4 py-8 text-center text-slate-500">
                  Caricamento…
                </td>
              </tr>
            )}
            {!loading && games.length === 0 && (
              <tr>
                <td colSpan={COLUMNS.length} className="px-4 py-8 text-center text-slate-500">
                  Nessun gioco trovato con i filtri actuelles.
                </td>
              </tr>
            )}
            {!loading &&
              games.map((g) => (
                <tr key={g.id} className="border-t border-slate-100 hover:bg-emerald-50/50">
                  <td className="px-4 py-3 font-medium text-slate-800">
                    {g.name}
                    {g.notes && (
                      <div className="text-xs font-normal text-slate-500 mt-0.5">{g.notes}</div>
                    )}
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap">{formatPrice(g.price)}</td>
                  <td className="px-4 py-3 whitespace-nowrap font-semibold text-emerald-700">
                    {g.odds_win_label ?? "—"}
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap">{g.odds_top_label ?? "—"}</td>
                  <td className="px-4 py-3 whitespace-nowrap font-semibold">
                    {g.top_prize_label ?? "—"}
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap">
                    <a
                      href={g.source_url}
                      target="_blank"
                      rel="noreferrer"
                      className="text-emerald-700 underline hover:text-emerald-900"
                    >
                      {g.source_label}
                    </a>
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>

      <p className="text-xs text-slate-500 mt-3">
        In media, su tutti i Gratta e Vinci in vendita, un biglietto paga un premio (superiore al costo)
        ogni {meta?.official_average_label ?? "1 su 3,60"} — dato ufficiale ADM. La probabilità è
        identica in ogni punto vendita: non esistono zone o lotti "fortunati".
      </p>
    </section>
  );
}
