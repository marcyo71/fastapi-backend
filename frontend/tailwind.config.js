export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#2563eb',     // blu intenso
        secondary: '#f3f4f6',   // grigio chiaro
        accent: '#10b981',      // verde brillante
        danger: '#ef4444',      // rosso
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      borderRadius: {
        md: '0.5rem',
        lg: '1rem',
      },
    },
  },
  plugins: [],
}
