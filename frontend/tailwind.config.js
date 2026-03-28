/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts}'],
  theme: {
    extend: {
      colors: {
        dark: {
          900: '#0a0a0f',
          800: '#111118',
          700: '#1a1a24',
          600: '#24242f',
          500: '#2e2e3a',
        },
        accent: {
          500: '#6c63ff',
          400: '#8b85ff',
          600: '#5248cc',
        }
      }
    }
  },
  plugins: []
}
