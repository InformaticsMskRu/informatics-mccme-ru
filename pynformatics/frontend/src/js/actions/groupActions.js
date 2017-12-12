import axios from '../utils/axios';

export function fetchGroup(groupId) {
    const url = `/group/${groupId}`;

    return {
        type: 'GET_GROUP',
        payload: axios.get(url),
        meta: {
            groupId,
        },
    };
}
