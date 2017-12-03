const initialState = {
};


export default function reducer(state=initialState, action) {
    switch (action.type) {
        case 'SET_CONTEXT_STATEMENT':
            return {
                ...state,
                statement_id: action.payload,
            }
    }

    return state;
}
