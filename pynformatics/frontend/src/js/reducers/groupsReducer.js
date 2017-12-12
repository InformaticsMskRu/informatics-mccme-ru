const initialState = {};

export default function reducer(state = initialState, action) {
    console.log(action);
    if (!action.meta)
        return state;

    const {groupId} = action.meta;

    switch (action.type) {
        case 'GET_GROUP_FULFILLED':
            const payload = action.payload;
            console.log(payload);
            return {
                ...state,
                [groupId]: {
                    ...state[groupId],
                    data: payload.data,
                    fetched: true,
                },
            };

        default:
            return state;
    }
}
