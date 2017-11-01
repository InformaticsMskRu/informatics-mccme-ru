import React from 'react';
import { Switch, Route, withRouter } from 'react-router-dom'
import { connect } from 'react-redux';

import * as config from 'Config';
import * as problemActions from '../actions/problemActions';

import Problem from './Problem';
import ProblemRuns from './ProblemRuns';


@withRouter
@connect((store) => {
    return {
    }
})
export default class App extends React.Component {
    handleProblemIdChange(e) {
        if (e.charCode == 13) {
            const problemId = e.target.value;
            this.props.history.push(`/x/${problemId}`);
            this.props.dispatch(problemActions.fetchProblem(problemId));
        }
    }

    render() {
        return <div>
            {/*<div>*/}
                {/*<span>Номер задачи: </span>*/}
                {/*<input name="problemId" onKeyPress={this.handleProblemIdChange.bind(this)}/>*/}
            {/*</div>*/}
            <div class="main-content">
                <Switch>
                    <Route exact path="/x/:problemId/" component={Problem} />
                    <Route exact path="/x/:problemId/runs/" component={ProblemRuns} />
                </Switch>
            </div>
        </div>
    }
}