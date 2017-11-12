import axios from 'axios';

import * as config from 'Config';

import store from '../store';


const axiosInstance = axios.create({
    baseURL: config.apiUrl,
});

axiosInstance.interceptors.request.use(config => {
    const { context } = store.getState();

    switch (config.method) {
        case 'get':
            config.params = {
                ...config.params,
                ...context,
            };
            break;
        case 'post':
            break;
    }
    return config;
});

export default axiosInstance;
