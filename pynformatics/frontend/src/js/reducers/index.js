import { combineReducers } from 'redux';
import { reducer as form } from 'redux-form';

import problems from './problemsReducer';
import statements from './statementsReducer';


export default combineReducers({
    form,
    problems,
    statements,
})
