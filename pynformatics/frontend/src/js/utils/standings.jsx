import * as _ from 'lodash';

const tempStandingsData = {
  12547: {
    first_name: 'Maxim',
    last_name: 'Grishkin',
    runs: [
      {
        problem_id: 1,
        status: 0,
        score: 100,
        time: '0:11',
      },
      {
        problem_id: 113736,
        status: 1,
        score: 0,
        time: '0:42',
      },
      {
        problem_id: 113736,
        status: 7,
        score: 34,
        time: '0:47',
      },
    ],
  },
  123: {
    first_name: 'Somebody',
    last_name: 'Once',
    runs: [
      {
        problem_id: 1,
        status: 0,
        score: 100,
        time: '0:11',
      },
      {
        problem_id: 2,
        status: 0,
        score: 100,
        time: '0:11',
      },
      {
        problem_id: 3,
        status: 0,
        score: 100,
        time: '0:11',
      },
      {
        problem_id: 4,
        status: 0,
        score: 100,
        time: '0:11',
      },
    ],
  }
}

/**
 * @description Добавляет в data[user_id] поле processed
 * @param {object} data 
 */
export function processStandingsData(data = tempStandingsData) {
  _.forEach(data, (userData, userId) => {
    userData.processed = _.reduce(
      userData.runs, 
      (processed, run) => {
        const { problem_id, score, status, time } = run;
        if (!_.has(processed.problems, `[${problem_id}]`)) {
          processed.problems[problem_id.toString()] = { attempts: 0 };
        }
        const problem = processed.problems[problem_id];

        // Если получен максимальный балл за задачу, игнорировать последующие посылки
        if (problem.score === 100) return processed;

        // В противном случае оценивать задачу по последней посылке
        problem.attempts += 1;
        problem.score = score;
        problem.status = status;
        if (time) problem.time = time;

        if (problem.score === 100) {
          processed.summary.total += 1;
          processed.summary.attempts += problem.attempts - 1;
        }

        return processed;
      },
      {
        summary: {total: 0, attempts: 0},
        problems: {},
      }
    );
  });

  return data;
}
