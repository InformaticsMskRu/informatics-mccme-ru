const initialState = {
};


export default function reducer(state=initialState, action) {
    const userId = action.meta ? action.meta.userId : undefined;

    console.log("reducer", action.type, userId, action.payload)

    switch (action.type) {
        case 'GET_USERDATA_FULFILLED':
            return {
                ...state,
                [userId]: {
                    ...action.payload.data,
                    fetched: true,
                },
            };
        default:
            return state;
    }
}