/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{astro,html,js,jsx,ts,tsx,md,mdx}"],
  theme: {
    extend: {
      // Les variables CSS contiennent des canaux RVB ("180 85 42"), pas du hex :
      // c'est ce qui permet aux modificateurs d'opacité Tailwind (bg-surface/90,
      // text-ink/70...) de fonctionner. La conversion hex -> canaux est faite
      // dans BaseLayout.astro à partir de theme.colors du config.
      colors: {
        primary: "rgb(var(--color-primary) / <alpha-value>)",
        secondary: "rgb(var(--color-secondary) / <alpha-value>)",
        accent: "rgb(var(--color-accent) / <alpha-value>)",
        surface: "rgb(var(--color-background) / <alpha-value>)",
        ink: "rgb(var(--color-text) / <alpha-value>)",
      },
      fontFamily: {
        heading: ["var(--font-heading)", "serif"],
        body: ["var(--font-body)", "sans-serif"],
      },
    },
  },
  plugins: [],
};
