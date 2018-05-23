const initialState = {};


export default function reducer(state = initialState, action) {
    switch (action.type) {
        case 'GET_PROBLEM_REQUEST_PENDING':
            return state;
        case 'GET_PROBLEM_REQUEST_FULFILLED':
            const requestId = action.meta ? action.meta.requestId : undefined;
            return {
                ...state,
                [requestId]: {
                    ...action.payload.data,
                }
            };
        case 'GET_PROBLEM_REQUEST_REJECTED':
            return state;

        case 'POST_PROBLEM_REQUEST_APPROVE_PENDING':
            return state;
        case 'POST_PROBLEM_REQUEST_APPROVE_FULFILLED':
            return {
                ...state,
                ...action.payload.data,
            };
        case 'POST_PROBLEM_REQUEST_APPROVE_REJECTED':
            return state;

        case 'POST_PROBLEM_REQUEST_DECLINE_PENDING':
            return state;
        case 'POST_PROBLEM_REQUEST_DECLINE_FULFILLED':
            return {
                ...state,
                ...action.payload.data,
            };
        case 'POST_PROBLEM_REQUEST_DECLINE_REJECTED':
            return state;

        default:
            return state;
    }
}