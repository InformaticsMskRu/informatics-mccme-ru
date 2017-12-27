const initialState = {
  data: [],
  pages_total: 0,
  page: 0
};


export default function reducer(state=initialState, action) {
  switch (action.type) {
    case 'GET_SEARCH_USER_PENDING':
      return {
        ...state,
        query: action.meta.query,
        type: 'user',
        fetched: false,
      };
    case 'GET_SEARCH_USER_FULFILLED':
      return {
        ...state,
        query: action.meta.query,
        type: 'user',
        ...action.payload.data,
        fetched: true,
        error: false
      };
    case 'GET_SEARCH_USER_REJECTED':
      return {
        ...state,
        query: action.meta.query,
        type: 'user',
        data: [],
        fetched: true,
        error: true,
        errorData: action.payload.response.data,
      };
  }
  return state;
}
