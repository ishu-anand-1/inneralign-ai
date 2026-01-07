/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        inter: ["Inter", "sans-serif"],
      },
      colors: {
        primary: "#6C63FF",
        secondary: "#A855F7",
      },
      boxShadow: {
        card: "0 10px 30px rgba(0,0,0,0.06)",
      },
    },
  },
  plugins: [],
};
