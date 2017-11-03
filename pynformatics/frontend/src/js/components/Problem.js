import React from 'react';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';

import * as problemActions from '../actions/problemActions';

import ProblemRuns from './ProblemRuns';
import ProblemSubmitForm from './ProblemSubmitForm';


@connect((state) => {
    return {
        problems: state.problems,
    }
})
@withRouter
export default class Problem extends React.Component {
    constructor(props) {
        super(props);
        this.fetchProblemData(props);
    }

    fetchProblemData(props) {
        const { problemId } = props.match.params;
        this.props.dispatch(problemActions.fetchProblem(problemId));
        this.props.dispatch(problemActions.fetchProblemRuns(problemId));
    }

    componentWillReceiveProps(nextProps) {
        const problemId = this.props.match.params.problemId;
        const nextProblemId = nextProps.match.params.problemId;
        if (problemId !== nextProblemId) {
            this.fetchProblemData(nextProps);
        }
    }

    renderLimits() {
        const { problemId } = this.props.match.params;
        const {data} = this.props.problems[problemId];

        if (!data.show_limits)
            return;

        const { memorylimit, timelimit } = data;

        return <div>
            <div>Ограничение по времени, сек: {timelimit}</div>
            <div>Ограничение по памяти, Мб: {memorylimit / 1024 / 1024}</div>
        </div>;
    }

    render() {
        const { problemId } = this.props.match.params;
        const problem = this.props.problems[problemId];

        if (!problem || (!problem.fetched && problem.fetching)) {
            return <div>
                fetching problem...
            </div>
        }

        const {fetched, data, runs} = problem;

        if (!fetched) {
            return <div>
                some error occured...
            </div>
        }
        return <div class="problem">
            <ProblemSubmitForm problem={problem}/>
            <ProblemRuns problem={problem}/>
            <h1 class="problem-title">Задача {data.id}: {data.name}</h1>
            {this.renderLimits()}
            <div dangerouslySetInnerHTML={{__html: data.content}} />
            <div dangerouslySetInnerHTML={{__html: data.sample_tests_html}}/>
        </div>
    }
}
