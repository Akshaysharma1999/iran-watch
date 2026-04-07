function pad2(n) {
  return String(n).padStart(2, "0");
}

function formatLocal(dt) {
  try {
    return new Intl.DateTimeFormat(undefined, {
      year: "numeric",
      month: "short",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    }).format(dt);
  } catch {
    return dt.toLocaleString();
  }
}

function nextTopOfHour(now) {
  const t = new Date(now);
  t.setMinutes(60, 0, 0);
  return t;
}

async function loadData() {
  // Cache-bust to avoid stale CDN copies.
  const res = await fetch(`./data.json?ts=${Date.now()}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`Failed to fetch data.json: ${res.status}`);
  return await res.json();
}

function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}

function setLink(id, href, text) {
  const el = document.getElementById(id);
  if (!el) return;
  el.href = href || "#";
  el.textContent = text || href || "—";
  if (!href) el.style.pointerEvents = "none";
}

function render(data) {
  setText("keyword", data.keyword || "IRAN");

  const updatedAt = data.updated_at ? new Date(data.updated_at) : null;
  setText("updatedAt", updatedAt ? formatLocal(updatedAt) : "—");

  setLink("sourceUrl", data.source?.feed_url, data.source?.feed_url);

  const lastSeenAt = data.last_match?.published_at ? new Date(data.last_match.published_at) : null;
  setText("lastSeenAt", lastSeenAt ? formatLocal(lastSeenAt) : "No match found yet");

  setText("lastText", data.last_match?.text || "");
  setLink("lastUrl", data.last_match?.url, data.last_match?.url ? "Open source post" : "No source link");
}

function startCountdown() {
  const tick = () => {
    const now = new Date();
    const next = nextTopOfHour(now);
    const ms = Math.max(0, next.getTime() - now.getTime());
    const totalSec = Math.floor(ms / 1000);
    const h = Math.floor(totalSec / 3600);
    const m = Math.floor((totalSec % 3600) / 60);
    const s = totalSec % 60;
    setText("nextCheck", `${pad2(h)}:${pad2(m)}:${pad2(s)}`);
    setText("nextCheckAt", `Next check at ${formatLocal(next)}`);
  };

  tick();
  setInterval(tick, 250);
}

async function init() {
  startCountdown();

  try {
    const data = await loadData();
    render(data);
  } catch (e) {
    setText("lastSeenAt", "Failed to load data.json");
    setText("lastText", String(e));
  }

  // Soft-refresh the JSON every 60s so the page updates soon after the hourly job runs.
  setInterval(async () => {
    try {
      const data = await loadData();
      render(data);
    } catch {
      // ignore
    }
  }, 60_000);
}

init();
