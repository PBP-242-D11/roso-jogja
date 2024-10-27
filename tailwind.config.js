const config = {
  content: [
    // Root templates directory
    "./templates/**/*.{html,js}",

    // App-level templates directories (assuming apps are in project root)
    "./**/templates/**/*.{html,js}",

    // Include static files as well
    "./static/**/*.{js,jsx,ts,tsx}",
    "./**/static/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        "rj-orange": "#FF7043",
        "rj-grey": "#333333",
      },
    },
  },
  plugins: [],
};

export default config;
