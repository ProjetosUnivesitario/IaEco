/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#069E6E',
        'primary-hover': '#009889',
        'secondary': '#3E7996',
        'tertiary': '#2D2E47',
        'quaternary': '#00BAB4',
        'quinary': '#2F6C82',
        'success': '#3ad29f',
        'warning': '#eea303',
        'danger': '#dc3545',
        'danger-hover': '#e35d6a',
      },
    },
  },
  plugins: [],
};
