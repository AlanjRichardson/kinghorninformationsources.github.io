// Search logic + selection

// Stores selected entries (Full Name + Photo file) across searches on this page load
// key: "fullName||photoFile" -> { fullName, photoFile }
const selectedEntries = new Map();

const DRIVE_FOLDER_URL =
  "https://drive.google.com/drive/folders/0B_ryY5OKr0WyRlZxUmVBUU0wbjg?resourcekey=0--wTJ-afNjfmQDnNBqjaA9g&usp=sharing";

function openDriveFolder() {
  window.open(DRIVE_FOLDER_URL, "_blank", "noopener,noreferrer");
}

// Show/hide the post-search tools area (Copy/Clear/Open Album etc.)
function setResultsToolsVisible(show) {
  const tools = document.getElementById("resultsTools");
  if (tools) tools.style.display = show ? "block" : "none";
}

function updateResultsInfo(matchCount = null, message = null) {
  const resultsInfo = document.getElementById("resultsInfo");
  if (!resultsInfo) return;

  if (message) {
    resultsInfo.textContent = message;
    return;
  }

  const selCount = selectedEntries.size;

  if (matchCount !== null) {
    resultsInfo.textContent =
      `${matchCount} result${matchCount === 1 ? "" : "s"} found. ` +
      `Selected entries: ${selCount}`;
  } else {
    resultsInfo.textContent = `Selected entries: ${selCount}`;
  }
}

function getCopyMode() {
  const modeEl = document.querySelector('input[name="copyMode"]:checked');
  return modeEl ? modeEl.value : "photo"; // default
}

// If in photo-only mode, keep only the newest selection
function enforceSingleSelectionIfPhotoMode(newKeyToKeep) {
  if (getCopyMode() !== "photo") return;

  // Keep only one selected entry in the Map
  for (const key of Array.from(selectedEntries.keys())) {
    if (key !== newKeyToKeep) selectedEntries.delete(key);
  }

  // Update UI checkboxes to match the Map
  document
    .querySelectorAll('#resultsArea input[type="checkbox"]')
    .forEach((cb) => {
      const fullName = cb.getAttribute("data-fullname") || "";
      const photo = cb.getAttribute("data-photo") || "";
      const key = `${fullName}||${photo}`;
      cb.checked = key === newKeyToKeep;
    });
}

function performSearch() {
  const input = document.getElementById("surnameInput");
  const resultsArea = document.getElementById("resultsArea");

  if (!input || !resultsArea) {
    updateResultsInfo(null, "Page elements not found. Please refresh.");
    return;
  }

  const prefix = input.value.trim().toLowerCase();
  resultsArea.innerHTML = "";

  if (prefix.length < 3) {
    setResultsToolsVisible(false);
    updateResultsInfo(null, "Please enter at least 3 letters of a surname.");
    return;
  }

  // Ensure people-data is loaded
  if (typeof people === "undefined" || !Array.isArray(people)) {
    setResultsToolsVisible(false);
    updateResultsInfo(
      null,
      "People data not loaded yet. Please refresh the page."
    );
    return;
  }

  // Filter people by surname prefix (case-insensitive)
  const matches = people.filter(
    (p) => p.surname && p.surname.toLowerCase().startsWith(prefix)
  );

  if (matches.length === 0) {
    setResultsToolsVisible(false);
    updateResultsInfo(null, "No matches found.");
    resultsArea.innerHTML =
      "<p><em>No people found with that surname prefix.</em></p>";
    return;
  }

  // Build results table (with checkboxes)
  // NOTE: surname column removed (now: Select | Full name | Photo file)
  let html = "";
  html += "<table>";
  html +=
    "<thead><tr>" +
    "<th>Tick</th>" +
    "<th>Full name</th>" +
    "<th>Photo file</th>" +
    "</tr></thead><tbody>";

  matches.forEach((p) => {
    const fullNameRaw = p.fullName || "";
    const photoRaw = p.photoFile || "";

    const fullName = escapeHtml(fullNameRaw);
    const photo = escapeHtml(photoRaw);

    const key = `${fullNameRaw}||${photoRaw}`;
    const checked = selectedEntries.has(key) ? "checked" : "";

    html +=
      "<tr>" +
      `<td><input type="checkbox"
            data-fullname="${escapeAttr(fullNameRaw)}"
            data-photo="${escapeAttr(photoRaw)}"
            ${checked}
            onchange="toggleSelected(this)"></td>` +
      `<td>${fullName}</td>` +
      `<td>${photo}</td>` +
      "</tr>";
  });

  html += "</tbody></table>";
  resultsArea.innerHTML = html;

  setResultsToolsVisible(true);
  updateResultsInfo(matches.length);

  // If we're currently in photo-only mode and multiple are already selected,
  // force it back to one to keep rules consistent.
  if (getCopyMode() === "photo" && selectedEntries.size > 1) {
    const firstKey = selectedEntries.keys().next().value;
    enforceSingleSelectionIfPhotoMode(firstKey);
    updateResultsInfo(null, "Photo-only mode: selection limited to one entry.");
  }
}

function toggleSelected(checkbox) {
  const fullName = checkbox.getAttribute("data-fullname") || "";
  const photo = checkbox.getAttribute("data-photo") || "";
  if (!photo) return; // photo is the essential bit

  const key = `${fullName}||${photo}`;

  if (checkbox.checked) {
    selectedEntries.set(key, { fullName, photoFile: photo });
    enforceSingleSelectionIfPhotoMode(key); // photo-mode: keep only this one
  } else {
    selectedEntries.delete(key);
  }

  updateResultsInfo(null);
}

async function copySelected() {
  if (selectedEntries.size === 0) {
    updateResultsInfo(null, "No selected entries to copy.");
    return;
  }

  const mode = getCopyMode();
  let text = "";
  let message = "";

  if (mode === "photo") {
    // photo-only mode: we enforce single selection, but handle safely anyway
    const photos = Array.from(
      new Set(
        Array.from(selectedEntries.values())
          .map((item) => item.photoFile)
          .filter(Boolean)
      )
    ).sort((a, b) => a.localeCompare(b));

    text = photos[0] || "";
    message = "Copied photo filename to clipboard (album search).";
  } else {
    const lines = Array.from(selectedEntries.values())
      .sort((a, b) => {
        const s = (a.fullName || "").localeCompare(b.fullName || "");
        return s !== 0 ? s : (a.photoFile || "").localeCompare(b.photoFile || "");
      })
      .map((item) => `${item.fullName} — ${item.photoFile}`);

    text = lines.join("\n");
    message =
      `Copied ${selectedEntries.size} selected entr` +
      `${selectedEntries.size === 1 ? "y" : "ies"} (notes format).`;
  }

  try {
    await navigator.clipboard.writeText(text);
    updateResultsInfo(null, message);
  } catch (e) {
    window.prompt("Copy to clipboard:", text);
  }
}

function clearSelected() {
  selectedEntries.clear();
  updateResultsInfo(null, "Selected entries cleared.");

  const input = document.getElementById("surnameInput");
  const prefix = input ? input.value.trim() : "";
  if (prefix.length >= 3) performSearch();
  else document.getElementById("resultsArea").innerHTML = "";
}

function clearSearch() {
  const input = document.getElementById("surnameInput");
  if (input) input.value = "";

  document.getElementById("resultsArea").innerHTML = "";
  setResultsToolsVisible(false);
  updateResultsInfo(null);

  if (input) input.focus();
}

function escapeHtml(text) {
  if (!text) return "";
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function escapeAttr(text) {
  if (!text) return "";
  return text
    .replace(/&/g, "&amp;")
    .replace(/"/g, "&quot;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("surnameInput");

  if (input) {
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        performSearch();
      }
    });
  }

  // When user switches copy mode to photo-only, enforce only one selection
  document.querySelectorAll('input[name="copyMode"]').forEach((radio) => {
    radio.addEventListener("change", () => {
      if (getCopyMode() === "photo" && selectedEntries.size > 1) {
        const firstKey = selectedEntries.keys().next().value;
        enforceSingleSelectionIfPhotoMode(firstKey);
        updateResultsInfo(null, "Photo-only mode: selection limited to one entry.");
      }
    });
  });

  setResultsToolsVisible(false);
  updateResultsInfo(null);
});

