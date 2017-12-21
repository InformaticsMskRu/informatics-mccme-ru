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


export function fetchProblemRuns(problemId) {
  return (dispatch) => {
    const url = `/problem/${problemId}/runs`;

    dispatch({
      type: 'GET_PROBLEM_RUNS',
      payload: axios.get(
        url,
        {
          withCredentials: true,
        },
      ),
      meta: { problemId },
    }).catch(() => {
    });
  };
}


export function submitProblem(problemId, data) {
  return (dispatch) => {
    const url = `/problem/${problemId}/submit_v2`;

    const formData = new FormData;
    formData.append('lang_id', data.langId);
    if (data.file) {
      formData.append('file', data.file);
    }
    else if (data.source) {
      const blob = new Blob([data.source], {type: 'text/plain'});
      formData.append('file', blob, `source${LANGUAGES[data.langId].extension}`);
    }
    else {
      alert('nothing to submit');
      return;
    }

    dispatch({
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
    }).then(() => dispatch(fetchProblemRuns(problemId))).catch(() => {
    });
  };
}


export function fetchProblemRunProtocol(problemId, contestId, runId) {
  return (dispatch) => {
    const url = `/protocol/get/${contestId}/${runId}`;

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
