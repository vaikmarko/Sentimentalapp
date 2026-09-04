import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { VitePWA } from "vite-plugin-pwa";

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    VitePWA({
      registerType: "autoUpdate",
      manifest: {
        name: "Sentimental",
        short_name: "Sentimental",
        description: "Talk for two minutes — get back a short, true story in your own words, kept private on your shelf.",
        theme_color: "#0E0C12",
        background_color: "#0E0C12",
        display: "standalone",
        orientation: "portrait",
        icons: [
          { src: "/icons/icon-192.png", sizes: "192x192", type: "image/png" },
          { src: "/icons/icon-512.png", sizes: "512x512", type: "image/png" },
          { src: "/icons/icon-512-maskable.png", sizes: "512x512", type: "image/png", purpose: "maskable" },
        ],
      },
      workbox: {
        // Never cache API responses at the SW layer; the app manages its own data.
        navigateFallbackDenylist: [/^\/api\//, /^\/s\//],
      },
    }),
  ],
  server: {
    proxy: {
      "/api": "http://localhost:8000",
    },
  },
  test: {
    environment: "jsdom",
    globals: true,
  },
});
