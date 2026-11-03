const LINK_LABELS = {
  adm_lotterie_istananee: "ADM – Elenco lotterie istantanee (Gratta e Vinci) attive",
  adm_note_probabilita: "ADM – Note informative sulle probabilità di vincita (1 su 3,60 in media)",
  concessionario_probabilita: "Portale ufficiale del concessionario – Probabilità di vincita",
  mylotteries_app: "App ufficiale My Lotteries (verifica vincite dopo aver grattato)",
  gioco_responsabile: "ADM – Gioco responsabile",
};

export default function SourcesPage({ meta }) {
  const links = meta?.links ?? {};
  return (
    <section>
      <h2 className="text-xl font-bold text-slate-800 mb-1">Fonti ufficiali & avvertenze</h2>
      <p className="text-sm text-slate-600 mb-4">
        GrattaData usa solo fonti pubbliche ufficiali. Le probabilità mostrate sono quelle
        pubblicate da ADM nei regolamenti di ciascun gioco.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-6">
        {Object.entries(links).map(([key, url]) => (
          <a
            key={key}
            href={url}
            target="_blank"
            rel="noreferrer"
            className="bg-white rounded-xl shadow p-4 hover:shadow-md hover:bg-emerald-50/50 transition"
          >
            <div className="font-semibold text-emerald-700">
              {LINK_LABELS[key] ?? key} ↗
            </div>
            <div className="text-xs text-slate-500 break-all mt-1">{url}</div>
          </a>
        ))}
      </div>

      <div className="bg-amber-50 border border-amber-300 rounded-xl p-4 mb-4 text-sm text-amber-900">
        <strong>Banner di trasparenza (presente in ogni pagina):</strong>
        <p className="mt-1">{meta?.disclaimer_banner}</p>
      </div>

      <div className="bg-red-50 border border-red-300 rounded-xl p-4 mb-4 text-sm text-red-900">
        <strong>Limite invalicabile:</strong>
        <p className="mt-1">{meta?.no_lucky_numbers}</p>
      </div>

      <div className="bg-white rounded-xl shadow p-4 text-sm text-slate-700">
        <strong>Come leggere le probabilità.</strong>
        <ul className="list-disc ml-5 mt-2 space-y-1">
          <li>
            La probabilità ufficiale (es. "1 su 7,84") conta i biglietti con premi{" "}
            <em>superiori al costo</em> sul totale del lotto, come stabilito dal decreto di
            indizione pubblicato da ADM.
          </li>
          <li>
            In media su tutti i giochi attivi un premio esce ogni{" "}
            {meta?.official_average_label ?? "1 su 3,60"}; la restituzione media in vincite può
            raggiungere il {meta?.payout_max_percent ?? 75}% dell'incasso complessivo.
          </li>
          <li>
            Un biglietto vincente può contenere più premi: il numero dei premi non coincide con il
            numero di biglietti vincenti.
          </li>
          <li>
            La distribuzione dei vincenti è casuale e identica ovunque: la tabaccheria, l'orario o
            i biglietti già usciti non cambiano le probabilità del prossimo biglietto.
          </li>
        </ul>
        <p className="text-xs text-slate-500 mt-3">{meta?.data_note}</p>
      </div>

      <p className="text-xs text-slate-500 mt-4">
        Gioco vietato ai minori di 18 anni. Il gioco può causare dipendenza patologica: gioca
        responsabilmente e solo quanto puoi permetterti di perdere.
      </p>
    </section>
  );
}
