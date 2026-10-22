# TerraNexus REST API Documentation

Base URL: `/api`

All API endpoints return JSON with standardized response structures:
```json
{
  "status": "success",
  "data": { ... }
}
```

---

## 1. Public Geography Endpoints

### `GET /api/countries`
Retrieve list of countries with optional filtering and sorting.
- **Query Parameters**:
  - `continent` (optional): Filter by continent slug (e.g. `asia`, `europe`).
  - `q` (optional): Substring search in name, capital, or ISO codes.
- **Response**: Array of countries with codes, capital, population, area, and flag emoji.

### `GET /api/countries/<identifier>`
Retrieve detailed country dossier.
- **Parameters**: `identifier` can be country slug (`india`), ISO-2 (`IN`), or ISO-3 (`IND`).
- **Response**: Full geographic, economic, and demographic attributes.

### `GET /api/countries/<identifier>/neighbors`
Retrieve bordering countries.
- **Response**: Array of neighboring nations with border type (`land`, `maritime`, `strait`) and length in km.

### `GET /api/countries/<identifier>/divisions`
Retrieve administrative divisions for a nation (e.g. Indian States, US States).

### `GET /api/continents`
Retrieve the 7 continents with surface areas and country counts.

### `GET /api/oceans` & `GET /api/oceans/<slug>`
Retrieve the 5 oceans with bathymetric sounding depths and currents.

### `GET /api/seas` & `GET /api/seas/<slug>`
Retrieve named seas catalog with filter by parent ocean.

### `GET /api/features` & `GET /api/features/<slug>`
Retrieve physical features (mountains, mountain ranges, rivers, deserts, straits, trenches).
- **Query Parameter**: `type` (`mountain`, `river`, `desert`, `strait`, `trench`).

### `GET /api/search?q=<query>&limit=15`
Global autocomplete search across countries, divisions, oceans, seas, and features.

### `GET /api/map/markers`
Retrieve geo-referenced point markers for capitals, seas, and landmarks formatted for Leaflet.js.

---

## 2. Authenticated User Endpoints

*(Requires valid session cookie)*

### `GET /api/me`
Retrieve currently logged-in user profile and permissions.

### `GET /api/me/favorites`
Retrieve list of saved countries, oceans, seas, and features.

### `POST /api/me/favorites`
Add an item to favorites.
- **Payload**:
```json
{
  "item_type": "country",
  "item_id": "india",
  "item_title": "India"
}
```

### `DELETE /api/me/favorites/<item_type>/<item_id>`
Remove an item from favorites.

### `POST /api/me/saved-locations`
Bookmark a custom map coordinate.
- **Payload**:
```json
{
  "name": "Himalayan Base Camp",
  "latitude": 28.0,
  "longitude": 86.8,
  "zoom_level": 8,
  "notes": "Research expedition checkpoint"
}
```
