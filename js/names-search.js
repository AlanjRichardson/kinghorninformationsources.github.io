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

function performSearch() {
  const input = document.getElementById("surnameInput");
  const prefix = input.value.trim().toLowerCase();
  const resultsArea = document.getElementById("resultsArea");

  resultsArea.innerHTML = "";

  if (prefix.length < 3) {
    setResultsToolsVisible(false);
    updateResultsInfo(null, "Please enter at least 3 letters of a surname.");
    return;
  }

  // Safety: ensure the people-data.js has loaded
  if (typeof people === "undefined" || !Array.isArray(people)) {
  setResultsToolsVisible(false);
  updateResultsInfo(
    null,
    "People data not loaded yet. Please refresh the page."
  );
  return;
}

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
  let html = "";
  html += "<table>";
  html +=
    "<thead><tr>" +
    "<th>Select</th>" +
    "<th>Surname</th>" +
    "<th>Full name</th>" +
    "<th>Photo file</th>" +
    "</tr></thead><tbody>";

  matches.forEach((p) => {
    const surnameRaw = p.surname || "";
    const fullNameRaw = p.fullName || "";
    const photoRaw = p.photoFile || "";

    const surname = escapeHtml(surnameRaw);
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
      `<td>${surname}</td>` +
      `<td>${fullName}</td>` +
      `<td>${photo}</td>` +
      "</tr>";
  });

  html += "</tbody></table>";
  resultsArea.innerHTML = html;

  setResultsToolsVisible(true);
  updateResultsInfo(matches.length);
}

function toggleSelected(checkbox) {
  const fullName = checkbox.getAttribute("data-fullname") || "";
  const photo = checkbox.getAttribute("data-photo") || "";

  // If you want to allow selecting even when fullName is blank, change to: if (!photo) return;
  if (!fullName || !photo) return;

  const key = `${fullName}||${photo}`;

  if (checkbox.checked) {
    selectedEntries.set(key, { fullName, photoFile: photo });
  } else {
    selectedEntries.delete(key);
  }

  updateResultsInfo(null);
}

// Optional (only used if you keep the "Show selected" button somewhere)
function showSelected() {
  const resultsArea = document.getElementById("resultsArea");

  if (selectedEntries.size === 0) {
    updateResultsInfo(null, "No selected entries yet.");
    resultsArea.innerHTML = "";
    return;
  }

  const items = Array.from(selectedEntries.values()).sort((a, b) => {
    const s = a.fullName.localeCompare(b.fullName);
    return s !== 0 ? s : a.photoFile.localeCompare(b.photoFile);
  });

  let html = "<h3>Selected entries (Full name — Photo file)</h3>";
  html += "<ul>";
  items.forEach((item) => {
    html += `<li>${escapeHtml(item.fullName)} — ${escapeHtml(
      item.photoFile
    )}</li>`;
  });
  html += "</ul>";

  resultsArea.innerHTML = html;
  updateResultsInfo(null);
}

function getCopyMode() {
  const modeEl = document.querySelector('input[name="copyMode"]:checked');
  return modeEl ? modeEl.value : "photo"; // default
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
    // Album search works best one filename at a time.
    const photos = Array.from(
      new Set(
        Array.from(selectedEntries.values())
          .map((item) => item.photoFile)
          .filter(Boolean)
      )
    ).sort((a, b) => a.localeCompare(b));

    if (photos.length === 0) {
      updateResultsInfo(null, "No photo filenames found to copy.");
      return;
    }

    if (photos.length > 1) {
      text = photos[0]; // copy only the first filename
      message =
        "Multiple photos selected. Copied the first filename only " +
        "(album search works one filename at a time).";
    } else {
      text = photos[0];
      message = "Copied photo filename to clipboard (album search).";
    }
  } else {
    // Full name + photo (for notes)
    const lines = Array.from(selectedEntries.values())
      .sort((a, b) => {
        const s = a.fullName.localeCompare(b.fullName);
        return s !== 0 ? s : a.photoFile.localeCompare(b.photoFile);
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

  // If a search is visible, refresh it so checkboxes clear
  const prefix = document.getElementById("surnameInput").value.trim();
  if (prefix.length >= 3) performSearch();
  else document.getElementById("resultsArea").innerHTML = "";
}

function clearSearch() {
  document.getElementById("surnameInput").value = "";
  document.getElementById("resultsArea").innerHTML = "";
  setResultsToolsVisible(false);
  updateResultsInfo(null);
  document.getElementById("surnameInput").focus();
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

// Allow Enter key to trigger the search
document.getElementById("surnameInput").addEventListener("keydown", function (e) {
  if (e.key === "Enter") {
    e.preventDefault();
    performSearch();
  }
});

// On first load, hide tools until a successful search
setResultsToolsVisible(false);
updateResultsInfo(null);
