import { combineReducers } from 'redux';
import { reducer as form } from 'redux-form';

import context from './contextReducer';
import group from './groupReducer';
import problems from './problemsReducer';
import problem_request_review from './problemRequestReviewReducer';
import problem_requests_list from './problemRequestsListReducer';
import statements from './statementsReducer';
import ui from './uiReducer';
import user from './userReducer';
import routing from './routingReducer';


export default combineReducers({
  context,
  group,
  form,
  problems,
  problem_request_review,
  problem_requests_list,
  statements,
  ui,
  user,
  routing
})
