import React from 'react';
import { connect } from 'react-redux';
import * as _ from 'lodash';

import * as problemActions from '../actions/problemActions';


@connect((state) => {
    return {
        problems: state.problems,
    }
})
export default class ProblemRuns extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            current_run_id: undefined,
        };
    }

    showRunProtocol(runId) {
        const problem = this.props.problems[this.props.problemId];
        const contestId = problem.runs[runId].contest_id;
        if (!problem.runs[runId].protocol)
            this.props.dispatch(problemActions.fetchProblemRunProtocol(this.props.problemId, contestId, runId));
        this.setState({
            ...this.state,
            current_run_id: runId,
        })
    }

    hideRunProtocol() {
        this.setState({
            ...this.state,
            current_run_id: undefined,
        })
    }

    render() {
        const problem = this.props.problems[this.props.problemId];
        if (!problem || !problem.runs) {
            return <div>FETCHING...</div>;
        }

        const {runs, data: {languages}} = problem;

        const runsRows = Object.keys(runs).map(
            runId => <tr key={runId}>
                <td>{runId}</td>
                <td>{runs[runId].create_time}</td>
                <td>{languages[runs[runId].lang_id]}</td>
                <td>{runs[runId].status}</td>
                <td>{runs[runId].score}</td>
                <td><button onClick={this.showRunProtocol.bind(this, runId)}>протокол</button></td>
            </tr>
        );

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
                return <tr key={key}>
                    <td>{key}</td>
                    <td>{value.status}</td>
                    <td>{value.time}</td>
                    <td>{value.max_memory_used}</td>
                </tr>
            });

            const protocolTable = <table>
                <thead>
                    <tr>
                        <th>Тест</th>
                        <th>Статус</th>
                        <th>Время</th>
                        <th>Память</th>
                    </tr>
                </thead>
                <tbody>{protocolTestsRows}</tbody>
            </table>;

            return <div>
                <div>{runTable}</div>
                <div>
                    <div><button onClick={this.hideRunProtocol.bind(this)}>close</button></div>
                    <div>{protocolTable}</div>
                </div>
            </div>;
        }
        else {
            return runTable;
        }
    }
}
