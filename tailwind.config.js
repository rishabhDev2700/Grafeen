/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html'
  ],
  theme: {
    extend: {
      fontFamily: {
        bebas: ["Bebas Neue", "sans-serif"],
        urbanist: ["Urbanist", "sans-serif"],
      },
      boxShadow: {
        "3xl": "8px 8px 0px rgba(0, 0, 0, 1)",
        "button": "3px 3px 0px rgba(0, 0, 0, 1)",
      },
      width: {
        "card": "22rem"
      },
      height: {
        "card": "38rem"
      }
    },
  },
  plugins: [],
};
