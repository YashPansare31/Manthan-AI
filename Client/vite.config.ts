import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";
import { componentTagger } from "lovable-tagger";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  
  return {
    server: {
      host: "::",
      port: 8080,
      // Only proxy in development
      ...(mode === 'development' && {
        proxy: {
          '/api': {
            target: 'http://localhost:8000',
            changeOrigin: true,
            secure: false,
          }
        }
      })
    },
    plugins: [
      react(),
      mode === 'development' && componentTagger(),
    ].filter(Boolean),
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
    define: {
      // Explicitly define the API URL for production
      'import.meta.env.VITE_API_URL': JSON.stringify(
        env.VITE_API_URL || (mode === 'production' 
          ? 'https://manthan-ai-69lq.onrender.com/api' 
          : 'http://localhost:8000/api')
      ),
    },
  };
});