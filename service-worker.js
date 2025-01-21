const CACHE_NAME = "bus-booking-cache-v1";
const urlsToCache = [
    "/Highway_Insight/",
    "/Highway_Insight/index.html",
    "/Highway_Insight/dashboard.html",
    "/Highway_Insight/booking.html",
    "/Highway_Insight/signin.html",
    "/Highway_Insight/signup.html",
    "/Highway_Insight/css/dashboard.css",
    "/Highway_Insight/css/signup.css",
    "/Highway_Insight/css/signin.css",
    "/Highway_Insight/css/booking.css",
    "/Highway_Insight/manifest.json",
    "/Highway_Insight/assets/images/icons/icon_72x72.png",
    "/Highway_Insight/assets/images/icons/icon_96x96.png",
    "/Highway_Insight/assets/images/icons/icon_128x128.png",
    "/Highway_Insight/assets/images/icons/icon_144x144.png",
    "/Highway_Insight/assets/images/icons/icon_152x152.png",
    "/Highway_Insight/assets/images/icons/icon_192x192.png",
    "/Highway_Insight/assets/images/icons/icon_512x512.png",
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
];

navigator.serviceWorker.register('/Highway_Insight/service-worker.js')


// Install the service worker and cache resources
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

// Cache and update requests
self.addEventListener("fetch", (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            // Return cached response or fetch from the network
            return response || fetch(event.request).catch(() => {
                if (event.request.mode === 'navigate') {
                    return caches.match('/Highway_Insight/index.html'); // Fallback to index.html
                }
                return caches.match('/fallback.html'); // Optional fallback page
            });
        })
    );
});

// Update the service worker and clean up old caches
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
