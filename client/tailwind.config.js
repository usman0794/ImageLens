/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      colors: {
        brand: {
          50: '#eef7ff',
          100: '#d9edff',
          200: '#bce0ff',
          300: '#8ecbff',
          400: '#59a9ff',
          500: '#3386ff',
          600: '#1f66f2',
          700: '#174edc',
          800: '#1a40b2',
          900: '#1b3c8c',
        },
      },
      boxShadow: {
        soft: '0 20px 60px -24px rgba(15, 23, 42, 0.45)',
        glow: '0 24px 80px -28px rgba(51, 134, 255, 0.65)',
      },
      backgroundImage: {
        mesh: 'radial-gradient(circle at top left, rgba(51,134,255,.22), transparent 28rem), radial-gradient(circle at 85% 15%, rgba(168,85,247,.16), transparent 24rem), linear-gradient(180deg, rgba(255,255,255,.94), rgba(248,250,252,.98))',
        'mesh-dark': 'radial-gradient(circle at top left, rgba(51,134,255,.22), transparent 28rem), radial-gradient(circle at 85% 15%, rgba(168,85,247,.18), transparent 24rem), linear-gradient(180deg, rgba(2,6,23,.98), rgba(15,23,42,.98))',
      },
    },
  },
  plugins: [],
}
