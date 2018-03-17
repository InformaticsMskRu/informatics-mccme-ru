import clone from 'clone';
import * as _ from 'lodash';

import axios from '../utils/axios';
import { processStandingsData } from '../utils/standings';


export function fetchStatement(statementId) {
  return (dispatch) => {
    const url = `/statement/${statementId}`;
    return dispatch({
      type: 'GET_STATEMENT',
      payload: axios.get(url, {
        params: {additional_fields: ['runs']},
      }),
      meta: {
        statementId,
      },
    });
  };
}


export function setSettings(statementId, settings) {
  return (dispatch) => {
    const url = `/statement/${statementId}/set_settings`;
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


export function start(statementId, virtual = false, password = null) {
  return (dispatch) => {
    const url = `/statement/${statementId}/start${virtual ? '_virtual' : ''}`;
    return dispatch({
      type: `POST_STATEMENT_START${virtual ? '_VIRTUAL' : ''}`,
      payload: axios.post(url, password ? { password } : {}),
      meta: { statementId },
    });
  };
}


export function finish(statementId, virtual = false) {
  return (dispatch) => {
    const url = `/statement/${statementId}/finish${virtual ? '_virtual' : ''}`;
    return dispatch({
      type: `POST_STATEMENT_FINISH${virtual ? '_VIRTUAL' : ''}`,
      payload: axios.post(url),
      meta: { statementId },
    }).then(() => dispatch(fetchStatement(statementId)));
  };
}


export function fetchStatementByCourseModuleId(courseModuleId) {
  return (dispatch) => {
    const url = '/statement';
    const params = {
      course_module_id: courseModuleId,
    };
    return dispatch({
      type: 'GET_STATEMENT_BY_COURSE_MODULE_ID',
      payload: axios.get(url, { params }),
    })
  }
}


export function fetchStatementStandings(statementId, groupId) {
  return (dispatch) => {
    const url = `/statement/${statementId}/standings`;
    const params = { group_id: groupId }
    return dispatch({
      type: 'GET_STATEMENT_STANDINGS',
      payload: axios.get(url, { params }),
      meta: { statementId },
    })
  }
}


export function processStandings(statementId, processAttrs = {}) {
  return (dispatch, getState) => {

    const standings = _.get(getState(), `statements[${statementId}].standings`, {});
    const processed = processStandingsData({data: clone(standings), ...processAttrs});

    return dispatch({
      type: 'STATEMENT_PROCESS_STANDINGS',
      payload: processed,
      meta: { statementId },
    })
  }
}
