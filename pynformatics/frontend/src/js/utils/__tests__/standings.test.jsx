import clone from 'clone';

import { processStandingsData } from '../standings';


const userId = 12547;
const standingsData = {
  [userId]: {
    first_name: 'Maxim',
    last_name: 'Grishkin',
    runs: [],
  },
};


describe('Processes standings data', () => {
  let data;

  beforeEach(() => {
    data = clone(standingsData);
  });

  it('single problem, 1 OK submit', () => {
    data[userId].runs = [
      {problem_id: 1, status: 0, score: 100}
    ];
    processStandingsData(data);

    expect(data[userId].processed).toEqual({
      summary: {total: 1, attempts: 0},
      problems: {
        1: { attempts: 1, score: 100, status: 0 }
      }
    });
  });

  it('single problem, 1 PT submit', () => {
    data[userId].runs = [
      {problem_id: 1, status: 7, score: 37, time: '1:00'}
    ];
    processStandingsData(data);

    expect(data[userId].processed).toEqual({
      summary: {total: 0, attempts: 0},
      problems: {
        1: { attempts: 1, score: 37, status: 7, time: '1:00' }
      }
    });
  })

  it('single problem, many submits, PT final', () => {
    data[userId].runs = [
      {problem_id: 1, status: 7, score: 37, time: '1'},
      {problem_id: 1, status: 7, score: 38, time: '2'},
      {problem_id: 1, status: 7, score: 56, time: '3'},
      {problem_id: 1, status: 7, score: 99, time: '4'},
    ];
    processStandingsData(data);

    expect(data[userId].processed).toEqual({
      summary: {total: 0, attempts: 0},
      problems: {
        1: { attempts: 4, score: 99, status: 7, time: '4' }
      }
    });
  })

  it('single problem, many submits, OK final', () => {
    data[userId].runs = [
      {problem_id: 1, status: 7, score: 37, time: '1'},
      {problem_id: 1, status: 7, score: 38, time: '2'},
      {problem_id: 1, status: 7, score: 56, time: '3'},
      {problem_id: 1, status: 0, score: 100, time: '4'},
    ];
    processStandingsData(data);

    expect(data[userId].processed).toEqual({
      summary: {total: 1, attempts: 3},
      problems: {
        1: { attempts: 4, score: 100, status: 0, time: '4' }
      }
    });
  })

  it('single problem, many submits, ignores after OK', () => {
    data[userId].runs = [
      {problem_id: 1, status: 0, score: 100, time: '1'},
      {problem_id: 1, status: 7, score: 56, time: '2'},
      {problem_id: 1, status: 7, score: 56, time: '3'},
    ];
    processStandingsData(data);

    expect(data[userId].processed).toEqual({
      summary: {total: 1, attempts: 0},
      problems: {
        1: { attempts: 1, score: 100, status: 0, time: '1' }
      }
    });
  })

  it('single problem, works without time', () => {
    data[userId].runs = [
      {problem_id: 1, status: 0, score: 100},
      {problem_id: 1, status: 7, score: 56},
      {problem_id: 1, status: 7, score: 56},
    ];
    processStandingsData(data);

    expect(data[userId].processed).toEqual({
      summary: {total: 1, attempts: 0},
      problems: {
        1: { attempts: 1, score: 100, status: 0}
      }
    });
  })

  it('multiple problems', () => {
    data[userId].runs = [
      {problem_id: 1, status: 0, score: 100, time: '1'},
      {problem_id: 2, status: 0, score: 100, time: '2'},
      {problem_id: 3, status: 0, score: 100, time: '3'},
    ];
    processStandingsData(data);

    expect(data[userId].processed).toEqual({
      summary: { total: 3, attempts: 0 },
      problems: {
        1: {attempts: 1, score: 100, status: 0, time: '1'},
        2: {attempts: 1, score: 100, status: 0, time: '2'},
        3: {attempts: 1, score: 100, status: 0, time: '3'},
      }
    });
  })

  it('multiple users', () => {
    const userId2 = 123;
    data[userId].runs = [
      {problem_id: 1, score: 100, status: 0, time: '1'},
      {problem_id: 2, score: 100, status: 0, time: '2'},
    ];
    data[userId2] = {
      first_name: 'Somebody',
      last_name: 'Once told me',
      runs: [
        {problem_id: 1, score: 78, status: 7, time: '3'},
        {problem_id: 1, score: 100, status: 0, time: '4'},
        {problem_id: 2, score: 78, status: 7, time: '5'},
      ]
    }
    processStandingsData(data);

    expect(data[userId].processed).toEqual({
      summary: { total: 2, attempts: 0 },
      problems: {
        1: { attempts: 1, score: 100, status: 0, time: '1' },
        2: { attempts: 1, score: 100, status: 0, time: '2' },
      }
    });
    expect(data[userId2].processed).toEqual({
      summary: { total: 1, attempts: 1 },
      problems: {
        1: { attempts: 2, score: 100, status: 0, time: '4' },
        2: { attempts: 1, score: 78, status: 7, time: '5' },
      }
    });
  })
});
