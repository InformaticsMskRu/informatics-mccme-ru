import {createStore, applyMiddleware} from 'redux';
import logger from 'redux-logger';
import promise from 'redux-promise-middleware';

import reducers from './reducers';

const middleware = applyMiddleware(
    logger,
    promise(),
);
export default createStore(reducers, middleware);