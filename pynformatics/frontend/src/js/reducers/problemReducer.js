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
            return {...state, fetching: false, fetched: false, error: action.payload};

        case "PROBLEM_SUBMIT_PENDING":
            return state;
        case "PROBLEM_SUBMIT_FULFILLED":
            console.log('haha');
            console.log(action);
            return state;
        case "PROBLEM_SUBMIT_REJECTED":
            return state;
    }
    return state;
}