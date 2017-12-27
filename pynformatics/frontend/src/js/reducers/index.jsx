import { combineReducers } from 'redux';
import { reducer as form } from 'redux-form';

import context from './contextReducer';
import problems from './problemsReducer';
import statements from './statementsReducer';
import user from './userReducer';
import search from './searchReducer';

export default combineReducers({
  context,
  form,
  problems,
  statements,
  user,
  search,
})
