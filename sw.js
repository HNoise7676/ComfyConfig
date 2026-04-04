self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('fetch', (event) => {
  // Must exist for the "Install" button to show up
  event.respondWith(fetch(event.request));
});