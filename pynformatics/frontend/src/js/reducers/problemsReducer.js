const initialState = {
};

export default function reducer(state=initialState, action) {
    const problemId = action.meta ? action.meta.problemId : undefined;
    switch (action.type) {
        case 'GET_PROBLEM_PENDING':
            return {
                ...state,
                [problemId]: {
                    ...state[problemId],
                    fetching: true,
                }
            };
        case 'GET_PROBLEM_FULFILLED':
            return {
                ...state,
                [problemId]: {
                    ...state[problemId],
                    fetching: false,
                    fetched: true,
                    data: action.payload.data,
                },
            };
        case 'GET_PROBLEM_REJECTED':
            return {
                ...state,
                [problemId]: {
                    ...state[problemId],
                    fetching: false,
                    fetched: false,
                }
            };

        case 'PROBLEM_SUBMIT_PENDING':
            return state;
        case 'PROBLEM_SUBMIT_FULFILLED':
            return state;
        case 'PROBLEM_SUBMIT_REJECTED':
            return state;

        case 'GET_PROBLEM_RUNS_PENDING':
            return {
                ...state,
                [problemId]: {
                    ...state[problemId],
                    fetchingRuns: true,
                },
            };
        case 'GET_PROBLEM_RUNS_FULFILLED':
            return {
                ...state,
                [problemId]: {
                    ...state[problemId],
                    fetchingRuns: false,
                    fetchedRuns: true,
                    runs: action.payload.data,
                },
            };
        case 'GET_PROBLEM_RUNS_REJECTED':
            return {
                ...state,
                [problemId]: {
                    ...state[problemId],
                    fetchingRuns: false,
                    fetchedRuns: false,
                },
            };
    }
    return state;
}