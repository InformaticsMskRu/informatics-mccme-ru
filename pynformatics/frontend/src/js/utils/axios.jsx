import axios from 'axios';
import { stringify } from 'query-string';
import camelcaseKeys from 'camelcase-keys';

import store from '../store';


const axiosInstance = axios.create({
  baseURL: '/api_v2',
  withCredentials: true,
});

axiosInstance.interceptors.request.use(config => {
  // const { context } = store.getState();
  // config.params = {
  //   ...config.params,
  //   ...context,
  // };
  config.paramsSerializer = (params) => stringify(params);
  return config;
});

axiosInstance.interceptors.response.use(response => {
  if (response.config.camelcaseKeys) {
    response.data = camelcaseKeys(response.data, {deep: true});
  }
  return response;
})

export default axiosInstance;
