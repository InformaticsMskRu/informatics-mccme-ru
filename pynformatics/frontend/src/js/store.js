import {createStore, applyMiddleware} from 'redux';
import logger from 'redux-logger';
import promise from 'redux-promise-middleware';
import thunk from 'redux-thunk';

import reducers from './reducers';


const middleware = applyMiddleware(
    thunk,
    logger,
    promise(),
);
export default createStore(reducers, middleware);