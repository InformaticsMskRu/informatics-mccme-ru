import { combineReducers } from 'redux';
import { reducer as form } from 'redux-form';

import context from './contextReducer';
import problems from './problemsReducer';
import statements from './statementsReducer';
import user from './userReducer';


export default combineReducers({
  context,
  form,
  problems,
  statements,
  user,
})
