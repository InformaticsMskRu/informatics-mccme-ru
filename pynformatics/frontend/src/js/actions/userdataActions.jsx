import axios from '../utils/axios';


export function fetchUserdata(userId) {
    const url = `/user/${userId}`;

    console.log("action", url);

    axios.get(url)
        .then(function (response) {
            console.log("axios", response);
        })
        .catch(function (error) {
            console.log("axios", error);
        });

    return {
        type: 'GET_USERDATA',
        payload: axios.get(url),
        meta: {
            userId,
        },
    };
}