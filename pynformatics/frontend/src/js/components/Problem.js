import React from 'react';
import {connect} from 'react-redux';

import * as problem from '../actions/problemActions';

import ProblemSubmitForm from './ProblemSubmitForm';


@connect((state) => {
    return {
        problem: state.problem,
    }
})
export default class Problem extends React.Component {
    componentWillMount() {
        this.props.dispatch(problem.fetchProblem(this.props.match.params.problemId));
    }

    renderLimits() {
        const {data} = this.props.problem;

        if (!data.show_limits)
            return;

        const {memorylimit, timelimit} = data;

        return <div>
            <div>Ограничение по времени, сек: {timelimit}</div>
            <div>Ограничение по памяти, Мб: {memorylimit / 1024 / 1024}</div>
        </div>;
    }

    render() {
        const {fetching, fetched, data} = this.props.problem;

        if (fetching) {
            return <div>
                fetching problem...
            </div>
        }
        else if (!fetched) {
            return <div>
                some error occured...
            </div>
        }
        return <div class="problem">
            <ProblemSubmitForm problem={data}/>
            <h1 class="problem-title">Задача {data.id}: {data.name}</h1>
            {this.renderLimits()}
            <div dangerouslySetInnerHTML={{__html: data.content}} />
            <div dangerouslySetInnerHTML={{__html: data.sample_tests_html}}/>
        </div>
    }
}
