import axios from '../utils/axios';


export function fetchBootstrap() {
  return (dispatch) => {
    const url = '/bootstrap';
    return dispatch({
      type: 'GET_BOOTSTRAP',
      payload: axios.get(url),
    });
  };
}
