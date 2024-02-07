import {resolve} from "path";
import {fileURLToPath, URL} from "url";
import {defineConfig} from "vite";
import vue from "@vitejs/plugin-vue";
import vuetify from "vite-plugin-vuetify";

// https://vitejs.dev/config/
export default defineConfig({
    build: {
        manifest: true, outDir: resolve("./dist"), emptyOutDir: true, rollupOptions: {
            input: {
                main: resolve("./src/main.js"),
            },
        },
    }, base: "/static/", server: {
        origin: "http://localhost:5173",
    }, plugins: [vue(), vuetify({autoImport: true})], resolve: {
        alias: [{
            find: "@", replacement: fileURLToPath(new URL("./src", import.meta.url)),
        },],
    },
});
