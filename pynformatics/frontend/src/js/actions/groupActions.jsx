import axios from '../utils/axios';


export function fetchGroup(groupId) {
  return (dispatch) => {
    const url = `/group/${groupId}`;

    return dispatch({
      type: 'GET_GROUP',
      payload: axios.get(url),
      meta: { groupId },
    });
  };
}


export function getGroupStudents(groupId) {
  return (dispatch) => {
    const url = `/group/${groupId}/students`;

    return dispatch({
      type: 'GET_GROUP_STUDENTS',
      payload: axios.get(url),
      meta: { groupId },
    });
  };
}

export function getGroupTeachers(groupId) {
  return (dispatch) => {
    const url = `/group/${groupId}/teachers`;

    return dispatch({
      type: 'GET_GROUP_TEACHERS',
      payload: axios.get(url),
      meta: { groupId },
    });
  };
}

export function getGroupInvites(groupId) {
  return (dispatch) => {
    const url = `/group/${groupId}/invite_links`;

    return dispatch({
      type: 'GET_GROUP_INVITES',
      payload: axios.get(url),
      meta: { groupId },
    });
  };
}

export function searchGroup(name, uid) {
  return (dispatch) => {
    const url = '/group';
    const params = { name };

    return dispatch({
      type: 'GET_GROUP_SEARCH',
      payload: axios.get(url, { params }),
      meta: { uid },
    })
  };
}


export function setGroupFilter(group) {
  return (dispatch) => { 
      return dispatch({
        type: 'SET_GROUP_FILTER',
        payload: { group },
      })
  };
}
