const initialState = {};

export default function reducer(state = initialState, action) {
    console.log(action);
    if (!action.meta)
        return state;

    const {groupId} = action.meta;

    switch (action.type) {
        case 'GET_GROUP_PENDING':
            return {
                ...state,
                [groupId]: {
                    ...state[groupId],
                    fetching: true,
                }
            };

        case 'GET_GROUP_FULFILLED':
            return {
                ...state,
                [groupId]: {
                    ...state[groupId],
                    data: action.payload.data,
                    fetching: false,
                    fetched: true,
                }
            };

        case 'GET_GROUP_REJECTED':
            return {
                ...state,
                [groupId]: {
                    ...state[groupId],
                    fetching: false,
                    fetched: false,
                }
            };

        default:
            return state;
    }
}
