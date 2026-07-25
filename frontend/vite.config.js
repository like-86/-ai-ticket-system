import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      // /api 转发到你的 FastAPI 后端地址
      '/api': {
        target: 'http://127.0.0.1:8000', // 后端uvicorn地址
        changeOrigin: true,
      }
    }
  }
})