import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5175,
    proxy: {
      '/api/reviews': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/api/test-cases/generate': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
    },
  },
})
