// Elemen DOM
const form = document.getElementById("frm");
const cityInput = document.getElementById("city");
const btn = document.getElementById("btn");
const resultEl = document.getElementById("result");
const statusEl = document.getElementById("status");
const msgEl = document.getElementById("msg");

// Simpan state HTML asli tombol untuk dipulihkan setelah loading
const BTN_ORIGINAL_HTML = btn.innerHTML;

// ---------- UI Helpers ----------
function setLoading(isLoading) {
  if (isLoading) {
    btn.disabled = true;
    btn.innerHTML = `<span class="inline-flex items-center gap-2">
      <i class="fas fa-spinner fa-spin"></i> <span>Loading...</span>
    </span>`;
    showStatus("Mengambil data cuaca…", "info");
  } else {
    btn.disabled = false;
    btn.innerHTML = BTN_ORIGINAL_HTML;
    hideStatus();
  }
}

function showStatus(msg, type = "info") {
  statusEl.classList.remove("hidden");
  statusEl.textContent = msg;
  statusEl.className =
    "mb-4 p-3 rounded-xl border " +
    (type === "error"
      ? "bg-red-50 border-red-200 text-red-800"
      : type === "info"
      ? "bg-blue-50 border-blue-200 text-blue-800"
      : "bg-yellow-50 border-yellow-200 text-yellow-800");
}

function hideStatus() {
  statusEl.classList.add("hidden");
}

// Flash message yang auto-hide
function flash(msg, type = "info", timeout = 2500) {
  const base =
    "text-sm text-center mb-4 py-2 rounded-md transition-opacity duration-300 ";
  const styles =
    type === "error"
      ? "bg-red-50 text-red-800 border border-red-200"
      : type === "success"
      ? "bg-green-50 text-green-800 border border-green-200"
      : "bg-yellow-50 text-yellow-800 border border-yellow-200";

  msgEl.className = base + styles;
  msgEl.textContent = msg;
  msgEl.classList.remove("hidden", "opacity-0");

  // Auto fade out
  setTimeout(() => {
    msgEl.classList.add("opacity-0");
    setTimeout(() => {
      msgEl.classList.add("hidden");
    }, 300);
  }, timeout);
}

// ---------- Icon Helpers ----------
// Peta ikon kondisi (description bisa ID atau EN)
function conditionIcon(description = "") {
  const d = String(description).toLowerCase();

  const isClear = d.includes("cerah") || d.includes("clear");
  const isCloud =
    d.includes("mendung") || d.includes("berawan") || d.includes("cloud");
  const isHeavy =
    d.includes("hujan deras") ||
    d.includes("hujan lebat") ||
    d.includes("heavy") ||
    d.includes("thunderstorm") ||
    d.includes("storm");
  const isRain =
    d.includes("hujan") || d.includes("rain") || d.includes("drizzle");

  if (isClear) return `<i class="fas fa-sun"></i>`;
  if (isHeavy) return `<i class="fas fa-cloud-showers-heavy"></i>`;
  if (isRain) return `<i class="fas fa-cloud-rain"></i>`;
  if (isCloud) return `<i class="fas fa-cloud"></i>`;
  // default fallback
  return `<i class="fas fa-cloud"></i>`;
}

function timeIcon(labelLower) {
  if (labelLower === "pagi") return `<i class="fas fa-coffee"></i>`;
  if (labelLower === "siang") return `<i class="fas fa-sun"></i>`;
  if (labelLower === "malam") return `<i class="fas fa-moon"></i>`;
  return "";
}

// ---------- View ----------
function card(day) {
  const { date, weekday, temps, description } = day;
  const dateFmt = new Date(date).toLocaleDateString("id-ID", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });

  const tempItem = (label, val) => `
    <div class="flex items-center justify-between text-sm">
      <span class="text-gray-700 inline-flex items-center gap-2">
        ${timeIcon(label.toLowerCase())} ${label}
      </span>
      <span class="font-semibold">${val !== null ? `${val}°C` : "-"}</span>
    </div>
  `;

  return `
    <article class="rounded-2xl bg-white shadow-sm border border-gray-100 p-4">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-lg font-semibold">${weekday}</h3>
          <p class="text-xs text-gray-500">${dateFmt}</p>
        </div>
        <div class="text-xl">${conditionIcon(description)}</div>
      </div>
      <p class="mt-2 text-sm capitalize">${description || ""}</p>
      <div class="mt-4 space-y-2">
        ${tempItem("Pagi", temps.morning)}
        ${tempItem("Siang", temps.day)}
        ${tempItem("Malam", temps.night)}
      </div>
    </article>
  `;
}

// ---------- Data Fetch ----------
async function fetchForecast(city) {
  setLoading(true);
  resultEl.innerHTML = "";

  try {
    const res = await fetch(`/api/forecast?city=${encodeURIComponent(city)}`, {
      headers: { "Cache-Control": "no-cache" },
    });
    const data = await res.json();

    if (!res.ok) {
      throw new Error(data?.error || "Gagal mengambil data.");
    }

    // Header kecil di atas grid
    const header = document.createElement("div");
    header.className = "col-span-full mb-2";
    header.innerHTML = `
      <h2 class="text-sm text-gray-700">
        Kota: <span class="font-semibold">${data.city}</span>, <span class="font-mono">ID</span>
      </h2>`;
    resultEl.appendChild(header);

    if (!data.days || data.days.length === 0) {
      flash("Tidak ada data prakiraan untuk tiga hari ke depan.", "info");
      return;
    }

    // Render tepat 3 kartu (hari ini, besok, lusa) jika tersedia
    data.days.slice(0, 3).forEach((d) => {
      const wrapper = document.createElement("div");
      wrapper.innerHTML = card(d);
      resultEl.appendChild(wrapper.firstElementChild);
    });

    flash("Data cuaca berhasil dimuat.", "success");
  } catch (err) {
    flash(err.message || "Terjadi kesalahan tidak diketahui.", "error");
  } finally {
    setLoading(false);
  }
}

// ---------- Events ----------
form.addEventListener("submit", (e) => {
  e.preventDefault();
  const city = cityInput.value.trim();
  if (!city) {
    flash("Masukkan nama kota terlebih dahulu.", "info");
    return;
  }
  fetchForecast(city);
});

// automatic load on first paint
window.addEventListener("DOMContentLoaded", () => {
  if (!cityInput.value) cityInput.value = "Jakarta";
  fetchForecast(cityInput.value);
});
