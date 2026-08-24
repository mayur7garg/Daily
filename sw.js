const CACHE_NAME = 'daily-cache-v4';
const urlsToCache = [
  './index.html',
  './styles.css',
  './favicon.png',
  './manifest.json',
  './app.js'
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
        // Only cache GET requests and valid responses (status 200 or opaque)
        if (event.request.method === 'GET' && (response.status === 200 || response.status === 0)) {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseClone);
          }).catch(err => console.error('Cache put error:', err));
        }
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
