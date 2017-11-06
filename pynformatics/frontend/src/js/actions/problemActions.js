import axios from 'axios';

import * as config from 'Config';
import { LANGUAGES } from '../constants';


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
        if (data.file)
            formData.append('file', data.file);
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
