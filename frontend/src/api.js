// Client HTTP per il backend GrattaData.
// In sviluppo il proxy di Vite gira /api verso http://localhost:8000;
// in produzione il backend FastAPI serve direttamente il build statico.

async function request(path, options = {}) {
  let res;
  try {
    res = await fetch(path, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
  } catch {
    throw new Error(
      "Backend non raggiungibile: avvia il server FastAPI (porta 8000), vedi README.md."
    );
  }
  let data = null;
  try {
    data = await res.json();
  } catch {
    // risposta senza body JSON: ignora
  }
  if (!res.ok) {
    const detail = data?.detail;
    let message;
    if (Array.isArray(detail)) {
      message = detail.map((d) => d.msg ?? JSON.stringify(d)).join("; ");
    } else if (typeof detail === "string") {
      message = detail;
    } else if (detail?.reasons) {
      message = [detail.message, ...detail.reasons].filter(Boolean).join(" ");
    } else if (detail?.message) {
      message = detail.message;
    } else {
      message = `Errore HTTP ${res.status}`;
    }
    throw new Error(message);
  }
  return data;
}

export function getMeta() {
  return request("/api/meta");
}

export function getGames(params = {}) {
  const qs = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value !== "" && value !== null && value !== undefined) qs.set(key, value);
  }
  return request(`/api/games?${qs.toString()}`);
}

export function getPrices() {
  return request("/api/games/meta/prices");
}

export function getOverview() {
  return request("/api/stats/overview");
}

export function getWhereWins(limit = 10) {
  return request(`/api/stats/where-wins?limit=${limit}`);
}

export function verifySerial(serial) {
  return request("/api/verify/serial", {
    method: "POST",
    body: JSON.stringify({ serial }),
  });
}

export function verifyScan(code, codeType) {
  return request("/api/verify/scan", {
    method: "POST",
    body: JSON.stringify({ code, code_type: codeType }),
  });
}
