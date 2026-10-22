import time
import requests
from api.config import API_REGISTRY, get_all_apis, update_api_url

class ApiGateway:
    """
    Unified API Gateway & Diagnostics Hub.
    Monitors live connections to all external services, measures latency,
    and handles graceful fallback if any provider experiences downtime.
    """

    @staticmethod
    def test_single_api(api_id):
        """Test live HTTP connectivity and measure roundtrip latency to an API."""
        cfg = API_REGISTRY.get(api_id)
        if not cfg:
            return {"status": "error", "message": f"API ID '{api_id}' not found"}

        ping_url = cfg.get("ping_url") or cfg.get("url")
        start_time = time.time()
        headers = {"User-Agent": "TerraNexus-Atlas/2.0 (Academic & Educational Research)"}

        try:
            res = requests.get(ping_url, headers=headers, timeout=5)
            latency_ms = round((time.time() - start_time) * 1000, 1)

            if res.status_code in (200, 201, 204, 304):
                return {
                    "id": api_id,
                    "name": cfg["name"],
                    "status": "connected",
                    "status_code": res.status_code,
                    "latency_ms": latency_ms,
                    "is_healthy": True,
                    "badge": "🟢 Connected",
                    "url": cfg["url"]
                }
            else:
                return {
                    "id": api_id,
                    "name": cfg["name"],
                    "status": "degraded",
                    "status_code": res.status_code,
                    "latency_ms": latency_ms,
                    "is_healthy": False,
                    "badge": f"🟡 HTTP {res.status_code}",
                    "url": cfg["url"]
                }
        except requests.exceptions.Timeout:
            return {
                "id": api_id,
                "name": cfg["name"],
                "status": "timeout",
                "status_code": None,
                "latency_ms": 5000.0,
                "is_healthy": False,
                "badge": "⏱️ Timeout (>5s)",
                "url": cfg["url"]
            }
        except Exception as e:
            return {
                "id": api_id,
                "name": cfg["name"],
                "status": "offline",
                "status_code": None,
                "latency_ms": None,
                "is_healthy": False,
                "badge": "🔴 Offline",
                "url": cfg["url"],
                "error": str(e)
            }

    @classmethod
    def test_all_connections(cls):
        """Benchmark all external APIs registered in the system."""
        results = []
        for api_id in API_REGISTRY:
            res = cls.test_single_api(api_id)
            # Attach metadata
            res["category"] = API_REGISTRY[api_id]["category"]
            res["is_free"] = API_REGISTRY[api_id]["is_free"]
            res["description"] = API_REGISTRY[api_id]["description"]
            results.append(res)
        return results

    @classmethod
    def search_location_free_api(cls, query, limit=5):
        """
        Query the Nominatim OpenStreetMap Free Public Geocoding API.
        Zero API keys required. Returns geographic coordinates and bounding boxes.
        """
        if not query or len(query.strip()) < 2:
            return []

        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": query.strip(),
            "format": "json",
            "addressdetails": 1,
            "limit": limit
        }
        headers = {
            "User-Agent": "TerraNexus-Atlas/2.0 (Geography Search Engine)"
        }

        try:
            res = requests.get(url, params=params, headers=headers, timeout=4)
            if res.ok:
                items = res.json()
                results = []
                for item in items:
                    results.append({
                        "name": item.get("display_name"),
                        "type": item.get("type", "feature"),
                        "category": item.get("class", "place"),
                        "lat": float(item.get("lat")),
                        "lon": float(item.get("lon")),
                        "boundingbox": item.get("boundingbox"),
                        "source": "Nominatim OpenStreetMap Free API"
                    })
                return results
        except Exception:
            pass
        return []
