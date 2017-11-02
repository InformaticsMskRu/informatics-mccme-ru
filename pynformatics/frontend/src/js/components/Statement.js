import React from 'react';
import { connect } from 'react-redux';
import { Switch, Route, Redirect, Link, withRouter } from 'react-router-dom';

import * as statementActions from '../actions/statementActions';

import Problem from './Problem';


@connect((state) => {
    return {
        statements: state.statements,
    }
})
@withRouter
export default class Statement extends React.Component {
    constructor(props) {
        super();
        console.log(props);
        this.statementId = props.match.params.statementId;
    }

    componentWillMount() {
        this.props.dispatch(statementActions.fetchStatement(this.statementId));
    }

    render() {
        const { match: {path, url} } = this.props;
        const statement = this.props.statements[this.statementId];
        if (!statement) {
            return <h1>...</h1>
        }
        const problemLis = Object.keys(statement.problems).map(problemRank => {
            const problemId = statement.problems[problemRank];
            return <li key={problemId}>
                <Link to={`${url}/problem/${problemId}`}>{problemId}</Link>
            </li>;
        });
        console.log(this.props);
        return <div>
            <h1>{statement.name}</h1>
            <div>
                <ol>{problemLis}</ol>
            </div>
            <div>
                <Switch>
                    <Route exact path={`${path}/problem/:problemId`} component={Problem}/>
                </Switch>
            </div>
        </div>;
    }
}
