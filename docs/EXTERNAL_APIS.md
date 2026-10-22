# External APIs & Map Providers

TerraNexus is designed to operate autonomously without mandatory paid external API keys. It leverages open-standard vector maps, public cartography, and self-hosted datasets.

---

## 1. Map Tiles Providers (Zero Key Required)

1. **CartoDB Dark Matter / Positron Tiles**:
   - URL: `https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png`
   - Key: None required for educational and standard exploration use.
2. **OpenStreetMap Standard Tile Layer**:
   - URL: `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`
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
