/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
  extend: {
    colors: {
      primary: {
        light: '#60a5fa',   // آبی روشن
        DEFAULT: '#2563eb', // آبی اصلی
        dark: '#1e3a8a'     // آبی تیره
      },
      secondary: {
        light: '#fbbf24',   // زرد روشن
        DEFAULT: '#f59e0b', // زرد اصلی
        dark: '#b45309'     // زرد تیره
      },
      accent: {
        light: '#34d399',   // سبز فیروزه‌ای
        DEFAULT: '#10b981', // سبز اصلی
        dark: '#047857'     // سبز تیره
      },
      background: {
        light: '#f8fafc',   // پس‌زمینه روشن
        dark: '#0f172a'     // پس‌زمینه تیره
      },
      surface: {
        light: '#ffffff',
        dark: '#1e293b'
      },
      text: {
        light: '#1e293b',
        dark: '#f8fafc'
      }
    },
  },
},
plugins: [],

}
