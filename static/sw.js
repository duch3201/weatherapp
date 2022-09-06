const cacheName = 'sw-cache-v1';
const cacheFiles = [
    '/',
    '/templates/index.html',
    '/static/sw.js',
    '/static/cloud_foggy.svg',
    '/static/cloud_thunder.svg',
    '/static/cloud_rain.svg',
    '/static/cloud_snow.svg',
    '/static/day_cloud_rain.svg',
    '/static/sunny.svg',
];

self.addEventListener('install', function(event) {
    const cache = await caches.open(cacheName);
    await cache.addAll(staticAssets);
    return self.skipWaiting();
});

window.addEventListener("load", () => {
    if ("serviceWorker" in navigator) {
      navigator.serviceWorker.register("service-worker.js");
    }
  });

self.addEventListener('activate', e => {
    self.clients.claim();
});