/* js/photos-with-names-gallery.js
   Works with:
     /photos-with-names/photos.json
     /photos-with-names/thumbnails/<file>
     /photos-with-names/full/<file>

   Expects in gallery.html:
     - input#gallery-filter
     - div#gallery-grid
     - span#gallery-count   (used for status)
*/

(() => {
  "use strict";

  // ---- CONFIG ----
  const JSON_URL   = "photos-with-names/photos.json";
  const THUMB_BASE = "photos-with-names/thumbnails/";
  const FULL_BASE  = "photos-with-names/full/";

  // Try these fields for captions / searchable text
  const TEXT_FIELDS = ["title", "caption", "desc", "description", "text", "label", "name", "people", "place", "year"];

  // ---- DOM ----
  const $ = (sel) => document.querySelector(sel);

  const searchEl = $("#gallery-filter");
  const gridEl   = $("#gallery-grid");
  const statusEl = $("#gallery-count"); // reuse this as status line

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
    return String(s || "").toLowerCase().replace(/\s+/g, " ").trim();
  }

  function basename(p) {
    const s = String(p || "");
    const q = s.split("?")[0].split("#")[0];
    const parts = q.split("/");
    return parts[parts.length - 1] || "";
  }

  function getItemText(item) {
    // Supports strings or objects
    const bits = [];

    if (typeof item === "string") {
      bits.push(item);
      return normaliseText(bits.join(" "));
    }

    if (!item || typeof item !== "object") return "";

    // possible filename-ish fields
    for (const k of ["filename", "file", "name", "image", "src", "url", "path", "full", "thumb", "thumbnail"]) {
      if (item[k]) bits.push(String(item[k]));
    }

    for (const f of TEXT_FIELDS) {
      if (item[f]) bits.push(String(item[f]));
    }

    if (item.meta && typeof item.meta === "object") {
      for (const f of TEXT_FIELDS) {
        if (item.meta[f]) bits.push(String(item.meta[f]));
      }
    }

    return normaliseText(bits.join(" "));
  }

  function resolveUrls(item) {
    // Returns { thumbUrl, fullUrl, title }
    // Handles:
    //   - item as "IMG_001.jpg"
    //   - { file:"IMG_001.jpg", caption:"..." }
    //   - { full:"photos-with-names/full/IMG_001.jpg", thumb:"photos-with-names/thumbnails/IMG_001.jpg" }
    //   - { src/url/path: "...jpg" }

    // string item (filename)
    if (typeof item === "string") {
      const file = item;
      return {
        thumbUrl: THUMB_BASE + encodeURIComponent(file),
        fullUrl:  FULL_BASE  + encodeURIComponent(file),
        title: file
      };
    }

    if (!item || typeof item !== "object") return null;

    // prefer explicit thumb/full if present
    const rawThumb = item.thumb || item.thumbnail || (item.urls && item.urls.thumb);
    const rawFull  = item.full  || item.image     || item.src || item.url || item.path || (item.urls && item.urls.full);

    // If they gave full/thumb as paths/urls, use them directly.
    // If they gave filenames, build from bases.
    const thumbFile = rawThumb ? basename(rawThumb) : basename(item.filename || item.file || item.name || "");
    const fullFile  = rawFull  ? basename(rawFull)  : basename(item.filename || item.file || item.name || "");

    const thumbUrl = rawThumb
      ? (String(rawThumb).includes("/") ? String(rawThumb) : (THUMB_BASE + encodeURIComponent(String(rawThumb))))
      : (thumbFile ? THUMB_BASE + encodeURIComponent(thumbFile) : "");

    const fullUrl = rawFull
      ? (String(rawFull).includes("/") ? String(rawFull) : (FULL_BASE + encodeURIComponent(String(rawFull))))
      : (fullFile ? FULL_BASE + encodeURIComponent(fullFile) : "");

    // title
    let title = "";
    for (const f of ["title", "caption", "description", "desc", "text", "label"]) {
      if (item[f]) { title = String(item[f]); break; }
    }
    if (!title && item.meta && typeof item.meta === "object") {
      for (const f of ["title", "caption", "description", "desc", "text", "label"]) {
        if (item.meta[f]) { title = String(item.meta[f]); break; }
      }
    }
    if (!title) title = fullFile || thumbFile || "Photo";

    if (!fullUrl) return null; // must have a full image target to click

    return { thumbUrl, fullUrl, title };
  }

  function makeCard(item) {
    const resolved = resolveUrls(item);
    if (!resolved) return null;

    const { thumbUrl, fullUrl, title } = resolved;

    const a = document.createElement("a");
    a.className = "gallery-item";
    a.href = fullUrl;
    a.target = "_blank";
    a.rel = "noopener";

    const img = document.createElement("img");
    img.loading = "lazy";
    img.alt = title;

    // If thumb is missing, use full as the thumbnail
    img.src = thumbUrl || fullUrl;
    img.addEventListener("error", () => { img.src = fullUrl; });

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
    const filtered = !q ? items : items.filter((it) => getItemText(it).includes(q));

    gridEl.innerHTML = "";
    const frag = document.createDocumentFragment();

    let rendered = 0;
    for (const item of filtered) {
      const card = makeCard(item);
      if (card) {
        frag.appendChild(card);
        rendered++;
      }
    }

    gridEl.appendChild(frag);
    setStatus(`${rendered} / ${items.length} photos`);
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

    // Accept either an array, or { photos:[...] }, or { items:[...] }
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
