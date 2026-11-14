/* Violet's Prompt Writer — offline app shell.
   Written by an AI assistant as part of a work-in-progress project. */

const CACHE_NAME = 'vpw-shell-v4';
const SHELL = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable-512.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE_NAME);
    await Promise.all(SHELL.map(async (url) => {
      try {
        await cache.add(new Request(url, { cache: 'reload' }));
      } catch (err) {
        // A missing optional asset should not block installation.
      }
    }));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(
      keys
        .filter((key) => key.startsWith('vpw-shell-') && key !== CACHE_NAME)
        .map((key) => caches.delete(key))
    );
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return; // Never intercept the remote tag CSV.

  if (request.mode === 'navigate') {
    event.respondWith((async () => {
      try {
        const fresh = await fetch(request);
        if (fresh.ok) {
          const cache = await caches.open(CACHE_NAME);
          await cache.put('./index.html', fresh.clone());
        }
        return fresh;
      } catch (err) {
        const cache = await caches.open(CACHE_NAME);
        return (await cache.match(request)) || (await cache.match('./index.html')) || Response.error();
      }
    })());
    return;
  }

  event.respondWith((async () => {
    const cache = await caches.open(CACHE_NAME);
    const cached = await cache.match(request);
    if (cached) {
      event.waitUntil(
        fetch(request)
          .then(async (fresh) => {
            if (fresh.ok) await cache.put(request, fresh.clone());
          })
          .catch(() => {})
      );
      return cached;
    }
    try {
      const fresh = await fetch(request);
      if (fresh.ok) await cache.put(request, fresh.clone());
      return fresh;
    } catch (err) {
      return new Response('', { status: 504, statusText: 'Offline' });
    }
  })());
});
