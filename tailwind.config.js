/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./llm_on_web/templates/**/*.html"],
  theme: {
    extend: {
        backgroundImage:{
            'gemma':  "url('/static/images/bg/bg2.jpg')",
        },
        fontFamily:{
            'sans1':['sans1'],
            'cassa':['cassa'],
        }

    },
  },
  plugins: [],
}
