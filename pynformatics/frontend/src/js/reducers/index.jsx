import { combineReducers } from 'redux';
import { reducer as form } from 'redux-form';

import context from './contextReducer';
import group from './groupReducer';
import problems from './problemsReducer';
import statements from './statementsReducer';
import ui from './uiReducer';
import user from './userReducer';


export default combineReducers({
  context,
  group,
  form,
  problems,
  statements,
  ui,
  user,
})
