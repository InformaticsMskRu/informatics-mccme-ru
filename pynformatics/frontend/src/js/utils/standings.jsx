import * as _ from 'lodash';

import moment from './moment';


const tempStandingsData = {
  12547: {
    firstname: 'Maxim',
    lastname: 'Grishkin',
    runs: [
      {
        run_id: 1,
        contest_id: 1,
        problem_id: 1,
        status: 0,
        score: 100,
        create_time: '2018-02-10T15:45:52',
      },
      {
        run_id: 2,
        contest_id: 1,
        problem_id: 113736,
        status: 7,
        score: 70,
        create_time: '2018-02-10T18:45:52',
      },
      {
        run_id: 3,
        contest_id: 1,
        problem_id: 113736,
        status: 0,
        score: 100,
        create_time: '2018-02-10T20:00:52',
      },
    ],
  },
}

/**
 * @description Добавляет в data[user_id] поле processed
 * @param {object} data 
 * @param {Date} startDate - начало олимпиады / виртуального контеста
 * @param {Date} endDate - конец олимпиады / виртуального контеста
 * @param {Date} maxDate - игнорирует посылки больше этого времени
 */
export function processStandingsData({data, startDate, endDate, maxDate}) {
  data = tempStandingsData;
  _.forEach(data, (userData, userId) => {
    userData.processed = _.reduce(
      userData.runs, 
      (processed, run) => {
        const { problem_id: problemId, score, status, create_time: createTime } = run;
        const time = new Date(createTime);

        // Если посылка после maxDate, игнорируем
        if (maxDate && time > maxDate) return processed;

        if (!_.has(processed.problems, `[${problemId}]`)) {
          processed.problems[problemId.toString()] = { attempts: 0 };
        }
        const problem = processed.problems[problemId];

        // Если получен максимальный балл за задачу, игнорировать последующие посылки
        if (problem.score === 100) return processed;

        // В противном случае оценивать задачу по последней посылке
        problem.attempts += 1;
        problem.score = score;
        problem.status = status;

        // Время указывается от начала контеста и только в том случае, если посылка отправлена во время
        if (startDate && endDate && time >= startDate && time < endDate) {
          const hours = Math.floor((time - startDate) / 1000 / 60 / 60);
          problem.time = hours + moment.utc(time - startDate).format(':mm');
        }

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
