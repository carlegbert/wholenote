const Webpack = require('webpack');
const path = require('path');

/** Depending on how the project is being served, this plugin
 *  may be wanted.
 *
 * const HTMLWebpackPluginConfig = new HTMLWebpackPlugin({
 *   template: path.join(__dirname, '/app/index.html'),
 *   filename: 'index.html',
 *   inject: 'head',
 * });
 *
**/

const jqPlugin = new Webpack.ProvidePlugin({
  $: 'jquery',
  jQuery: 'jquery',
  'window.jQuery': 'jquery',
});

module.exports = {
  entry: path.join(__dirname, '/app/main.js'),
  module: {
    loaders: [
      {
        test: /\.css$/,
        loader: 'style-loader!css-loader',
      }, {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'babel-loader',
      },
    ],
  },
  output: {
    filename: 'bundle.js',
    path: path.join(__dirname, '/build'),
  },
  plugins: [
    jqPlugin,
    new Webpack.optimize.OccurrenceOrderPlugin(true),
    new Webpack.optimize.UglifyJsPlugin({
      compress: { warnings: false },
      sourceMap: false,
    }),
  ],
};
