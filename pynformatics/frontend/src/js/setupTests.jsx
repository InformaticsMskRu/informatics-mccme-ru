import axios from 'axios';
import configureMockStore from 'redux-mock-store'
import promise from 'redux-promise-middleware';
import thunk from 'redux-thunk';
import MockAdapter from 'axios-mock-adapter';

global.axiosMock = new MockAdapter(axios);

global.middlewares = [
  thunk,
  promise(),
];
global.mockStore = configureMockStore(middlewares);
