import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import { Link, withRouter } from 'react-router-dom';
import * as _ from 'lodash';

import * as contextActions from '../actions/contextActions';
import * as statementActions from '../actions/statementActions';

import Problem from './Problem';


const VIRTUAL_STATEMENT_STATUS = {
  NOT_STARTED: 0,
  ACTIVE: 1,
  FINISHED: 2,
};


function getStatementStatus(statement) {
  if (!statement.virtual_olympiad) {
    return undefined;
  }
  const { virtual_participant: virtualParticipant } = statement;
  if (!virtualParticipant) {
    return VIRTUAL_STATEMENT_STATUS.NOT_STARTED;
  }
  const { start, duration } = virtualParticipant;
  const finishDate = new Date((start + (duration * 60)) * 1000);
  return finishDate > new Date() ?
    VIRTUAL_STATEMENT_STATUS.ACTIVE : VIRTUAL_STATEMENT_STATUS.FINISHED;
}


@withRouter
@connect(state => ({
  statements: state.statements,
  user: state.user,
}))
export default class Statement extends React.Component {
  static propTypes = {
    statements: PropTypes.any,
    user: PropTypes.any,
    match: PropTypes.any,
    history: PropTypes.any,
    dispatch: PropTypes.func,
  };

  constructor(props) {
    super(props);
    this.startVirtual = this.startVirtual.bind(this);
    this.finishVirtual = this.finishVirtual.bind(this);
  }

  componentWillMount() {
    const { statementId } = this.props.match.params;
    this.props.dispatch(contextActions.setContextStatement(statementId));
    this.props.dispatch(statementActions.fetchStatement(statementId));
  }

  componentWillReceiveProps(nextProps) {
    const { statementId } = this.props.match.params;
    const { statementId: nextStatementId, problemRank: nextProblemRank } = nextProps.match.params;
    const { statements: nextStatements } = nextProps;

    if (statementId !== nextStatementId) {
      this.props.dispatch(contextActions.setContextStatement(statementId));
    }

    if (!nextProblemRank && _.has(nextStatements, `[${nextStatementId}].problems`)) {
      const newProblemRank = _.min(_.keys(nextStatements[nextStatementId].problems));
      nextProps.history.replace(`/statement/${nextStatementId}/problem/${newProblemRank}`);
    }
  }

  startVirtual() {
    const { statementId } = this.props.match.params;
    this.props.dispatch(statementActions.startVirtual(statementId));
  }

  finishVirtual() {
    const { statementId } = this.props.match.params;
    this.props.dispatch(statementActions.finishVirtual(statementId));
  }

  render() {
    const { statementId, problemRank } = this.props.match.params;
    const statement = this.props.statements[statementId];
    const { user } = this.props;

    if (!statement) {
      return <h1>fetching statement...</h1>;
    }

    const problemLis = _.keys(statement.problems).map((problemRank) => {
      return (
        <li key={problemRank}>
          <Link to={`/statement/${statementId}/problem/${problemRank}`}>{problemRank}</Link>
        </li>
      );
    });

    const problemId = _.get(statement, `problems.[${problemRank}]`);

    return (
      <div>
        <h1>
          <a href={`http://informatics.msk.ru/mod/statements/view.php?id=${statement.course_module_id}#1`}>#</a>
          {statement.name}
          {
            (() => {
              const activeStatementId = _.get(user, 'active_virtual.statement_id');
              switch (getStatementStatus(statement)) {
                case VIRTUAL_STATEMENT_STATUS.NOT_STARTED:
                  return (
                    <button onClick={this.startVirtual} disabled={activeStatementId}>start</button>
                  );
                case VIRTUAL_STATEMENT_STATUS.ACTIVE:
                  return <button onClick={this.finishVirtual}>finish</button>;
                case VIRTUAL_STATEMENT_STATUS.FINISHED:
                  return <span> (finished)</span>;
                default:
              }
            })()
          }
        </h1>
        <div>{problemLis}</div>
        <div>{problemId && <Problem problemId={problemId} />}</div>
      </div>
    );
  }
}
