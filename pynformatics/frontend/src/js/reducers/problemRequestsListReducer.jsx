const initialState = {};


export default function reducer(state = initialState, action) {
    switch (action.type) {
        case 'GET_PROBLEM_REQUESTS_LIST_PENDING':
            return state;
        case 'GET_PROBLEM_REQUESTS_LIST_FULFILLED':
            return {
                ...state,
                ...action.payload.data,
            };
        case 'GET_PROBLEM_REQUESTS_LIST_REJECTED':
            return state;

        default:
            return state;
    }
}