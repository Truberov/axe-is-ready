// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: false },
  ssr: false,
  modules: [
    '@nuxtjs/tailwindcss',
    '@nuxtjs/eslint-module',
    'nuxt-quasar-ui',
    'nuxt-mdi',
  ],
  quasar: {
    plugins: [
      'Notify',
    ],
    lang: 'ru',

    config: {
      brand: {
        primary: '#333',
        secondary: '#eaebed',
      },
    },
  },
  css: ['@/assets/css/tailwind.css', '@/assets/css/main.css'],
  runtimeConfig: {
    public: {
      baseURL: 'http://158.160.164.237:8080',
      headers: {},
    },
  },

});
