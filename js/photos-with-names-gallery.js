/* js/photos-with-names-gallery.js
   Gallery driven by people-index.json (from people-data.js)

   Expects in gallery.html:
     - input#gallery-filter
     - div#gallery-grid
     - span#gallery-count
*/

(() => {
  "use strict";

  // ---- CONFIG (paths are relative to gallery.html in repo root) ----
  const INDEX_URL = "photos-with-names/people-index.json";
  const THUMB_BASE = "photos-with-names/thumbnails/";
  const FULL_BASE  = "photos-with-names/full/";

  // ---- DOM ----
  const $ = (sel) => document.querySelector(sel);
  const searchEl = $("#gallery-filter");
  const gridEl   = $("#gallery-grid");
  const statusEl = $("#gallery-count"); // we use this as the status/count line

  function setStatus(msg) {
    if (statusEl) statusEl.textContent = msg || "";
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({
      "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;"
    }[c]));
  }

  function showError(msg) {
    console.error(msg);
    if (!gridEl) return;
    gridEl.innerHTML = `
      <div class="gallery-error" style="border:2px solid pink; background:#FFF0F5; padding:12px; border-radius:10px;">
        <strong>Gallery error:</strong>
        <div style="margin-top:6px;">${escapeHtml(msg)}</div>
        <div style="margin-top:10px; font-size:0.95em;">
          Check that <code>${INDEX_URL}</code> exists and that your folder paths match.
        </div>
      </div>`;
    setStatus("");
  }

  function normaliseText(s) {
    return String(s || "")
      .toLowerCase()
      .replace(/\s+/g, " ")
      .trim();
  }

  // Year extraction rule:
  // Find first 4-digit year 1800–2099 anywhere in filename (handles School1948a.jpg etc.)
  function extractYearFromFilename(filename) {
    const m = String(filename || "").match(/\b(18\d{2}|19\d{2}|20\d{2})\b/);
    return m ? m[1] : "";
  }

  function resolveFile(item) {
    // Your index should have photoFile
    return item.photoFile || item.file || item.filename || "";
  }

  function resolveTitle(item, file) {
    // Prefer "Surname — FullName" if available, otherwise fallback to file
    const surname = item.surname ? String(item.surname).trim() : "";
    const fullName = item.fullName ? String(item.fullName).trim() : "";
    if (surname && fullName) return `${surname} — ${fullName}`;
    if (fullName) return fullName;
    if (surname) return surname;
    return file || "Photo";
  }

  function getSearchText(item) {
    const file = resolveFile(item);
    const year = extractYearFromFilename(file);

    const bits = [
      item.surname || "",
      item.fullName || "",
      file || "",
      year || ""
    ];

    return normaliseText(bits.join(" "));
  }

  function makeCard(item) {
    const file = resolveFile(item);
    if (!file) return null;

    const thumbUrl = THUMB_BASE + encodeURIComponent(file);
    const fullUrl  = FULL_BASE  + encodeURIComponent(file);

    const year = extractYearFromFilename(file);
    const title = resolveTitle(item, file);
    const caption = year ? `${title} (${year})` : title;

    const a = document.createElement("a");
    a.className = "gallery-item";
    a.href = fullUrl;
    a.target = "_blank";
    a.rel = "noopener";

    const img = document.createElement("img");
    img.loading = "lazy";
    img.src = thumbUrl;
    img.alt = caption;

    // If thumbnail missing, fall back to full image
    img.addEventListener("error", () => {
      img.src = fullUrl;
    });

    const cap = document.createElement("div");
    cap.className = "gallery-caption";
    cap.textContent = caption;

    a.appendChild(img);
    a.appendChild(cap);

    return a;
  }

  function render(items, query) {
    if (!gridEl) return;

    const q = normaliseText(query);

    const filtered = !q
      ? items
      : items.filter((it) => getSearchText(it).includes(q));

    gridEl.innerHTML = "";
    const frag = document.createDocumentFragment();

    for (const item of filtered) {
      const card = makeCard(item);
      if (card) frag.appendChild(card);
    }

    gridEl.appendChild(frag);
    setStatus(`${filtered.length} / ${items.length} entries`);
  }

  async function loadIndex() {
    setStatus("Loading…");

    let resp;
    try {
      resp = await fetch(INDEX_URL, { cache: "no-store" });
    } catch (e) {
      showError(`Could not fetch ${INDEX_URL}. (${e})`);
      return null;
    }

    if (!resp.ok) {
      showError(`Fetch failed for ${INDEX_URL}: HTTP ${resp.status} ${resp.statusText}`);
      return null;
    }

    let data;
    try {
      data = await resp.json();
    } catch (e) {
      showError(`JSON parse error in ${INDEX_URL}: ${e}`);
      return null;
    }

    if (!Array.isArray(data)) {
      showError(`Unexpected JSON structure in ${INDEX_URL}. Expected an array.`);
      return null;
    }

    return data;
  }

  function debounce(fn, ms = 120) {
    let t = null;
    return (...args) => {
      clearTimeout(t);
      t = setTimeout(() => fn(...args), ms);
    };
  }

  async function init() {
    if (!gridEl) {
      console.warn("No #gallery-grid element found — nothing to render.");
      return;
    }

    const items = await loadIndex();
    if (!items) return;

    render(items, "");

    if (searchEl) {
      const onInput = debounce(() => render(items, searchEl.value), 120);
      searchEl.addEventListener("input", onInput);
    }
  }

  document.addEventListener("DOMContentLoaded", init);
})();
