const CACHE_NAME = "bus-booking-cache-v1";
const urlsToCache = [
    "/",
    "/index.html",
    "/dashboard.html",
    "/booking.html",
    "/signin.html",
    "/signup.html",
    "/css/dashboard.css",
    "/css/signup.css",
    "/css/signin.css",
    "/css/booking.css",
    "/manifest.json",
    "/assets/images/icons/icon_72x72.png",
    "/assets/images/icons/icon_96x96.png",
    "/assets/images/icons/icon_128x128.png",
    "/assets/images/icons/icon_144x144.png",
    "/assets/images/icons/icon_152x152.png",
    "/assets/images/icons/icon_192x192.png",
    "/assets/images/icons/icon_512x512.png",
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
];

self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log("Opened cache");
            return cache.addAll(urlsToCache).catch((error) => {
                console.error("Failed to cache resources during install", error);
            });
        })
    );
});

self.addEventListener("fetch", (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request).then((fetchResponse) => {
                return caches.open(CACHE_NAME).then((cache) => {
                    cache.put(event.request, fetchResponse.clone());
                    return fetchResponse;
                });
            }).catch((error) => {
                console.error("Fetch failed, returning cached content if available", error);
                return caches.match(event.request);
            });
        })
    );
});

self.addEventListener("activate", (event) => {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (!cacheWhitelist.includes(cacheName)) {
                        console.log(`Deleting old cache: ${cacheName}`);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => {
            console.log("Service Worker activated and old caches cleared");
        })
    );
});
