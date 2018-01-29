import axios from 'axios';

import store from '../store';


const axiosInstance = axios.create({
    baseURL: '/api_v2',
    withCredentials: true,
});

axiosInstance.interceptors.request.use(config => {
    const { context } = store.getState();
    config.params = {
        ...config.params,
        ...context,
    };
    return config;
});

export default axiosInstance;
