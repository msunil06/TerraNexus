// TerraNexus Global Live Search Engine
document.addEventListener("DOMContentLoaded", () => {
  const searchInputs = document.querySelectorAll(".tn-search-input");

  searchInputs.forEach((input) => {
    const wrapper = input.closest(".tn-search-wrapper");
    const dropdown = wrapper ? wrapper.querySelector(".tn-search-dropdown") : null;
    if (!dropdown) return;

    let debounceTimer = null;
    let selectedIndex = -1;

    input.addEventListener("input", () => {
      clearTimeout(debounceTimer);
      const query = input.value.trim();

      if (query.length === 0) {
        dropdown.classList.remove("active");
        dropdown.innerHTML = "";
        selectedIndex = -1;
        return;
      }

      debounceTimer = setTimeout(() => {
        fetchSearchResults(query, dropdown);
      }, 250);
    });

    // Keyboard navigation
    input.addEventListener("keydown", (e) => {
      const items = dropdown.querySelectorAll(".tn-search-item");
      if (!dropdown.classList.contains("active") || items.length === 0) return;

      if (e.key === "ArrowDown") {
        e.preventDefault();
        selectedIndex = (selectedIndex + 1) % items.length;
        updateSelection(items, selectedIndex);
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        selectedIndex = (selectedIndex - 1 + items.length) % items.length;
        updateSelection(items, selectedIndex);
      } else if (e.key === "Enter") {
        if (selectedIndex >= 0 && items[selectedIndex]) {
          e.preventDefault();
          window.location.href = items[selectedIndex].getAttribute("href");
        }
      } else if (e.key === "Escape") {
        dropdown.classList.remove("active");
      }
    });

    // Close on click outside
    document.addEventListener("click", (e) => {
      if (!wrapper.contains(e.target)) {
        dropdown.classList.remove("active");
      }
    });

    // Show on focus if input has value
    input.addEventListener("focus", () => {
      if (input.value.trim().length > 0 && dropdown.children.length > 0) {
        dropdown.classList.add("active");
      }
    });
  });
});

async function fetchSearchResults(query, dropdown) {
  try {
    dropdown.innerHTML = `<div style="padding: 12px; text-align: center; color: var(--text-muted); font-size: 0.85rem;">Searching global registry...</div>`;
    dropdown.classList.add("active");

    const res = await fetch(`/api/search?q=${encodeURIComponent(query)}&limit=8`);
    if (!res.ok) throw new Error("Search network error");

    const data = await res.json();
    const results = data.data || [];

    if (results.length === 0) {
      dropdown.innerHTML = `
        <div style="padding: 16px; text-align: center; color: var(--text-muted); font-size: 0.88rem;">
          No geographic records found for "<strong>${escapeHtml(query)}</strong>"
        </div>
      `;
      return;
    }

    dropdown.innerHTML = "";
    results.forEach((item) => {
      const el = document.createElement("a");
      el.className = "tn-search-item";
      el.href = item.url;
      el.innerHTML = `
        <div class="tn-search-item-info">
          <span class="tn-search-item-flag">${item.flag || "📍"}</span>
          <div>
            <div class="tn-search-item-title">${escapeHtml(item.title)}</div>
            <div class="tn-search-item-subtitle">${escapeHtml(item.subtitle)}</div>
          </div>
        </div>
        <span class="tn-badge">${escapeHtml(item.badge)}</span>
      `;
      dropdown.appendChild(el);
    });
  } catch (err) {
    console.error("Search fetch error:", err);
    dropdown.innerHTML = `<div style="padding: 12px; text-align: center; color: var(--danger); font-size: 0.85rem;">Error retrieving search results</div>`;
  }
}

function updateSelection(items, index) {
  items.forEach((item, i) => {
    item.classList.toggle("selected", i === index);
    if (i === index) {
      item.scrollIntoView({ block: "nearest" });
    }
  });
}

function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/[&<>"']/g, (m) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[m]));
}
