/* js/photos-with-names-gallery.js
   Works with photos-with-names/photos.json entries like:
     { "full":"full/X.jpg", "thumb":"thumbnails/X.jpg", "title":"..." }
   Page expects:
     #gallery-filter, #gallery-grid, #gallery-count
*/

(() => {
  "use strict";

  // ---- CONFIG ----
  const JSON_URL = "photos-with-names/photos.json";
  const PATH_PREFIX = "photos-with-names/"; // because JSON paths are relative to photos-with-names/

  // ---- DOM ----
  const $ = (sel) => document.querySelector(sel);

  const searchEl = $("#gallery-filter");
  const gridEl   = $("#gallery-grid");
  const statusEl = $("#gallery-count");

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
          Check that <code>${JSON_URL}</code> exists and that the JSON paths match your folders.
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
    // searchable text: title + paths (helps searching by filename)
    const bits = [];
    if (item.title) bits.push(item.title);
    if (item.full)  bits.push(item.full);
    if (item.thumb) bits.push(item.thumb);
    return normaliseText(bits.join(" "));
  }

  function joinUrl(prefix, p) {
    // Ensure we don’t double-prefix if p already starts with "photos-with-names/"
    const path = String(p || "").replace(/^\/+/, "");
    if (!path) return "";
    if (path.startsWith(PATH_PREFIX)) return path;
    return prefix + path;
  }

  function makeFigure(item) {
    const fullRel  = item.full  || "";
    const thumbRel = item.thumb || "";
    const title    = item.title || fullRel || "Photo";

    const fullUrl  = joinUrl(PATH_PREFIX, fullRel);
    const thumbUrl = joinUrl(PATH_PREFIX, thumbRel);

    if (!fullUrl || !thumbUrl) return null;

    const fig = document.createElement("figure");

    const a = document.createElement("a");
    a.href = fullUrl;
    a.target = "_blank";
    a.rel = "noopener";
    a.setAttribute("aria-label", title);

    const img = document.createElement("img");
    img.loading = "lazy";
    img.src = thumbUrl;
    img.alt = title;

    // If thumb missing, fall back ONCE to full image (avoid infinite error loops)
    img.addEventListener("error", () => {
      if (img.dataset.fellback) return;
      img.dataset.fellback = "1";
      img.src = fullUrl;
    });

    a.appendChild(img);

    const cap = document.createElement("figcaption");
    cap.textContent = title;

    fig.appendChild(a);
    fig.appendChild(cap);

    return fig;
  }

  function render(items, query) {
    if (!gridEl) return;

    const q = normaliseText(query);
    const filtered = !q ? items : items.filter((it) => getItemText(it).includes(q));

    gridEl.innerHTML = "";
    const frag = document.createDocumentFragment();

    for (const item of filtered) {
      const fig = makeFigure(item);
      if (fig) frag.appendChild(fig);
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

    const items = Array.isArray(data) ? data
      : Array.isArray(data.photos) ? data.photos
      : Array.isArray(data.items) ? data.items
      : null;

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
    if (!gridEl) return;

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
