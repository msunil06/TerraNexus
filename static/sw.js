// TerraNexus Service Worker (PWA)
const CACHE_NAME = "terranexus-cache-v1";
const STATIC_ASSETS = [
  "/",
  "/static/css/style.css",
  "/static/css/responsive.css",
  "/static/js/main.js",
  "/static/js/search.js",
  "/static/js/map.js",
  "/static/icons/icon-192.png",
  "/static/icons/icon-512.png",
  "/static/images/logo.png",
  "/static/manifest.json"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  // Only handle GET requests and skip private/auth/admin routes
  if (event.request.method !== "GET") return;
  const url = new URL(event.request.url);

  // Never cache authentication, admin, or user personal data
  if (
    url.pathname.startsWith("/admin") ||
    url.pathname.startsWith("/auth") ||
    url.pathname.startsWith("/api/me") ||
    url.pathname.includes("login") ||
    url.pathname.includes("register") ||
    url.pathname.includes("profile") ||
    url.pathname.includes("settings")
  ) {
    return;
  }

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request).catch(() => {
        // Fallback for offline navigation
        if (event.request.mode === "navigate") {
          return caches.match("/");
        }
      });
    })
  );
});
