var path = require("path");
var webpack = require("webpack");
var Promise = require("es6-promise").Promise;
require("es6-promise").polyfill();
const config = require("./src/config/config.json");

module.exports = {
  entry: "./src/main.js",
  output: {
    path: path.resolve(__dirname, "./dist"),
    publicPath: `${config.PATH}/dist/`,
    filename: "build.js"
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ["vue-style-loader", "css-loader"]
      },
      {
        test: /\.vue$/,
        loader: "vue-loader",
        options: {
          loaders: {}
          // other vue-loader options go here
        }
      },
      {
        test: /\.js$/,
        loader: "babel-loader",
        exclude: /node_modules/
      },
      {
        test: /\.(png|jpg|gif)$/,
        loader: "file-loader",
        options: {
          name: "assets/images/[name].[ext]?"
        }
      },
      {
        test: /\.(woff|woff2|eot|ttf|svg)$/,
        loader: "url-loader?limit=100000"
      }
    ]
  },
  resolve: {
    alias: {
      vue$: "vue/dist/vue.esm.js"
    },
    // extensions: ['*', '.js', '.vue', '.json']
    extensions: [
      ".wasm",
      ".ts",
      ".tsx",
      ".mjs",
      ".cjs",
      ".js",
      ".json",
      ".vue",
      ".woff2",
      ".woff"
    ]
  },
  devServer: {
    host: "localhost",
    port: 8095,
    historyApiFallback: true,
    noInfo: true,
    overlay: true
  },
  performance: {
    hints: false
  },
  devtool: "#eval-source-map",
  plugins: [
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
      moment: "moment"
    })
  ]
};
