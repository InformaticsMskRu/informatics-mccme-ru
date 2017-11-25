const initialState = {};

export default function reducer(state = initialState, action) {
  switch (action.type) {
    case 'GET_BOOTSTRAP_PENDING':
      return state;
    case 'GET_BOOTSTRAP_FULFILLED':
      return {
        ...state,
        ...action.payload.data.user,
      };
    case 'GET_BOOTSTRAP_REJECTED':
      return state;
    default:
      return state;
  }
}
