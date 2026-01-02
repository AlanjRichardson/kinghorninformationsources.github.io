/* js/photos-with-names-gallery.js
   Works with:
     /photos-with-names/photos.json

   Where each JSON item looks like:
     { "full":"full/xxx.jpg", "thumb":"thumbnails/xxx.jpg", "title":"..." }

   Expects in gallery.html:
     - input#gallery-filter
     - div#gallery-grid
     - span#gallery-count
*/

(() => {
  "use strict";

  // Base folder that contains photos.json AND the full/ + thumbnails/ folders
  const BASE = "photos-with-names/";
  const JSON_URL = BASE + "photos.json";

  const $ = (sel) => document.querySelector(sel);

  const searchEl = $("#gallery-filter");
  const gridEl   = $("#gallery-grid");
  const countEl  = $("#gallery-count");

  function setCount(msg) {
    if (countEl) countEl.textContent = msg || "";
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
          Check that <code>${JSON_URL}</code> exists and that your JSON items contain <code>thumb</code> and <code>full</code>.
        </div>
      </div>`;
    setCount("");
  }

  function normaliseText(s) {
    return String(s || "").toLowerCase().replace(/\s+/g, " ").trim();
  }

  function getSearchText(item) {
    // Search by title + file paths (handy if you type part of filename)
    return normaliseText([
      item.title || "",
      item.full  || "",
      item.thumb || ""
    ].join(" "));
  }

  function makeCard(item) {
    // Your JSON uses "thumb" and "full"
    if (!item || !item.thumb || !item.full) return null;

    const thumbUrl = BASE + item.thumb;
    const fullUrl  = BASE + item.full;
    const title    = item.title ? String(item.title) : "Photo";

    // Use <figure> so your existing CSS for .gallery-grid figure/figcaption applies
    const fig = document.createElement("figure");

    const a = document.createElement("a");
    a.href = fullUrl;
    a.target = "_blank";
    a.rel = "noopener";

    const img = document.createElement("img");
    img.loading = "lazy";
    img.src = thumbUrl;
    img.alt = title;

    // Thumbnail missing? fall back to full image
    img.addEventListener("error", () => {
      img.src = fullUrl;
    });

    const cap = document.createElement("figcaption");
    cap.textContent = title;

    a.appendChild(img);
    fig.appendChild(a);
    fig.appendChild(cap);

    return fig;
  }

  function render(items, query) {
    if (!gridEl) return;

    const q = normaliseText(query);
    const filtered = !q ? items : items.filter((it) => getSearchText(it).includes(q));

    gridEl.innerHTML = "";
    const frag = document.createDocumentFragment();

    for (const item of filtered) {
      const card = makeCard(item);
      if (card) frag.appendChild(card);
    }

    gridEl.appendChild(frag);
    setCount(`${filtered.length} / ${items.length} photos`);
  }

  async function loadItems() {
    setCount("Loading photos…");

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

    if (!Array.isArray(data)) {
      showError(`Unexpected JSON structure in ${JSON_URL}. Expected a top-level array: [ {...}, {...} ]`);
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
    if (!gridEl) return;

    const items = await loadItems();
    if (!items) return;

    render(items, "");

    if (searchEl) {
      const onInput = debounce(() => render(items, searchEl.value), 120);
      searchEl.addEventListener("input", onInput);
    }
  }

  document.addEventListener("DOMContentLoaded", init);
})();
