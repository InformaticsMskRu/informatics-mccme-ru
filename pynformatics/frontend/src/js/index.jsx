import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';

import * as config from 'Config';

import App from './components/App';
import store from './store';


ReactDOM.render(
  <Provider store={store}>
    <BrowserRouter basename={config.baseUrl}>
      <App />
    </BrowserRouter>
  </Provider>,
  document.getElementById('app'),
);
