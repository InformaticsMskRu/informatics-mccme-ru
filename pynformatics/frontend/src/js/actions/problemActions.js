import axios from 'axios';

import * as config from 'Config';


export function fetchProblem(problemId) {
    const url = `${config.apiUrl}/problem/${problemId}`;

    return {
        type: 'PROBLEM',
        payload: axios.get(url),
    }
}


export function submitProblem(problemId, data) {
    return dispatch => {
        const url = `${config.apiUrl}/problem/${problemId}/submit`;

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
            meta: {
                handleErrors: true,
            }
        }).catch(error => {
            alert(`${code}: ${message}`);
        });
    }
}
