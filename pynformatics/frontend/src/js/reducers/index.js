import { combineReducers } from 'redux';
import { reducer as form } from 'redux-form';

import problem from './problemReducer';


export default combineReducers({
    problem,
    form,
})
