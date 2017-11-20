import * as _ from 'lodash';

import axios from '../utils/axios';


export function fetchStatement(statementId) {
  return (dispatch) => {
    const url = `/statement/${statementId}`;
    return dispatch({
      type: 'GET_STATEMENT',
      payload: axios.get(url),
      meta: {
        statementId,
      },
    });
  };
}


export function setSettings(statementId, settings) {
  return (dispatch) => {
    const url = `/statement/${statementId}/set_settings`;

    const formData = new FormData();
    _.each(settings, (value, key) => formData.append(key, value));

    return dispatch({
      type: 'POST_STATEMENT_SET_SETTINGS',
      payload: axios.post(
        url,
        settings,
        {
          headers: {
            'Content-Type': 'application/json',
          },
        },
      ),
      meta: {
        statementId,
      },
    });
  };
}
