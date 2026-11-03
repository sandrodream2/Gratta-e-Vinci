import { useEffect, useState } from "react";
import { getOverview, getWhereWins } from "../api.js";

export default function StatsPage({ meta }) {
  const [overview, setOverview] = useState(null);
  const [whereWins, setWhereWins] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([getOverview(), getWhereWins(10)])
      .then(([o, w]) => {
        setOverview(o);
        setWhereWins(w);
      })
      .catch((e) => setError(e.message));
  }, []);

  const maxWins = whereWins?.rows?.length
    ? Math.max(...whereWins.rows.map((r) => r.wins_recorded))
    : 1;

  return (
    <section>
      <h2 className="text-xl font-bold text-slate-800 mb-1">Dove si vince di più?</h2>
      <p className="text-sm text-slate-600 mb-4">
        Statistiche aggregate (dati di esempio) sui punti vendita: più biglietti venduti = più
        probabilità che escano premi. È una <strong>correlazione statistica, non una predizione</strong>.
      </p>

      {error && (
        <div className="bg-red-100 border border-red-300 text-red-800 rounded-lg px-4 py-3 mb-4 text-sm">
          {error}
        </div>
      )}

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
        <div className="bg-white rounded-xl shadow p-4">
          <div className="text-xs text-slate-500 font-semibold">Giochi attivi nel catalogo</div>
          <div className="text-2xl font-bold text-emerald-700">{overview?.games_count ?? "…"}</div>
        </div>
        <div className="bg-white rounded-xl shadow p-4">
          <div className="text-xs text-slate-500 font-semibold">Probabilità media ufficiale (ADM)</div>
          <div className="text-2xl font-bold text-emerald-700">
            {meta?.official_average_label ?? "1 su 3,60"}
          </div>
        </div>
        <div className="bg-white rounded-xl shadow p-4">
          <div className="text-xs text-slate-500 font-semibold">Restituzione media in vincite</div>
          <div className="text-2xl font-bold text-emerald-700">
            fino al {overview?.payout_max_percent ?? 75}%
          </div>
        </div>
        <div className="bg-white rounded-xl shadow p-4">
          <div className="text-xs text-slate-500 font-semibold">Migliore probabilità del catalogo</div>
          <div className="text-2xl font-bold text-emerald-700">
            {overview?.best_odds_win_label ?? "…"}
          </div>
        </div>
      </div>

      <div className="bg-amber-50 border border-amber-300 rounded-xl p-4 mb-6 text-sm text-amber-900">
        <strong>Attenzione:</strong> {whereWins?.disclaimer ?? meta?.disclaimer_stats}
      </div>

      <div className="bg-white rounded-xl shadow overflow-hidden">
        <table className="min-w-full text-sm">
          <thead className="bg-slate-100 text-slate-600">
            <tr>
              <th className="text-left px-4 py-3 font-semibold">Punto vendita</th>
              <th className="text-left px-4 py-3 font-semibold">Città</th>
              <th className="text-right px-4 py-3 font-semibold">Biglietti venduti</th>
              <th className="text-right px-4 py-3 font-semibold">Vincite registrate</th>
              <th className="text-left px-4 py-3 font-semibold w-40">Distribuzione</th>
            </tr>
          </thead>
          <tbody>
            {whereWins?.rows?.map((r) => (
              <tr key={r.name + r.city} className="border-t border-slate-100">
                <td className="px-4 py-3 font-medium text-slate-800">{r.name}</td>
                <td className="px-4 py-3 text-slate-600">
                  {r.city} ({r.region})
                </td>
                <td className="px-4 py-3 text-right tabular-nums">
                  {r.tickets_sold.toLocaleString("it-IT")}
                </td>
                <td className="px-4 py-3 text-right tabular-nums font-semibold text-emerald-700">
                  {r.wins_recorded.toLocaleString("it-IT")}
                  <span className="block text-xs font-normal text-slate-500">
                    {r.wins_per_1000.toLocaleString("it-IT")} ogni 1.000 biglietti
                  </span>
                </td>
                <td className="px-4 py-3">
                  <div className="h-3 w-full bg-slate-100 rounded">
                    <div
                      className="h-3 bg-emerald-500 rounded"
                      style={{ width: `${(r.wins_recorded / maxWins) * 100}%` }}
                    />
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {whereWins && (
          <p className="px-4 py-3 text-xs text-slate-500 border-t border-slate-100">
            {whereWins.rows[0]?.data_note}. Questi dati non indicano dove "conviene" comprare: la
            probabilità di ogni singolo biglietto è casuale e identica ovunque.
          </p>
        )}
      </div>

      <div className="bg-red-50 border border-red-300 rounded-xl p-4 mt-6 text-sm text-red-900">
        <strong>È impossibile prevedere i biglietti vincenti.</strong>{" "}
        {meta?.no_lucky_numbers ??
          "Non esistono lotti fortunati o numeri di serie vincenti prevedibili prima di grattare."}
      </div>
    </section>
  );
}
