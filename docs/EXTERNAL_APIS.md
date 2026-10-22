# External APIs & Map Providers

TerraNexus is designed to operate autonomously without mandatory paid external API keys. It leverages open-standard vector maps, public cartography, and self-hosted datasets.

---

## 1. Map Tiles Providers (Zero Key Required)

1. **ESRI Canvas Dark Gray Base**:
   - URL: `https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}`
   - Key: 100% Free Public GIS Tiles, Zero Watermarks, Zero API Key.
2. **ESRI World Imagery (Satellite)**:
   - URL: `https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}`
   - Key: 100% Free Public Satellite Tiles, Zero Watermarks.
3. **OpenStreetMap Standard Tile Layer**:
   - URL: `https://tile.openstreetmap.org/{z}/{x}/{y}.png`
   - Key: None required under standard OSM usage policy with proper attribution.

---

## 2. Optional Commercial Enhancements

If you choose to enable commercial geocoding or satellite imagery providers in the future, configure the respective environment variables:

| Service | Environment Variable | Usage |
| :--- | :--- | :--- |
| **Mapbox Satellite** | `MAPBOX_ACCESS_TOKEN` | Ultra-high resolution global satellite raster imagery |
| **OpenCage Geocoder** | `OPENCAGE_API_KEY` | Forward and reverse geocoding fallback |
| **ExchangeRate-API** | `EXCHANGERATE_API_KEY` | Live fiat and cryptocurrency foreign exchange rates |

All core functions of TerraNexus remain 100% operational when these optional keys are omitted.
