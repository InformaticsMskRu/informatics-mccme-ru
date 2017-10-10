import React from 'react';
import ReactDOM from 'react-dom';
import {Provider} from 'react-redux';
import {BrowserRouter, HistoryLocation} from 'react-router-dom'

import * as config from 'Config';

import store from './store';
import App from './components/App';

// for debug purposes
window.store = store;

ReactDOM.render(
    <Provider store={store}>
        <BrowserRouter basename={config.baseUrl}>
            <App/>
        </BrowserRouter>
    </Provider>,
    document.getElementById('app')
);
