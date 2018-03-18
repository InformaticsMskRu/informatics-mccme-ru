const initialState = {
  bootstrapPending: true,
};


export default function reducer(state = initialState, action) {
  switch (action.type) {
    case 'GET_BOOTSTRAP_PENDING':
      return {
        ...state,
        bootstrapPending: true
      };
    case 'GET_BOOTSTRAP_FULFILLED':
      return {
        ...state,
        ...action.payload.data.user,
        bootstrapPending: false
      };
    case 'GET_BOOTSTRAP_REJECTED':
      return {
        ...state,
        bootstrapPending: false
      };

    case 'POST_LOGIN_PENDING':
      return state;
    case 'POST_LOGIN_FULFILLED':
      return {
        ...state,
        ...action.payload.data,
      };
    case 'POST_LOGIN_REJECTED':
      return state;

    case 'POST_LOGOUT_PENDING':
      return state;
    case 'POST_LOGOUT_FULFILLED':
      return initialState;
    case 'POST_LOGOUT_REJECTED':
      return state;

    case 'POST_OAUTH_LOGIN_PENDING':
      return state;
    case 'POST_OAUTH_LOGIN_FULFILLED':
      return {
        ...state,
        ...action.payload.data,
      };
    case 'POST_OAUTH_LOGIN_REJECTED':
      return state;

    default:
      return state;
  }
}
