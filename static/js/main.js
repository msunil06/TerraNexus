// TerraNexus Main Client Logic
document.addEventListener("DOMContentLoaded", () => {
  initTheme();
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

  // Dispatch global event for interactive components (e.g. Leaflet map)
  window.dispatchEvent(new CustomEvent("themeChanged", { detail: { theme } }));
}

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
