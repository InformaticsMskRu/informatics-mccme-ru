let debug = process.env.NODE_ENV !== 'production';
let webpack = require('webpack');
let path = require('path');

module.exports = {
    context: path.join(__dirname, 'src'),
    devtool: debug ? 'inline-sourcemap' : null,
    entry: './js/index.js',
    module: {
        loaders: [
            {
                test: /\.jsx?$/,
                exclude: /(node_modules|bower_components)/,
                loader: 'babel-loader',
                query: {
                    presets: ['react', 'es2015', 'stage-0'],
                    plugins: ['react-html-attrs', 'transform-class-properties', 'transform-decorators-legacy'],
                }
            }
        ]
    },
    output: {
        path: path.join(__dirname, 'dist'),
        filename: 'app.min.js',
    },
    plugins: debug ? [] : [
        new webpack.optimize.DedupePlugin(),
        new webpack.optimize.OccurrenceOrderPlugin(),
        new webpack.optimize.UglifyJsPlugin({ mangle: false, sourcemap: false }),
    ],
    externals: {
        'Config': JSON.stringify(debug ? {
            baseUrl: '/frontend/',
            apiUrl: 'http://informatics.msk.ru:6546',
        } : {
        }),
    }
};
