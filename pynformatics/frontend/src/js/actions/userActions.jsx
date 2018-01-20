import axios from '../utils/axios';


export function login(username, password) {
  return (dispatch) => {
    const url = '/auth/login';
    return dispatch({
      type: 'POST_LOGIN',
      payload: axios.post(
        url,
        {
          username,
          password,
        },
      ),
    });
  };
}


export function logout() {
  return (dispatch) => {
    const url = '/auth/logout';
    return dispatch({
      type: 'POST_LOGOUT',
      payload: axios.post(url),
    });
  };
}


export function oauthLogin(provider, code) {
  return (dispatch) => {
    const url = '/auth/oauth_login';
    return dispatch({
      type: 'POST_OAUTH_LOGIN',
      payload: axios.post(
        url,
        {
          provider,
          code,
        },
      ),
    });
  };
}

export function oauthConnect(provider, code) {
  return (dispatch) => {
    const url = '/user/set_oauth_id';
    return dispatch({
      type: 'POST_SET_OAUTH_ID',
      payload: axios.post(
        url,
        {
          provider,
          code,
        },
      ),
    });
  };
}


export function resetPassword(userId) {
  return (dispatch) => {
    const url = '/user/reset_password';
    return dispatch({
      type: 'POST_RESET_PASSWORD',
      meta: {userId},
      payload: axios.post(url, {
        params: {
          id: userId,
        }
      }),
    });
  };
}
