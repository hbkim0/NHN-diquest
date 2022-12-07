const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  pluginOptions: {
    mock: { entry: './mock/index.js', debug: true },
  },
  transpileDependencies: [
    'vuetify'
  ]
})
