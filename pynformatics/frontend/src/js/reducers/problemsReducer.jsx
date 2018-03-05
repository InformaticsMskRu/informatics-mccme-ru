import * as _ from 'lodash';

import { STATUSES } from '../constants';


const initialState = {
};

export default function reducer(state=initialState, action) {
  if (!action.meta)
    return state;
  const {problemId, runId} = action.meta;
  switch (action.type) {
    case 'GET_PROBLEM_PENDING':
      return {
        ...state,
        [problemId]: {
          ...state[problemId],
          fetching: true,
        }
      };
    case 'GET_PROBLEM_FULFILLED':
      return {
        ...state,
        [problemId]: {
          ...state[problemId],
          fetching: false,
          fetched: true,
          data: action.payload.data,
        },
      };
    case 'GET_PROBLEM_REJECTED':
      return {
        ...state,
        [problemId]: {
          ...state[problemId],
          fetching: false,
          fetched: false,
        }
      };

    case 'PROBLEM_SUBMIT_PENDING':
      return state;
    case 'PROBLEM_SUBMIT_FULFILLED':
      return state;
    case 'PROBLEM_SUBMIT_REJECTED':
      return state;

    case 'GET_PROBLEM_RUNS_PENDING':
      return {
        ...state,
        [problemId]: {
          ...state[problemId],
          fetchingRuns: true,
        },
      };
    case 'GET_PROBLEM_RUNS_FULFILLED':
      return {
        ...state,
        [problemId]: {
          ...state[problemId],
          fetchingRuns: false,
          fetchedRuns: true,
          runs: action.payload.data,
        },
      };
    case 'GET_PROBLEM_RUNS_REJECTED':
      return {
        ...state,
        [problemId]: {
          ...state[problemId],
          fetchingRuns: false,
          fetchedRuns: false,
        },
      };


    case 'GET_PROBLEM_RUN_PROTOCOL_PENDING':
      return state;
    case 'GET_PROBLEM_RUN_PROTOCOL_FULFILLED':
      const protocolData = action.payload.data;
      protocolData.tests = _.mapValues(protocolData.tests, testProtocol => ({
        ..._.omit(testProtocol, ['status', 'string_status']),
        status: parseInt(_.findKey(STATUSES, status => status.short === testProtocol.status)),
      }));

      return {
        ...state,
        [problemId]: {
          ...state[problemId],
          runs: {
            ...state[problemId].runs,
            [runId]: {
              ...state[problemId].runs[runId],
              protocol: protocolData,
            }
          }
        }
      };
    case 'GET_PROBLEM_RUN_PROTOCOL_REJECTED':
      return state;
    
    case 'GET_PROBLEM_STANDINGS_FULFILLED':
      return {
        ...state,
        [problemId]: {
          ...state[problemId],
          standings: actions.payload.data,
        }
      };
  }
  return state;
}