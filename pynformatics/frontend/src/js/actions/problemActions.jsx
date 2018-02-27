import axios from '../utils/axios';

import { LANGUAGES } from '../constants';


export function fetchProblem(problemId) {
  const url = `/problem/${problemId}`;

  return {
    type: 'GET_PROBLEM',
    payload: axios.get(url),
    meta: {
      problemId,
    },
  };
}


export function fetchProblemRuns(problemId, statementId) {
  return (dispatch) => {
    const url = `/problem/${problemId}/runs`;

    const params = statementId ? {statement_id: statementId} : {};

    return dispatch({
      type: 'GET_PROBLEM_RUNS',
      payload: axios.get(
        url,
        {
          params,
          withCredentials: true,
        },
      ),
      meta: { problemId },
    }).catch(() => {
    });
  };
}


export function submitProblem(problemId, { languageId, file, source }, statementId) {
  return (dispatch) => {
    const url = `/problem/${problemId}/submit_v2`;

    const formData = new FormData;
    formData.append('lang_id', languageId);
    if (file) {
      formData.append('file', file);
    }
    else if (source) {
      const blob = new Blob([source], {type: 'text/plain'});
      formData.append('file', blob, `source${LANGUAGES[languageId].extension}`);
    }
    else {
      alert('nothing to submit');
      return;
    }

    if (typeof statementId !== 'undefined') {
      formData.append('statement_id', statementId);
    }

    return dispatch({
      type: 'PROBLEM_SUBMIT',
      payload: axios.post(
        url,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          withCredentials: true,
        },
      ),
      meta: { problemId },
    }).then(() => dispatch(fetchProblemRuns(problemId, statementId)));
  };
}


export function fetchProblemRunProtocol(problemId, contestId, runId) {
  return (dispatch) => {
    const url = `/protocol/get_v2/${contestId}/${runId}`;

    return dispatch({
      type: 'GET_PROBLEM_RUN_PROTOCOL',
      payload: axios.get(
        url,
        {
          withCredentials: true,
        },
      ),
      meta: { problemId, runId },
    });
  };
}


export function fetchProblemStandings(problemId) {
  return (dispatch) => {
    const url = `/problem/${problemId}/standings`;

    return dispatch({
      type: 'GET_PROBLEM_STANDINGS',
      payload: axios.get(
        url,
        {
          withCredentials: true,
        }
      ),
      meta: { problemId },
    });
  }
}
