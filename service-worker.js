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
    "/assets/images/icons/icon_72x72.png",
    "/assets/images/icons/icon_96x96.png",
    "/assets/images/icons/con_128x128.png",
    "/assets/images/icons/icon_144x144.png",
    "/assets/images/icons/icon_152x152.png",
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
];

// Install the service worker and cache resources
self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log("Opened cache");
            return cache.addAll(urlsToCache);
        })
    );
});

// Cache and update requests
self.addEventListener("fetch", (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});

// Update the service worker
self.addEventListener("activate", (event) => {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (!cacheWhitelist.includes(cacheName)) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});
