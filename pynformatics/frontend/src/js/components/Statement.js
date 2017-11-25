import React from 'react';
import { connect } from 'react-redux';
import { Link, withRouter } from 'react-router-dom';

import * as contextActions from '../actions/contextActions';
import * as statementActions from '../actions/statementActions';

import Problem from './Problem';


@connect((state) => {
    return {
        statements: state.statements,
    }
})
@withRouter
export default class Statement extends React.Component {
    componentWillMount() {
        const { statementId } = this.props.match.params;
        this.props.dispatch(contextActions.setContextStatement(statementId));
        this.props.dispatch(statementActions.fetchStatement(statementId));
    }

    componentWillReceiveProps(nextProps) {
        const {statementId} = this.props.match.params;
        const nextStatementId = nextProps.match.params.statementId;
        if (statementId !== nextStatementId)
            this.props.dispatch(contextActions.setContextStatement(statementId));
    }


    render() {
        const {problemRank, statementId} = this.props.match.params;
        const statement = this.props.statements[statementId];

        if (!statement) {
            return <h1>...</h1>
        }

        const problemLis = Object.keys(statement.problems).map(problemRank => {
            return <li key={problemRank}>
                <Link to={`/statement/${statementId}/problem/${problemRank}`}>{problemRank}</Link>
            </li>;
        });

        return <div>
            <h1>{statement.name}</h1>
            <div>
                <ol>{problemLis}</ol>
            </div>
            <div>
                <Problem problemId={statement.problems[problemRank]}/>
            </div>
        </div>;
    }
}
