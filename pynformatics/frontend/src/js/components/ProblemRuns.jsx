import * as _ from 'lodash';
import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';

import * as problemActions from '../actions/problemActions';


@connect(state => ({
  problems: state.problems,
}))
export default class ProblemRuns extends React.Component {
  static propTypes = {
    problemId: PropTypes.number.isRequired,
    problems: PropTypes.any,
    dispatch: PropTypes.func,
  };

  constructor(props) {
    super(props);

    this.state = {
      current_run_id: undefined,
      verbose: undefined,
    };

    this.showRunProtocol = this.showRunProtocol.bind(this);
    this.showFullRunProtocol = this.showFullRunProtocol.bind(this);
    this.hideRunProtocol = this.hideRunProtocol.bind(this);
  }

  showRunProtocol(runId) {
    const problem = this.props.problems[this.props.problemId];
    const contestId = problem.runs[runId].contest_id;
    if (!problem.runs[runId].protocol) {
      this.props.dispatch(problemActions.fetchProblemRunProtocol(
        this.props.problemId,
        contestId,
        runId,
      ));
    }
    this.setState({
      ...this.state,
      current_run_id: runId,
      verbose: undefined,
    });
  }

  hideRunProtocol() {
    this.setState({
      ...this.state,
      current_run_id: undefined,
      verbose: undefined,
    });
  }

  showFullRunProtocol(test) {
    this.setState({
      ...this.state,
      verbose: test,
    });
  }

  verboseProtocol() {
    if (!_.get(this, 'state.verbose')) {
      return null;
    }
    const problem = this.props.problems[this.props.problemId];
    const test = problem.runs[this.state.current_run_id].protocol.tests[this.state.verbose];
    return (
      <div>
        <h3>input</h3>
        <div>{test.input}</div>

        <h3>output</h3>
        <div>{test.output}</div>

        <h3>correct</h3>
        <div>{test.correct}</div>
      </div>
    );
  }

  render() {
    const problem = this.props.problems[this.props.problemId];
    if (!problem || !problem.runs) {
      return <div>FETCHING...</div>;
    }

    const {runs, data: {languages}} = problem;

    const runsRows = Object.keys(runs).map(runId => (
      <tr key={runId}>
        <td>{runId}</td>
        <td>{runs[runId].create_time}</td>
        <td>{languages[runs[runId].lang_id]}</td>
        <td>{runs[runId].status}</td>
        <td>{runs[runId].score}</td>
        <td><button onClick={this.showRunProtocol.bind(this, runId)}>протокол</button></td>
      </tr>
    ));

    const runTable = (
      <table>
        <thead>
        <tr>
          <th>ID</th>
          <th>Время</th>
          <th>Язык</th>
          <th>Статус</th>
          <th>Баллы</th>
          <th>Протокол</th>
        </tr>
        </thead>
        <tbody>{runsRows}</tbody>
      </table>
    );

    if (this.state.current_run_id
      && problem.runs[this.state.current_run_id].protocol) {
      const { protocol } = problem.runs[this.state.current_run_id];

      const protocolTestsRows = _.map(protocol.tests, (value, key) => {
        return (
          <tr key={key}>
            <td>{key}</td>
            <td>{value.status}</td>
            <td>{value.time}</td>
            <td>{value.max_memory_used}</td>
            <td>
              <button disabled={!value.input} onClick={this.showFullRunProtocol.bind(this, key)}>
                подробнее
              </button>
            </td>
          </tr>
        );
      });

      const protocolTable = (
        <table>
          <thead>
          <tr>
            <th>Тест</th>
            <th>Статус</th>
            <th>Время</th>
            <th>Память</th>
            <th></th>
          </tr>
          </thead>
          <tbody>{protocolTestsRows}</tbody>
        </table>
      );

      return (
        <div>
          <div>{runTable}</div>
          <div>
            <div><button onClick={this.hideRunProtocol}>close</button></div>
            <div>
              <div>{this.verboseProtocol()}</div>
              <div>{protocolTable}</div>
              <div>
                <h3>compiler output</h3>
                <div>{protocol.compiler_output}</div>
              </div>
            </div>
          </div>
        </div>
      );
    } else {
      return runTable;
    }
  }
}
