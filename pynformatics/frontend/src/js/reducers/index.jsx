import {combineReducers} from 'redux';
import {reducer as form} from 'redux-form';

import context from './contextReducer';
import problems from './problemsReducer';
import statements from './statementsReducer';
import ui from './uiReducer';
import user from './userReducer';
import groups from './groupsReducer';


export default combineReducers({
  context,
  form,
  problems,
  statements,
  ui,
  user,
  groups,
})
