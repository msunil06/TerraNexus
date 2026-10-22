// TerraNexus Main Client Logic
document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  initSidebarDrawer();
  initNavDropdown();
  initCityMapModal();
  initMobileNav();
  initPWA();
  initFavoriteButtons();
  initTabs();
  initLivePopulationTickers();
});

// 1. Theme Management (Dark Cosmos & Light Atlas)
function initTheme() {
  const themeToggle = document.getElementById("themeToggle");
  const storedTheme = localStorage.getItem("tn_theme") || "dark";
  applyTheme(storedTheme);

  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      const current = document.documentElement.getAttribute("data-theme") || "dark";
      const next = current === "dark" ? "light" : "dark";
      applyTheme(next);
    });
  }
}

function applyTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  try {
    localStorage.setItem("tn_theme", theme);
  } catch (e) {}

  const themeIcon = document.getElementById("themeIcon");
  const themeText = document.getElementById("themeText");
  if (themeIcon) {
    themeIcon.textContent = theme === "dark" ? "🌙" : "☀️";
  }
  if (themeText) {
    themeText.textContent = theme === "dark" ? "Dark Cosmos" : "Light Atlas";
  }

  // Update profile select if present
  const profileSelect = document.getElementById("profileThemeSelect");
  if (profileSelect && profileSelect.value !== theme) {
    profileSelect.value = theme;
  }

  // Update settings badge if present
  const currentBadge = document.getElementById("currentThemeBadge");
  if (currentBadge) {
    currentBadge.textContent = theme === "dark" ? "🌙 Dark Cosmos" : "☀️ Light Atlas";
  }

  // Persist to user account if authenticated
  try {
    fetch("/api/theme", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ theme: theme })
    }).catch(() => {});
  } catch (e) {}

  // Dispatch global event for interactive components (e.g. Leaflet map)
  window.dispatchEvent(new CustomEvent("themeChanged", { detail: { theme } }));
}
window.applyTheme = applyTheme;

// 1b. Collapsible Sliding Sidebar Drawer
function initSidebarDrawer() {
  const toggleBtn = document.getElementById("sidebarToggleBtn");
  const closeBtn = document.getElementById("closeSidebarBtn");
  const backdrop = document.getElementById("tnSidebarBackdrop");
  const sidebar = document.getElementById("tnSidebar");

  function openSidebar() {
    if (sidebar) sidebar.classList.add("active");
    if (backdrop) backdrop.classList.add("active");
    document.body.style.overflow = "hidden";
  }

  function closeSidebar() {
    if (sidebar) sidebar.classList.remove("active");
    if (backdrop) backdrop.classList.remove("active");
    document.body.style.overflow = "";
  }

  if (toggleBtn) toggleBtn.addEventListener("click", openSidebar);
  if (closeBtn) closeBtn.addEventListener("click", closeSidebar);
  if (backdrop) backdrop.addEventListener("click", closeSidebar);

  // Close on ESC key
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeSidebar();
      closeCityMapModal();
    }
  });
}

// 1b-2. Navigation Dropdown Toggle (More Menu)
function initNavDropdown() {
  const dropdown = document.getElementById("navMoreDropdown");
  const btn = document.getElementById("navMoreDropdownBtn");
  if (!dropdown || !btn) return;

  btn.addEventListener("click", (e) => {
    e.stopPropagation();
    const isOpen = dropdown.classList.toggle("active");
    btn.setAttribute("aria-expanded", isOpen ? "true" : "false");
  });

  // Close when clicking outside
  document.addEventListener("click", (e) => {
    if (!dropdown.contains(e.target)) {
      dropdown.classList.remove("active");
      btn.setAttribute("aria-expanded", "false");
    }
  });

  // Close on ESC key
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      dropdown.classList.remove("active");
      btn.setAttribute("aria-expanded", "false");
    }
  });
}

// 1c. Universal City, Capital, and Island Map Modal
let cityModalMap = null;
let cityModalMarker = null;

function initCityMapModal() {
  // Delegate clicks on any button with data-view-map
  document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-view-map]");
    if (!btn) return;
    e.preventDefault();

    const name = btn.dataset.mapName || "Location";
    const lat = parseFloat(btn.dataset.mapLat);
    const lon = parseFloat(btn.dataset.mapLon);
    const context = btn.dataset.mapContext || "";
    const zoom = btn.dataset.mapZoom ? parseInt(btn.dataset.mapZoom) : 10;

    if (!isNaN(lat) && !isNaN(lon)) {
      openCityMapModal(name, lat, lon, context, zoom);
    }
  });

  const closeBtn = document.getElementById("closeCityModalBtn");
  const backdrop = document.getElementById("cityMapModalBackdrop");
  if (closeBtn) closeBtn.addEventListener("click", closeCityMapModal);
  if (backdrop) backdrop.addEventListener("click", (e) => {
    if (e.target === backdrop) closeCityMapModal();
  });
}

function openCityMapModal(name, lat, lon, context = "", zoom = 10) {
  const backdrop = document.getElementById("cityMapModalBackdrop");
  const titleEl = document.getElementById("cityModalTitle");
  const subEl = document.getElementById("cityModalSubtitle");
  const container = document.getElementById("cityModalMapFrame");
  const modalElem = document.getElementById("cityModalCard");
  const fullIcon = document.getElementById("fullScreenBtnIcon");
  const fullText = document.getElementById("fullScreenBtnText");

  if (!backdrop || !container) return;

  if (titleEl) titleEl.textContent = name;
  if (subEl) subEl.textContent = context ? `${context} • Coordinates: ${lat.toFixed(4)}° N, ${lon.toFixed(4)}° E` : `${lat.toFixed(4)}° N, ${lon.toFixed(4)}° E`;

  backdrop.classList.add("active");
  document.body.style.overflow = "hidden";

  // Setup full mode toggle
  const fullScreenBtn = document.getElementById("toggleModalFullScreenBtn");
  if (fullScreenBtn && modalElem) {
    fullScreenBtn.onclick = function(e) {
      e.stopPropagation();
      const isFull = modalElem.classList.toggle("full-mode");
      if (fullIcon) fullIcon.textContent = isFull ? "🗗" : "⛶";
      if (fullText) fullText.textContent = isFull ? "Normal Mode" : "Full Mode";
      setTimeout(() => {
        if (cityModalMap) cityModalMap.invalidateSize();
      }, 150);
    };
  }

  setTimeout(() => {
    if (!cityModalMap && typeof L !== "undefined") {
      cityModalMap = L.map(container, {
        center: [lat, lon],
        zoom: zoom,
        zoomControl: true
      });

      // 100% Free Public Tiles - Zero Watermarks & Zero API Key Required
      const satLayer = L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", {
        attribution: 'Tiles &copy; Esri &mdash; High-Res Satellite (Free Public)',
        maxZoom: 18
      }).addTo(cityModalMap);

      const darkLayer = L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}", {
        attribution: 'Tiles &copy; Esri Dark Canvas (Zero API Key)',
        maxZoom: 16
      });

      const streetLayer = L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}", {
        attribution: 'Tiles &copy; Esri World Street (Zero API Key)',
        maxZoom: 18
      });

      const osmLayer = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; OpenStreetMap contributors',
        maxZoom: 19
      });

      L.control.layers({
        "ESRI Satellite": satLayer,
        "ESRI Dark Canvas": darkLayer,
        "ESRI Street Map": streetLayer,
        "OpenStreetMap": osmLayer
      }, null, { position: "topright" }).addTo(cityModalMap);

      cityModalMarker = L.marker([lat, lon]).addTo(cityModalMap);
    } else if (cityModalMap) {
      cityModalMap.setView([lat, lon], zoom);
      if (cityModalMarker) {
        cityModalMarker.setLatLng([lat, lon]);
      } else {
        cityModalMarker = L.marker([lat, lon]).addTo(cityModalMap);
      }
    }

    if (cityModalMarker) {
      cityModalMarker.bindPopup(`<strong>${name}</strong><br>${context}`).openPopup();
    }

    if (cityModalMap) {
      cityModalMap.invalidateSize();
    }
  }, 200);
}

function closeCityMapModal() {
  const backdrop = document.getElementById("cityMapModalBackdrop");
  const modalElem = document.getElementById("cityModalCard");
  const fullIcon = document.getElementById("fullScreenBtnIcon");
  const fullText = document.getElementById("fullScreenBtnText");

  if (modalElem && modalElem.classList.contains("full-mode")) {
    modalElem.classList.remove("full-mode");
    if (fullIcon) fullIcon.textContent = "⛶";
    if (fullText) fullText.textContent = "Full Mode";
  }

  if (backdrop) {
    backdrop.classList.remove("active");
    document.body.style.overflow = "";
  }
}
window.openCityMapModal = openCityMapModal;
window.closeCityMapModal = closeCityMapModal;

// 2. Real-Time Live Population Ticker (Worldometer-style)
function initLivePopulationTickers() {
  const tickerEls = document.querySelectorAll("[data-live-population]");
  tickerEls.forEach((el) => {
    let currentPop = parseFloat(el.getAttribute("data-live-population"));
    const growthPerSec = parseFloat(el.getAttribute("data-growth-per-sec")) || 0.0;

    if (!isNaN(currentPop) && growthPerSec !== 0) {
      const intervalMs = 200; // update 5 times per second for ultra-smooth fluid count
      const incrementPerTick = growthPerSec * (intervalMs / 1000.0);

      setInterval(() => {
        currentPop += incrementPerTick;
        el.textContent = Math.round(currentPop).toLocaleString();
      }, intervalMs);
    }
  });
}

// 2. Mobile Navigation Toggle
function initMobileNav() {
  const toggleBtn = document.getElementById("mobileNavToggle");
  const navLinks = document.getElementById("navLinks");

  if (toggleBtn && navLinks) {
    toggleBtn.addEventListener("click", () => {
      navLinks.classList.toggle("active");
      toggleBtn.setAttribute("aria-expanded", navLinks.classList.contains("active"));
    });
  }
}

// 3. PWA Registration
function initPWA() {
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/static/sw.js")
      .then((reg) => console.log("TerraNexus PWA Service Worker Registered", reg.scope))
      .catch((err) => console.warn("PWA Service Worker registration skipped:", err));
  }
}

// 4. Dynamic Favorites Toggling
function initFavoriteButtons() {
  document.querySelectorAll(".tn-fav-btn").forEach((btn) => {
    btn.addEventListener("click", async (e) => {
      e.preventDefault();
      const itemType = btn.dataset.itemType;
      const itemId = btn.dataset.itemId;
      const itemTitle = btn.dataset.itemTitle || itemId;
      const isFav = btn.classList.contains("active");

      try {
        if (isFav) {
          // Remove favorite
          const res = await fetch(`/api/me/favorites/${itemType}/${itemId}`, { method: "DELETE" });
          if (res.ok) {
            btn.classList.remove("active");
            btn.innerHTML = "☆ Save";
            showToast("Removed from your saved favorites", "info");
          }
        } else {
          // Add favorite
          const res = await fetch("/api/me/favorites", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ item_type: itemType, item_id: itemId, item_title: itemTitle })
          });
          if (res.ok) {
            btn.classList.add("active");
            btn.innerHTML = "★ Saved";
            showToast("Saved to your favorites!", "success");
          } else if (res.status === 401) {
            showToast("Please sign in to save favorites.", "warning");
          }
        }
      } catch (err) {
        console.error("Error toggling favorite:", err);
      }
    });
  });
}

// 5. Tabs Switching
function initTabs() {
  document.querySelectorAll(".tn-tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const target = btn.dataset.target;
      const parent = btn.closest(".tn-tabs-container") || document;

      parent.querySelectorAll(".tn-tab-btn").forEach((b) => b.classList.remove("active"));
      parent.querySelectorAll(".tn-tab-content").forEach((c) => c.classList.remove("active"));

      btn.classList.add("active");
      const targetEl = document.getElementById(target);
      if (targetEl) targetEl.classList.add("active");
    });
  });
}

// 6. Simple Toast Notification
function showToast(message, type = "info") {
  let toastContainer = document.getElementById("toastContainer");
  if (!toastContainer) {
    toastContainer = document.createElement("div");
    toastContainer.id = "toastContainer";
    toastContainer.style.cssText = `
      position: fixed; bottom: 20px; right: 20px; z-index: 9999;
      display: flex; flex-direction: column; gap: 8px; pointer-events: none;
    `;
    document.body.appendChild(toastContainer);
  }

  const toast = document.createElement("div");
  const bg = type === "success" ? "#10b981" : (type === "warning" ? "#f59e0b" : "#1282a2");
  toast.style.cssText = `
    background: ${bg}; color: #ffffff; padding: 10px 18px; border-radius: 8px;
    font-size: 0.9rem; font-weight: 500; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    transition: opacity 0.3s ease; pointer-events: auto;
  `;
  toast.textContent = message;
  toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    setTimeout(() => toast.remove(), 300);
  }, 3200);
}
