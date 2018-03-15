const debug = process.env.NODE_ENV !== 'production';
const webpack = require('webpack');
const path = require('path');


const API_URLS = {
  'debug': {
    'websocket': JSON.stringify('ws://informatics.msk.ru:6349/websocket'),
  },
  'production': {
    'websocket': JSON.stringify('wss://rmatics.msk.ru/websocket'),
  }
}


module.exports = {
  context: path.join(__dirname, 'src'),
  devtool: debug ? 'inline-sourcemap' : false,
  entry: './js/index.jsx',
  module: {
    loaders: [
      {
        test: /\.jsx?$/,
        exclude: /(node_modules|bower_components)/,
        loader: 'babel-loader',
        query: {
          presets: [
            'react',
            'es2015',
            'stage-0',
          ],
          plugins: [
            'react-html-attrs',
            'transform-class-properties',
            'transform-decorators-legacy',
          ],
        }
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.(jpe?g|png|gif|eot|ttf|woff)$/,
        loaders: [
          'file-loader?hash=sha512&digest=hex&name=[hash].[ext]',
          {
            loader: 'image-webpack-loader?bypassOnDebug&optimizationLevel=7&interlaced=false',
            query: {
              mozjpeg: {
                progressive: true,
              },
              gifsicle: {
                interlaced: false,
              },
              optipng: {
                optimizationLevel: 4,
              },
              pngquant: {
                quality: '75-90',
                speed: 3,
              },
            },
          }
        ],
      },
      {
        test: /\.svg$/,
        loader: 'svg-inline-loader'
      }
    ]
  },
  output: {
    path: path.join(__dirname, 'dist'),
    filename: 'app.min.js',
  },
  plugins: debug ? [
    new webpack.optimize.OccurrenceOrderPlugin(),
    new webpack.DefinePlugin({
      '__websocket__': API_URLS['debug']['websocket'],
    })
  ] : [
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify('production'),
      '__websocket__': API_URLS['production']['websocket'],
    }),
    new webpack.optimize.OccurrenceOrderPlugin(),
    new webpack.optimize.UglifyJsPlugin({
      compress: {
        warnings: false,
        screw_ie8: true,
        conditionals: true,
        unused: true,
        comparisons: true,
        sequences: true,
        dead_code: true,
        evaluate: true,
        if_return: true,
        join_vars: true
      },
      output: {
        comments: false
      },
      mangle: true,
    }),
  ],
  resolve: {
    extensions: ['.js', '.jsx'],
  },
  devServer: {
    port: 8080,
    contentBase: path.join(__dirname, 'dist'),
    compress: true,
    disableHostCheck: true,
    historyApiFallback: true,
    proxy: {
      '/api_v2': {
        target: 'http://informatics.msk.ru:6349',
        pathRewrite: {'^/api_v2': ''},
      }
    },
  }
};
