import { createStore, applyMiddleware } from 'redux';
import { createLogger } from 'redux-logger';
import promise from 'redux-promise-middleware';
import thunk from 'redux-thunk';

import reducers from './reducers';


const middleware = applyMiddleware(
    thunk,
    promise(),
    createLogger({
        collapsed: true,
    }),
);
export default createStore(reducers, middleware);