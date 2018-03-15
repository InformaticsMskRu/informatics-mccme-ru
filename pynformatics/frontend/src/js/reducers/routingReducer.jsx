const initialState = {};


export default function reducer(state = initialState, action) {
  switch (action.type) {
    case 'SET_REDIRECT_URL':
      return {
        ...state,
        redirectUrl: action.payload.url,
      };

    case 'RESET_REDIRECT_URL':
      const stateCopy = {...state};
      delete stateCopy.redirectUrl;
      return stateCopy;

    default:
      return state;
  }
};
