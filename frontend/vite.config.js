import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 8501,
    open: false,
    proxy: {
      '/api': {
        target: 'http://localhost:8432',
        changeOrigin: true,
      },
    },
  },
})
