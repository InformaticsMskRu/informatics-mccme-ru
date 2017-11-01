import React from 'react';
import { connect } from 'react-redux';

import * as problem from '../actions/problemActions';


export default class ProblemRuns extends React.Component {
    render() {
        const problem = this.props.problem;
        if (!problem || !problem.runs) {
            return <div>FETCHING...</div>;
        }

        const {runs, data: {languages}} = problem;

        const runs_rows = Object.keys(runs).map(
            run_id => <tr key={run_id}>
                <td>{run_id}</td>
                <td>{runs[run_id].create_time}</td>
                <td>{languages[runs[run_id].lang_id]}</td>
                <td>{runs[run_id].status}</td>
                <td>{runs[run_id].score}</td>
            </tr>
        );
        return <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Время</th>
                    <th>Язык</th>
                    <th>Статус</th>
                    <th>Баллы</th>
                </tr>
            </thead>
            <tbody>{runs_rows}</tbody>
        </table>;
    }
}
