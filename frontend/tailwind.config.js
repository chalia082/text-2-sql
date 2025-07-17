/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
			fontFamily: {
        sans: ['"Geist"', 'sans-serif'],
      },
      colors: {
        'wl-red': '#EE2D3D',
        'accent2': '#602CF3',
        'accent3': '#48B9FD',
        'accent4': '#140C64',
        'accent5': '#872CC1',
        'accent6': '#C10D68',
        'gray': '#9A9A9A',
      },
		},
  },
  plugins: [],
}
