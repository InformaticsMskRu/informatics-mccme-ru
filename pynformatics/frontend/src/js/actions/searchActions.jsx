import axios from '../utils/axios';


export function searchUser(query, additionalParams = {}) {
  if (!query) query = '';
  return (dispatch) => {
    const url = '/search/user';
    return dispatch({
      type: 'GET_SEARCH_USER',
      meta: {query},
      payload: axios.get(url, {
        params: {
          query,
          ...additionalParams
        }
      }),
    });
  };
}
