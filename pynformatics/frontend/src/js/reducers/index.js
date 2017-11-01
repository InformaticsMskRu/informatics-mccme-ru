import { combineReducers } from 'redux';
import { reducer as form } from 'redux-form';

import problems from './problemsReducer';


export default combineReducers({
    problems,
    form,
})
