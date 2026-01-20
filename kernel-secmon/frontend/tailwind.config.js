/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                cyber: {
                    black: "#050505",
                    dark: "#0a0a0f",
                    card: "#12121a",
                    border: "#1f2937",
                    primary: "#00ff9d",   // Neon Green
                    secondary: "#00f0ff", // Neon Cyan
                    alert: "#ff003c",     // Cyber Red
                    warning: "#fcee0a",   // Cyber Yellow
                }
            },
            fontFamily: {
                mono: ['"Courier New"', 'Courier', 'monospace'],
                display: ['"Orbitron"', 'sans-serif'],
            },
            animation: {
                'pulse-fast': 'pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'flicker': 'flicker 0.15s infinite',
            },
            keyframes: {
                flicker: {
                    '0%': { opacity: 0.9 },
                    '50%': { opacity: 1.0 },
                    '100%': { opacity: 0.85 },
                }
            }
        },
    },
    plugins: [],
}
