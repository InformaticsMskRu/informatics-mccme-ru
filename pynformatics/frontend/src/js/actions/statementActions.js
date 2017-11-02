import axios from 'axios';

import * as config from 'Config';


export function fetchStatement(statementId) {
    return (dispatch) => {
        const url = `${config.apiUrl}/statement/${statementId}`;
        dispatch({
            type: 'GET_STATEMENT',
            payload: axios.get(url),
            meta: {
                statementId,
            }
        })
    }
}
