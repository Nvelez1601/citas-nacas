/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      boxShadow: {
        soft: "0 18px 40px rgba(47, 27, 27, 0.12)"
      }
    }
  },
  plugins: []
};
