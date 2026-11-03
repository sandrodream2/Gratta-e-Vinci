import { useEffect, useRef, useState } from "react";
import { BrowserMultiFormatReader, BarcodeFormat } from "@zxing/browser";
import { verifyScan, verifySerial } from "../api.js";

function ResultCard({ result }) {
  if (!result) return null;
  return (
    <div
      className={`rounded-xl border p-4 text-sm ${
        result.valid
          ? "bg-emerald-50 border-emerald-300 text-emerald-900"
          : "bg-red-50 border-red-300 text-red-900"
      }`}
    >
      <div className="font-bold mb-1">
        {result.valid ? "✅ " : "❌ "}
        {result.message}
      </div>
      {result.warning && <p className="text-xs mt-2 opacity-90">{result.warning}</p>}
    </div>
  );
}

function ScannerPanel({ onResult }) {
  const videoRef = useRef(null);
  const readerRef = useRef(null);
  const controlsRef = useRef(null);
  const busyRef = useRef(false);
  const [scanning, setScanning] = useState(false);
  const [error, setError] = useState(null);
  const [lastCode, setLastCode] = useState(null);

  const stop = () => {
    controlsRef.current?.stop();
    controlsRef.current = null;
    readerRef.current = null;
    setScanning(false);
  };

  useEffect(() => () => stop(), []); // cleanup allo smontaggio

  const handleDecoded = async (text, formatName) => {
    if (busyRef.current) return;
    busyRef.current = true;
    setLastCode({ text, formatName });
    try {
      const result = await verifyScan(text, formatName);
      onResult(result);
      stop();
    } catch (e) {
      onResult({
        valid: false,
        message: e.message,
        warning: "Riprova a scansionare il codice a barre/QR dopo aver grattato la zona premio.",
      });
    } finally {
      busyRef.current = false;
    }
  };

  const start = async () => {
    setError(null);
    onResult(null);
    try {
      const reader = new BrowserMultiFormatReader();
      readerRef.current = reader;
      const controls = await reader.decodeFromVideoDevice(
        undefined, // fotocamera di default
        videoRef.current,
        (result) => {
          if (result) {
            const formatName = BarcodeFormat[result.getBarcodeFormat()] ?? "unknown";
            void handleDecoded(result.getText(), formatName);
          }
        }
      );
      controlsRef.current = controls;
      setScanning(true);
    } catch (e) {
      const msg =
        e?.name === "NotAllowedError"
          ? "Permesso fotocamera negato. Concedi l'accesso alla fotocamera nelle impostazioni del browser e riprova."
          : `Fotocamera non disponibile: ${e?.message ?? e}`;
      setError(msg);
    }
  };

  return (
    <div>
      <div className="flex flex-wrap gap-2 mb-3">
        {!scanning ? (
          <button
            onClick={start}
            className="bg-emerald-700 text-white rounded-lg px-4 py-2 text-sm font-semibold hover:bg-emerald-800"
          >
            📷 Avvia fotocamera
          </button>
        ) : (
          <button
            onClick={stop}
            className="bg-red-600 text-white rounded-lg px-4 py-2 text-sm font-semibold hover:bg-red-700"
          >
            ⏹ Ferma scanner
          </button>
        )}
      </div>
      {error && (
        <div className="bg-red-100 border border-red-300 text-red-800 rounded-lg px-4 py-3 mb-3 text-sm">
          {error}
        </div>
      )}
      <div className="rounded-xl overflow-hidden border border-slate-300 bg-black max-w-md">
        <video ref={videoRef} className="w-full max-h-80 object-cover" muted playsInline />
      </div>
      <p className="text-xs text-slate-500 mt-2">
        {scanning
          ? "Inquadra il codice a barre/QR sul biglietto (dopo aver grattato la zona premio)…"
          : "La fotocamera si attiva solo con il pulsante e resta sul tuo dispositivo: il codice viene inviato solo al backend locale per la verifica simulata."}
        {lastCode && (
          <span className="block mt-1">
            Ultimo codice letto ({lastCode.formatName}): <code>{lastCode.text}</code>
          </span>
        )}
      </p>
    </div>
  );
}

function ManualPanel({ onResult }) {
  const [serial, setSerial] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setError(null);
    onResult(null);
    setLoading(true);
    try {
      const result = await verifySerial(serial);
      onResult(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={submit} className="max-w-md">
      <label className="block text-sm font-semibold text-slate-600 mb-1">
        Numero di serie del biglietto
      </label>
      <input
        type="text"
        value={serial}
        onChange={(e) => setSerial(e.target.value)}
        placeholder="es. AB1234567890"
        className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm font-mono focus:border-emerald-500 focus:outline-none"
      />
      {error && (
        <div className="bg-red-100 border border-red-300 text-red-800 rounded-lg px-4 py-2 mt-2 text-sm">
          {error}
        </div>
      )}
      <button
        type="submit"
        disabled={loading || !serial.trim()}
        className="mt-3 bg-emerald-700 text-white rounded-lg px-4 py-2 text-sm font-semibold hover:bg-emerald-800 disabled:opacity-50"
      >
        {loading ? "Verifica in corso…" : "Verifica formato"}
      </button>
      <p className="text-xs text-slate-500 mt-2">
        Il controllo è solo formale (10-20 caratteri alfanumerici, almeno 8 cifre). Non verifica
        vincite: per l'esito certo gratta il biglietto e usa l'app ufficiale My Lotteries.
      </p>
    </form>
  );
}

export default function VerifyPage({ meta }) {
  const [mode, setMode] = useState("scan");
  const [result, setResult] = useState(null);

  return (
    <section>
      <h2 className="text-xl font-bold text-slate-800 mb-1">Verifica biglietto</h2>
      <p className="text-sm text-slate-600 mb-4">
        Leggi il codice a barre/QR con la fotocamera oppure inserisci il numero di serie.
        L'esito qui è <strong>simulato / formale</strong>: nessun sistema può dire se un biglietto
        è vincente prima di grattarlo.
      </p>

      <div className="bg-amber-50 border border-amber-300 rounded-xl p-4 mb-6 text-sm text-amber-900">
        {meta?.disclaimer_verify}
      </div>

      <div className="flex gap-2 mb-4">
        {[
          { id: "scan", label: "📷 Scanner (fotocamera)" },
          { id: "manuale", label: "⌨️ Numero di serie manuale" },
        ].map((m) => (
          <button
            key={m.id}
            onClick={() => {
              setMode(m.id);
              setResult(null);
            }}
            className={`rounded-lg px-4 py-2 text-sm font-semibold border ${
              mode === m.id
                ? "bg-emerald-700 text-white border-emerald-700"
                : "bg-white text-slate-700 border-slate-300 hover:bg-slate-50"
            }`}
          >
            {m.label}
          </button>
        ))}
      </div>

      <div className="bg-white rounded-xl shadow p-4 mb-4">
        {mode === "scan" ? (
          <ScannerPanel onResult={setResult} />
        ) : (
          <ManualPanel onResult={setResult} />
        )}
      </div>

      <ResultCard result={result} />
    </section>
  );
}
