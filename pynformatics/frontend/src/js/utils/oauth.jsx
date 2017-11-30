import * as _ from 'lodash';


export const OAUTH_CONFIG = {
  vk: {
    url: 'https://oauth.vk.com/authorize',
    params: {
      client_id: 6279574,
      display: 'page',
      redirect_uri: 'https://informatics.msk.ru/frontend/login',
      response_type: 'code',
      scope: 0,
      v: 5.69,
    },
  },
  google: {
    url: 'https://accounts.google.com/o/oauth2/v2/auth',
    params: {
      client_id: '629729803861-vilqpepmi33rdd5jtguq9cv0aifseera.apps.googleusercontent.com',
      redirect_uri: 'https://informatics.msk.ru/frontend/login',
      response_type: 'code',
      scope: 'profile',
    },
  },
};

export function getRedirectUrl(provider, state) {
  const config = OAUTH_CONFIG[provider];
  const stateParams = {
    ...config.params,
    state: JSON.stringify({
      ...state,
      provider,
    }),
  };
  const params = _.join(_.map(stateParams, (value, key) => `${key}=${value}`), '&');
  return `${config.url}?${params}`;
}
