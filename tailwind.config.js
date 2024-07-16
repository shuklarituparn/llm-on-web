/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./llm_on_web/templates/**/*.html", "./llm_on_web/static/**/*.js"],
  theme: {
    extend: {
        backgroundImage:{
            'gemma':  "url('/static/images/bg/bg2.jpg')",
        },
        fontFamily:{
            'sans1':['sans1'],
            'cassa':['cassa'],
        },
        height: {
          'custom-vh': 'calc(100vh - 6rem)',
        },
    },
  },
  plugins: [],
}
