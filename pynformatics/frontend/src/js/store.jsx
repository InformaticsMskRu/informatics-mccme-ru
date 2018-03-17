import promise from 'redux-promise-middleware';
import storage from 'redux-persist/lib/storage';
import thunk from 'redux-thunk';
import { composeWithDevTools } from 'redux-devtools-extension';
import { applyMiddleware, createStore } from 'redux';
import { persistStore, persistReducer } from 'redux-persist';
import { createWhitelistFilter } from 'redux-persist-transform-filter';

import reducers from './reducers';
import Socket from './utils/websocket';


const persistConfig = {
  key: 'root',
  whitelist: ['group'],
  transforms: [
    createWhitelistFilter('group', ['filterGroup']),
  ],
  storage,
};

const persistedReducer = persistReducer(persistConfig, reducers);

const middleware = applyMiddleware(
  thunk,
  promise(),
);


const store = createStore(persistedReducer, composeWithDevTools(middleware));
const persistor = persistStore(store);

const socket = new Socket(__websocket__, store.dispatch.bind(store));


export {
  store,
  persistor,
};