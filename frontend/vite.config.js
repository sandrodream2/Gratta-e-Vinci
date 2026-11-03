import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 5173,
    proxy: {
      // In sviluppo le chiamate /api vengono girate al backend FastAPI
      "/api": "http://localhost:8000",
    },
  },
});
