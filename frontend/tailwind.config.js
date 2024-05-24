const {nextui} = require("@nextui-org/react");

/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./app/**/*.{js,ts,jsx,tsx,mdx}",
        "./pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./components/**/*.{js,ts,jsx,tsx,mdx}",

        // Or if using `src` directory:
        "./src/**/*.{js,ts,jsx,tsx,mdx}",
        "./node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {},
    },
    darkMode: "class",
    plugins: [
        nextui({
            themes: {
                dark: {
                    colors: {
                        background: "#191919",
                        foreground: "#eeeeee",
                        content1: "#232323",
                        danger: {
                            DEFAULT: '#EF4444',
                            foreground: '#eee'
                        }
                    },
                },
                light: {
                    colors: {
                        background: "#eeeeee",
                        foreground: "#191919",
                        content1: "#eeeeee",
                        danger: {
                            DEFAULT: '#EF4444',
                            foreground: '#eee'
                        }
                    },
                },
            },
        }),
    ],
};
