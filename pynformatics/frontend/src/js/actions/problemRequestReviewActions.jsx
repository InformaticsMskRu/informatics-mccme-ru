import axios from '../utils/axios';


export function fetchRequest(requestId) {
    const url = `/problem_request/${requestId}`;

    return {
        type: 'GET_PROBLEM_REQUEST',
        payload: axios.get(url),
        meta: { requestId },
    };
}

export function approveRequest(requestId, name, content) {
    const url = '/problem_request_approve';

    return {
        type: 'POST_PROBLEM_REQUEST_APPROVE',
        payload: axios.post(url, {
            problem_request_id: requestId,
            name: name,
            content: content
        }),
    };
}

export function declineRequest(requestId) {
    const url = '/problem_request_decline';

    return {
        type: 'POST_PROBLEM_REQUEST_DECLINE',
        payload: axios.post(url, {
            problem_request_id: requestId
        }),
    };
}
