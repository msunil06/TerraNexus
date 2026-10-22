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
    worldCopyJump: true
  });

  // Custom Zoom Control placed top-left
  L.control.zoom({ position: "topleft" }).addTo(map);

  // Add scale bar
  L.control.scale({ imperial: true, metric: true, position: "bottomright" }).addTo(map);

  // 2. Base Tile Layers (Dark CartoDB / OpenStreetMap fallback)
  const darkTiles = L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: "abcd",
    maxZoom: 19
  });

  const streetTiles = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19
  });

  darkTiles.addTo(map);

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

  // 5. Controls (Reset view & Fullscreen)
  const resetBtn = document.getElementById("resetMapView");
  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      map.setView([20.0, 10.0], 2);
    });
  }

  const layerToggle = document.getElementById("tileLayerSelect");
  if (layerToggle) {
    layerToggle.addEventListener("change", (e) => {
      if (e.target.value === "streets") {
        map.removeLayer(darkTiles);
        streetTiles.addTo(map);
      } else {
        map.removeLayer(streetTiles);
        darkTiles.addTo(map);
      }
    });
  }

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
