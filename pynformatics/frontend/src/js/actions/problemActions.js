import axios from '../utils/axios';


export function fetchProblem(problemId) {
    const url = `/problem/${problemId}`;

    return {
        type: 'GET_PROBLEM',
        payload: axios.get(url),
        meta: {
            problemId,
        }
    }
}


export function submitProblem(problemId, data) {
    return dispatch => {
        const url = `/problem/${problemId}/submit_v2`;

        let formData = new FormData;
        formData.append('lang_id', data.langId);
        formData.append('file', data.file);

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
                }
            ),
            meta: { problemId }
        }).then(response => dispatch(fetchProblemRuns(problemId))).catch(error => {
            // alert(`${code}: ${message}`);
        });
    }
}


export function fetchProblemRuns(problemId) {
    return dispatch => {
        const url = `/problem/${problemId}/runs`;

        dispatch({
            type: 'GET_PROBLEM_RUNS',
            payload: axios.get(
                url,
                {
                    withCredentials: true,
                }
            ),
            meta: { problemId }
        }).catch(error => {
            // alert(`${code}: ${message}`);
        });
    }
}


export function fetchProblemRunProtocol(problemId, contestId, runId) {
    return dispatch => {
        const url = `${config.apiUrl}/protocol/get/${contestId}/${runId}`;

        dispatch({
            type: 'GET_PROBLEM_RUN_PROTOCOL',
            payload: axios.get(
                url,
                {
                    withCredentials: true,
                }
            ),
            meta: { problemId, runId },
        })
    }
}
