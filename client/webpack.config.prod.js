const Webpack = require('webpack');
const path = require('path');

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
    path: path.join(__dirname, '../fnote/static/js'),
  },
  plugins: [
    new Webpack.optimize.OccurrenceOrderPlugin(true),
    new Webpack.optimize.UglifyJsPlugin({
      compress: { warnings: false },
      sourceMap: false,
    }),
    new Webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery',
      'window.jQuery': 'jquery',
    }),
  ],
};
