const initialState = {
    fetched: false,
    data: null,
};

export default function reducer(state=initialState, action) {

    switch (action.type) {
        case "PROBLEM_PENDING":
            return {...state, fetching: true};
        case "PROBLEM_FULFILLED":
            return {...state, fetching: false, fetched: true, data: action.payload.data};
        case "PROBLEM_REJECTED":
            return {...state, fetching: false, fetched: false};

        case "PROBLEM_SUBMIT_PENDING":
            return {...state, submitting: true};
        case "PROBLEM_SUBMIT_FULFILLED":
            return {...state, submitting: false};
        case "PROBLEM_SUBMIT_REJECTED":
            return {...state, submitting: false};
    }
    return state;
}