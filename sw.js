const CACHE_NAME = 'daily-cache-v2';
const urlsToCache = [
  './',
  './index.html',
  './styles.css',
  './favicon.png',
  './manifest.json',
  './app.js',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    fetch(event.request)
      .then(response => {
        // Network was successful, clone response and update cache
        const responseClone = response.clone();
        caches.open(CACHE_NAME).then(cache => {
          cache.put(event.request, responseClone);
        });
        return response;
      })
      .catch(() => {
        // Network failed, fallback to cache
        return caches.match(event.request, { ignoreSearch: true })
          .then(cachedResponse => {
            if (cachedResponse) {
              return cachedResponse;
            }
            // If it's a navigation request and nothing matches, fallback to index.html
            if (event.request.mode === 'navigate') {
              return caches.match('./index.html');
            }
          });
      })
  );
});
