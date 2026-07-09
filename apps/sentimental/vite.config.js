import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    // Built files land in the repo-level public/ dir served by Firebase Hosting
    outDir: '../../public',
    emptyOutDir: false,
  },
  server: {
    proxy: {
      '/api': {
        // Flask backend (app.py defaults to PORT 8080)
        target: 'http://localhost:8080',
        changeOrigin: true,
      },
    },
  },
})
