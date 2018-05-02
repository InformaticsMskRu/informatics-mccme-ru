import axios from '../utils/axios';


export function fetchRequestsList() {
    const url = '/problem_requests';

    return {
        type: 'GET_PROBLEM_REQUESTS_LIST',
        payload: axios.get(url),
    };
}