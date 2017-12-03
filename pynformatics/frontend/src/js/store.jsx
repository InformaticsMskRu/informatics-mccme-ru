import { createStore, applyMiddleware } from 'redux';
import { composeWithDevTools } from 'redux-devtools-extension';
import promise from 'redux-promise-middleware';
import thunk from 'redux-thunk';

import reducers from './reducers';


const middleware = applyMiddleware(
  thunk,
  promise(),
);
export default createStore(reducers, composeWithDevTools(middleware));