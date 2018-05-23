import { combineReducers } from 'redux';
import { reducer as form } from 'redux-form';

import context from './contextReducer';
import group from './groupReducer';
import problems from './problemsReducer';
import problemRequestReview from './problemRequestReviewReducer';
import problemRequestsList from './problemRequestsListReducer';
import statements from './statementsReducer';
import ui from './uiReducer';
import user from './userReducer';
import routing from './routingReducer';


export default combineReducers({
  context,
  group,
  form,
  problems,
  problemRequestReview,
  problemRequestsList,
  statements,
  ui,
  user,
  routing
})
