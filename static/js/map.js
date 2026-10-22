// TerraNexus Leaflet Interactive World Map Implementation
let map = null;
let geojsonLayer = null;
let markersLayerGroup = null;
let selectedLayer = null;

document.addEventListener("DOMContentLoaded", () => {
  const mapElement = document.getElementById("worldMap");
  if (!mapElement) return;

  initTerraNexusMap(mapElement);
});

function initTerraNexusMap(container) {
  // 1. Initialize Leaflet Map centered on world coordinates
  const initialLat = container.dataset.lat ? parseFloat(container.dataset.lat) : 20.0;
  const initialLon = container.dataset.lon ? parseFloat(container.dataset.lon) : 10.0;
  const initialZoom = container.dataset.zoom ? parseInt(container.dataset.zoom) : 2;

  map = L.map(container, {
    center: [initialLat, initialLon],
    zoom: initialZoom,
    minZoom: 2,
    maxZoom: 18,
    zoomControl: false,
    worldCopyJump: true,
    scrollWheelZoom: false,
    dragging: false,
    touchZoom: false,
    doubleClickZoom: false,
    boxZoom: false,
    keyboard: false
  });

  // Custom Zoom Control placed top-left
  const zoomControl = L.control.zoom({ position: "topleft" }).addTo(map);

  // Full-Screen interactive lock logic (Requirement 8)
  let isFullScreen = false;

  function setInteractions(enabled) {
    if (enabled) {
      map.scrollWheelZoom.enable();
      map.dragging.enable();
      map.touchZoom.enable();
      map.doubleClickZoom.enable();
      map.boxZoom.enable();
      map.keyboard.enable();
    } else {
      map.scrollWheelZoom.disable();
      map.dragging.disable();
      map.touchZoom.disable();
      map.doubleClickZoom.disable();
      map.boxZoom.disable();
      map.keyboard.disable();
    }
  }

  // Initially locked
  setInteractions(false);

  function toggleFullScreen() {
    const mapCard = container.closest(".tn-map-card") || container;
    const lockBanner = document.getElementById("mapFsLockBanner");
    const exitBtn = document.getElementById("exitFsFloatingBtn");
    const toggleBtn = document.getElementById("btnMapFullScreen");

    isFullScreen = !isFullScreen;

    if (isFullScreen) {
      mapCard.classList.add("fullscreen-mode");
      setInteractions(true);
      if (lockBanner) lockBanner.classList.add("hidden");
      if (exitBtn) exitBtn.style.display = "inline-flex";
      if (toggleBtn) toggleBtn.innerHTML = "✕ Exit Full-Screen";
      document.body.style.overflow = "hidden";
    } else {
      mapCard.classList.remove("fullscreen-mode");
      setInteractions(false);
      if (lockBanner) lockBanner.classList.remove("hidden");
      if (exitBtn) exitBtn.style.display = "none";
      if (toggleBtn) toggleBtn.innerHTML = "⛶ Enter Full-Screen";
      document.body.style.overflow = "";
    }

    setTimeout(() => {
      map.invalidateSize();
    }, 200);
  }

  const fsBtn = document.getElementById("btnMapFullScreen");
  if (fsBtn) fsBtn.addEventListener("click", toggleFullScreen);

  const bannerBtn = document.getElementById("bannerEnterFsBtn");
  if (bannerBtn) bannerBtn.addEventListener("click", toggleFullScreen);

  const exitFloating = document.getElementById("exitFsFloatingBtn");
  if (exitFloating) exitFloating.addEventListener("click", toggleFullScreen);

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && isFullScreen) {
      toggleFullScreen();
    }
  });

  // User feedback on clicking locked map
  map.on("mousedown", () => {
    if (!isFullScreen) {
      const banner = document.getElementById("mapFsLockBanner");
      if (banner) {
        banner.style.boxShadow = "0 0 25px rgba(245, 158, 11, 0.9)";
        banner.style.borderColor = "#f59e0b";
        setTimeout(() => {
          banner.style.boxShadow = "";
          banner.style.borderColor = "";
        }, 800);
      }
    }
  });

  // Add scale bar
  L.control.scale({ imperial: true, metric: true, position: "bottomright" }).addTo(map);

  // 2. Base Tile Layers (100% Free Public APIs - Zero API Key Required)
  const tileLayers = {
    satellite: L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", {
      attribution: 'Tiles &copy; Esri &mdash; High-Resolution Satellite & Aerial Imagery (Free Public)',
      maxZoom: 18
    }),
    dark: L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}", {
      attribution: 'Tiles &copy; Esri &mdash; Esri Dark Canvas (Zero API Key)',
      maxZoom: 16
    }),
    light: L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}", {
      attribution: 'Tiles &copy; Esri &mdash; Esri World Street (Zero API Key)',
      maxZoom: 18
    }),
    streets: L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 19
    }),
    topo: L.tileLayer("https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png", {
      attribution: '&copy; <a href="https://opentopomap.org">OpenTopoMap</a> & OpenStreetMap',
      maxZoom: 17
    })
  };

  const initialTheme = document.documentElement.getAttribute("data-theme") || "dark";
  let activeTileKey = initialTheme === "light" ? "light" : "dark";
  tileLayers[activeTileKey].addTo(map);

  function switchTileLayer(key) {
    if (!tileLayers[key] || key === activeTileKey) return;
    map.removeLayer(tileLayers[activeTileKey]);
    tileLayers[key].addTo(map);
    activeTileKey = key;
  }

  // 3. Layer Groups
  markersLayerGroup = L.layerGroup().addTo(map);

  // 4. Track mouse coordinates
  const coordsPill = document.getElementById("coordsDisplay");
  if (coordsPill) {
    map.on("mousemove", (e) => {
      const lat = e.latlng.lat.toFixed(4);
      const lng = e.latlng.lng.toFixed(4);
      coordsPill.textContent = `${lat}° N, ${lng}° E`;
    });
  }

  // 5. Controls (Reset view & Layer Toggle)
  const resetBtn = document.getElementById("resetMapView");
  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      map.setView([20.0, 10.0], 2);
    });
  }

  const layerToggle = document.getElementById("tileLayerSelect");
  if (layerToggle) {
    layerToggle.value = activeTileKey;
    layerToggle.addEventListener("change", (e) => {
      switchTileLayer(e.target.value);
    });
  }

  // Sync with global website theme toggle (Dark / Light)
  window.addEventListener("themeChanged", (e) => {
    const nextTheme = e.detail && e.detail.theme;
    if (layerToggle && (activeTileKey === "dark" || activeTileKey === "light")) {
      const targetLayer = nextTheme === "light" ? "light" : "dark";
      switchTileLayer(targetLayer);
      layerToggle.value = targetLayer;
    }
  });

  // 6. Load Boundaries (GeoJSON) and Markers
  loadCountryBoundaries();
  loadMapMarkers();
}

// Load vector boundaries
async function loadCountryBoundaries() {
  try {
    const res = await fetch("/static/data/world_countries.json");
    if (!res.ok) return;

    const geoData = await res.json();

    geojsonLayer = L.geoJSON(geoData, {
      style: (feature) => ({
        fillColor: "#034078",
        weight: 1.5,
        opacity: 0.8,
        color: "#00f5d4",
        dashArray: "2",
        fillOpacity: 0.2
      }),
      onEachFeature: (feature, layer) => {
        layer.on({
          mouseover: (e) => {
            const l = e.target;
            if (l !== selectedLayer) {
              l.setStyle({
                fillColor: "#00f5d4",
                fillOpacity: 0.45,
                weight: 2
              });
            }
          },
          mouseout: (e) => {
            if (e.target !== selectedLayer) {
              geojsonLayer.resetStyle(e.target);
            }
          },
          click: (e) => {
            highlightFeature(e.target);
            displayCountryPanel(feature.properties);
          }
        });
      }
    }).addTo(map);
  } catch (err) {
    console.warn("GeoJSON boundaries skipped or local fallback:", err);
  }
}

function highlightFeature(layer) {
  if (selectedLayer && geojsonLayer) {
    geojsonLayer.resetStyle(selectedLayer);
  }
  selectedLayer = layer;
  selectedLayer.setStyle({
    fillColor: "#00f5d4",
    fillOpacity: 0.6,
    weight: 2.5,
    color: "#ffffff"
  });
  if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
    selectedLayer.bringToFront();
  }
}

// Load interactive markers (Capitals, Seas, Physical Features)
async function loadMapMarkers() {
  try {
    const res = await fetch("/api/map/markers");
    if (!res.ok) return;

    const json = await res.json();
    const markers = json.data || [];

    markers.forEach((m) => {
      let iconColor = "#00f5d4";
      let iconSymbol = "📍";

      if (m.type === "country") {
        iconSymbol = m.flag || "🏛️";
      } else if (m.type === "sea") {
        iconSymbol = "⛵";
      } else if (m.type === "mountain" || m.type === "mountain_range") {
        iconSymbol = "🏔️";
      } else if (m.type === "river" || m.type === "strait") {
        iconSymbol = "🌊";
      } else if (m.type === "trench") {
        iconSymbol = "⚓";
      }

      const customIcon = L.divIcon({
        className: "tn-custom-marker",
        html: `<div style="
          background: rgba(10, 19, 36, 0.9);
          border: 1.5px solid #00f5d4;
          border-radius: 50%;
          width: 28px;
          height: 28px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 14px;
          box-shadow: 0 0 10px rgba(0, 245, 212, 0.4);
        ">${iconSymbol}</div>`,
        iconSize: [28, 28],
        iconAnchor: [14, 14]
      });

      const marker = L.marker([m.lat, m.lon], { icon: customIcon });

      marker.bindPopup(`
        <div style="color: #060c18; padding: 4px;">
          <h4 style="margin: 0 0 4px; font-size: 1rem; font-weight: 700;">${m.name}</h4>
          ${m.capital ? `<p style="margin: 0 0 4px; font-size: 0.85rem;">Capital: <strong>${m.capital}</strong></p>` : ""}
          ${m.population ? `<p style="margin: 0 0 4px; font-size: 0.85rem;">Population: <strong>${m.population.toLocaleString()}</strong></p>` : ""}
          <a href="${m.url}" style="display: inline-block; margin-top: 6px; font-size: 0.82rem; font-weight: 600; color: #034078;">Explore Details &rarr;</a>
        </div>
      `);

      marker.addTo(markersLayerGroup);
    });
  } catch (err) {
    console.error("Error loading map markers:", err);
  }
}

// Display Slideout Info Panel
function displayCountryPanel(props) {
  const panel = document.getElementById("mapInfoPanel");
  if (!panel) return;

  const titleEl = document.getElementById("panelTitle");
  const descEl = document.getElementById("panelBody");
  const linkEl = document.getElementById("panelLink");

  if (titleEl) titleEl.textContent = props.name;
  if (descEl) {
    descEl.innerHTML = `
      <p style="margin-bottom: 6px; font-size: 0.88rem; color: var(--text-secondary);">
        Capital: <strong style="color: var(--text-primary);">${props.capital || "N/A"}</strong>
      </p>
      <p style="margin-bottom: 6px; font-size: 0.88rem; color: var(--text-secondary);">
        ISO Code: <strong style="color: var(--text-primary);">${props.iso_a3 || props.iso_a2}</strong>
      </p>
    `;
  }
  if (linkEl) {
    linkEl.href = `/countries/${props.slug}`;
    linkEl.style.display = "inline-flex";
  }

  panel.style.display = "block";
}

function closeMapPanel() {
  const panel = document.getElementById("mapInfoPanel");
  if (panel) panel.style.display = "none";
  if (selectedLayer && geojsonLayer) {
    geojsonLayer.resetStyle(selectedLayer);
    selectedLayer = null;
  }
}
