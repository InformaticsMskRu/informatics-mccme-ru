const initialState = {
};


export default function reducer(state=initialState, action) {
  const statementId = action.meta ? action.meta.statementId : undefined;

  switch (action.type) {
    case 'GET_STATEMENT_PENDING':
      return state;

    case 'GET_STATEMENT_FULFILLED':
      return {
        ...state,
        [statementId]: {
          ...action.payload.data,
          fetched: true,
        },
      };

    case 'GET_STATEMENT_REJECTED':
      return {
        ...state,
        [statementId]: {
          ...state[statementId],
          fetched: false,
        },
      };

    case 'POST_STATEMENT_SET_SETTINGS':
      return {
        ...state,
        [statementId]: {
          ...action.payload.data,
          fetched: true,
        },
      };

    default:
      return state;
  }
}
