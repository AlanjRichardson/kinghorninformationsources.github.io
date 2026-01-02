/* js/photos-with-names-gallery.js
   Uses people index:
     /photos-with-names/people-index.json  (array of {surname, fullName, photoFile, ...})
   Images live in:
     /photos-with-names/thumbnails/<file>
     /photos-with-names/full/<file>

   Expects in gallery.html:
     - input#gallery-filter
     - div#gallery-grid
     - span#gallery-count
*/

(() => {
  "use strict";

  // ---- CONFIG ----
  const INDEX_URL  = "photos-with-names/people-index.json";
  const THUMB_BASE = "photos-with-names/thumbnails/";
  const FULL_BASE  = "photos-with-names/full/";

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
          Check that <code>${INDEX_URL}</code> exists and paths match your repo structure.
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

  // Year extraction rule (your requested behaviour):
  // - find a 4-digit year in the filename (e.g. School1948a.jpg -> 1948)
  // - allow suffix letters (a,b,c) and various cases
  function extractYearFromFilename(filename) {
    const m = String(filename || "").match(/(18\d{2}|19\d{2}|20\d{2})/);
    return m ? m[1] : "";
  }

  function isYearQuery(q) {
    return /^(18\d{2}|19\d{2}|20\d{2})$/.test(q);
  }

  function debounce(fn, ms = 120) {
    let t = null;
    return (...args) => {
      clearTimeout(t);
      t = setTimeout(() => fn(...args), ms);
    };
  }

  function resolveFilename(item) {
    // people-index.json likely uses photoFile
    return item.photoFile || item.filename || item.file || item.name || item.image || "";
  }

  // Build grouped photo records from per-person rows:
  // { file, year, allNames:Set, searchText }
  function groupByPhoto(rows) {
    const map = new Map();

    for (const r of rows) {
      const file = resolveFilename(r);
      if (!file) continue;

      let rec = map.get(file);
      if (!rec) {
        rec = {
          file,
          year: extractYearFromFilename(file),
          allNames: new Set(),
          // We'll build searchText later
          searchText: ""
        };
        map.set(file, rec);
      }

      if (r.fullName) rec.allNames.add(String(r.fullName));
      // surname can help searching too
      if (r.surname) rec.allNames.add(String(r.surname));
    }

    // Create searchable strings per photo
    for (const rec of map.values()) {
      const names = Array.from(rec.allNames).join(" ");
      rec.searchText = normaliseText([rec.file, rec.year, names].join(" "));
    }

    return Array.from(map.values());
  }

  function makeCard(photoRec, captionText) {
    const file = photoRec.file;

    const thumbUrl = THUMB_BASE + encodeURIComponent(file);
    const fullUrl  = FULL_BASE  + encodeURIComponent(file);

    const a = document.createElement("a");
    a.className = "gallery-item";
    a.href = fullUrl;
    a.target = "_blank";
    a.rel = "noopener";

    const img = document.createElement("img");
    img.loading = "lazy";
    img.src = thumbUrl;
    img.alt = captionText || file;

    // If thumbnail missing, fall back to full
    img.addEventListener("error", () => {
      img.src = fullUrl;
    });

    const cap = document.createElement("div");
    cap.className = "gallery-caption";
    cap.textContent = captionText || file;

    a.appendChild(img);
    a.appendChild(cap);
    return a;
  }

  function render(photoRecs, query) {
    if (!gridEl) return;

    const q = normaliseText(query);
    const yearMode = isYearQuery(q);

    // Filter photos
    const filtered = !q
      ? photoRecs
      : photoRecs.filter((p) => p.searchText.includes(q));

    // Build captions:
    // - year search: keep it simple (file without extension, or file)
    // - name search: show matching names only
    const frag = document.createDocumentFragment();
    gridEl.innerHTML = "";

    for (const p of filtered) {
      let caption = "";

      if (!q) {
        caption = p.file.replace(/\.[^.]+$/, ""); // default title: filename minus extension
      } else if (yearMode) {
        caption = p.file.replace(/\.[^.]+$/, ""); // year browsing: no names
      } else {
        // Name browsing: show only names that match the query words
        // (simple contains match, good enough and fast)
        const qWords = q.split(" ").filter(Boolean);
        const names = Array.from(p.allNames)
          .filter((nm) => {
            const n = normaliseText(nm);
            return qWords.every((w) => n.includes(w));
          });

        if (names.length === 0) {
          // fallback
          caption = p.file.replace(/\.[^.]+$/, "");
        } else if (names.length <= 3) {
          caption = names.join(", ");
        } else {
          caption = `${names.slice(0, 3).join(", ")} (+${names.length - 3} more)`;
        }
      }

      frag.appendChild(makeCard(p, caption));
    }

    gridEl.appendChild(frag);
    setStatus(`${filtered.length} / ${photoRecs.length} photos`);
  }

  async function loadIndex() {
    setStatus("Loading photos…");

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

    let rows;
    try {
      rows = await resp.json();
    } catch (e) {
      showError(`JSON parse error in ${INDEX_URL}: ${e}`);
      return null;
    }

    if (!Array.isArray(rows)) {
      showError(`Unexpected JSON structure in ${INDEX_URL}. Expected an array.`);
      return null;
    }

    return rows;
  }

  async function init() {
    if (!gridEl) {
      console.warn("No #gallery-grid element found — nothing to render.");
      return;
    }

    const rows = await loadIndex();
    if (!rows) return;

    const photoRecs = groupByPhoto(rows);

    // Initial render
    render(photoRecs, "");

    // Search
    if (searchEl) {
      const onInput = debounce(() => render(photoRecs, searchEl.value), 120);
      searchEl.addEventListener("input", onInput);
    }
  }

  document.addEventListener("DOMContentLoaded", init);
})();
