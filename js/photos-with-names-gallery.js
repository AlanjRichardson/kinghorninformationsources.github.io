/* js/photos-with-names-gallery.js
   Gallery loader for:
     photos-with-names/photos.json
     photos-with-names/thumbnails/<file>
     photos-with-names/full/<file>

   Expects in gallery.html:
     - input#gallery-filter
     - div#gallery-grid
     - span#gallery-count
*/

(() => {
  "use strict";

  // ---- CONFIG ----
  const JSON_URL   = "photos-with-names/photos.json";
  const THUMB_BASE = "photos-with-names/thumbnails/";
  const FULL_BASE  = "photos-with-names/full/";

  // If your JSON uses different field names, add them here.
  const TEXT_FIELDS = ["title", "caption", "desc", "description", "text", "label", "name"];

  // ---- DOM ----
  const $ = (sel) => document.querySelector(sel);

  const searchEl = $("#gallery-filter");
  const gridEl   = $("#gallery-grid");
  const statusEl = $("#gallery-count"); // show "x / y photos" here

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
          Check that <code>${JSON_URL}</code> exists and paths match your repo structure.
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

  function getItemText(item) {
    const bits = [];
    if (item.filename) bits.push(item.filename);
    if (item.file) bits.push(item.file);
    if (item.name) bits.push(item.name);

    for (const f of TEXT_FIELDS) {
      if (item[f]) bits.push(item[f]);
    }

    if (item.meta && typeof item.meta === "object") {
      for (const f of TEXT_FIELDS) {
        if (item.meta[f]) bits.push(item.meta[f]);
      }
    }

    return normaliseText(bits.join(" "));
  }

  function resolveFilename(item) {
    return item.filename || item.file || item.name || item.image || "";
  }

  function resolveTitle(item, fallbackFilename) {
    for (const f of ["title", "caption", "description", "desc", "text", "label"]) {
      if (item[f]) return String(item[f]);
    }
    if (item.meta && typeof item.meta === "object") {
      for (const f of ["title", "caption", "description", "desc", "text", "label"]) {
        if (item.meta[f]) return String(item.meta[f]);
      }
    }
    return fallbackFilename || "Photo";
  }

  function makeCard(item) {
    const file = resolveFilename(item);
    if (!file) return null;

    const thumbUrl = THUMB_BASE + encodeURIComponent(file);
    const fullUrl  = FULL_BASE  + encodeURIComponent(file);

    const title = resolveTitle(item, file);

    const a = document.createElement("a");
    a.className = "gallery-item";
    a.href = fullUrl;
    a.target = "_blank";
    a.rel = "noopener";

    const img = document.createElement("img");
    img.loading = "lazy";
    img.src = thumbUrl;
    img.alt = title;

    img.addEventListener("error", () => {
      img.src = fullUrl;
    });

    const cap = document.createElement("div");
    cap.className = "gallery-caption";
    cap.textContent = title;

    a.appendChild(img);
    a.appendChild(cap);

    return a;
  }

  function render(items, query) {
    if (!gridEl) return;

    const q = normaliseText(query);

    const filtered = !q
      ? items
      : items.filter((it) => getItemText(it).includes(q));

    gridEl.innerHTML = "";
    const frag = document.createDocumentFragment();

    for (const item of filtered) {
      const card = makeCard(item);
      if (card) frag.appendChild(card);
    }

    gridEl.appendChild(frag);
    setStatus(`${filtered.length} / ${items.length} photos`);
  }

  async function loadJson() {
    setStatus("Loading photos…");

    let resp;
    try {
      resp = await fetch(JSON_URL, { cache: "no-store" });
    } catch (e) {
      showError(`Could not fetch ${JSON_URL}. (${e})`);
      return null;
    }

    if (!resp.ok) {
      showError(`Fetch failed for ${JSON_URL}: HTTP ${resp.status} ${resp.statusText}`);
      return null;
    }

    let data;
    try {
      data = await resp.json();
    } catch (e) {
      showError(`JSON parse error in ${JSON_URL}: ${e}`);
      return null;
    }

    const items =
      Array.isArray(data) ? data :
      Array.isArray(data.photos) ? data.photos :
      Array.isArray(data.items) ? data.items :
      null;

    if (!items) {
      showError(`Unexpected JSON structure in ${JSON_URL}. Expected an array, or { "photos": [...] }.`);
      return null;
    }

    return items;
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

    const items = await loadJson();
    if (!items) return;

    render(items, "");

    if (searchEl) {
      const onInput = debounce(() => render(items, searchEl.value), 120);
      searchEl.addEventListener("input", onInput);
    }
  }

  document.addEventListener("DOMContentLoaded", init);
})();
