// Banner di trasparenza mostrato in TUTTE le pagine.
const FALLBACK =
  "Le probabilità sono casuali e uguali ovunque. Nessuna app può prevedere se un biglietto è vincente prima di grattarlo.";

export default function Banner({ text }) {
  return (
    <div className="bg-amber-400 text-amber-950">
      <div className="max-w-6xl mx-auto px-4 py-2 flex items-center gap-2 text-sm font-semibold">
        <span aria-hidden="true">⚠️</span>
        <p>{text ?? FALLBACK}</p>
      </div>
    </div>
  );
}
