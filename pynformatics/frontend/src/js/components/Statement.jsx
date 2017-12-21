import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import { Link, withRouter } from 'react-router-dom';
import * as _ from 'lodash';

import * as contextActions from '../actions/contextActions';
import * as statementActions from '../actions/statementActions';

import Problem from './Problem';


const STATEMENT_STATUS = {
  NOT_STARTED: 0,
  ACTIVE: 1,
  FINISHED: 2,
};

const PARTICIPANT_STATUS = {
  NOT_STARTED: 0,
  ACTIVE: 1,
  FINISHED: 2,
};


function getStatus(statement) {
  if (!statement.olympiad && !statement.virtual_olympiad) {
    return {};
  }

  const nowDate = new Date();

  const {
    participant,
    timestart: timeStart,
    timestop: timeStop,
  } = statement;
  const statementStartDate = new Date(timeStart * 1000);
  const statementStopDate = new Date(timeStop * 1000);

  let statementStatus;
  if (nowDate < statementStartDate) {
    statementStatus = STATEMENT_STATUS.NOT_STARTED;
  } else if (nowDate >= statementStartDate && nowDate < statementStopDate) {
    statementStatus = STATEMENT_STATUS.ACTIVE;
  } else {
    statementStatus = STATEMENT_STATUS.FINISHED;
  }

  let participantStatus;
  if (!participant) {
    participantStatus = STATEMENT_STATUS.NOT_STARTED;
  } else {
    const { start, duration } = participant;
    const participantStopDate = new Date((start + duration) * 1000);
    if (participantStopDate > nowDate) {
      participantStatus = PARTICIPANT_STATUS.ACTIVE;
    } else {
      participantStatus = PARTICIPANT_STATUS.FINISHED;
    }
  }
  return {
    participantStatus,
    statementStatus,
  };
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
    this.start = this.start.bind(this);
    this.finish = this.finish.bind(this);
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

  getStatement() {
    const { statementId } = this.props.match.params;
    return this.props.statements[statementId];
  }

  start() {
    const statement = this.getStatement();
    this.props.dispatch(statementActions.start(statement.id, statement.virtual_olympiad));
  }

  finish() {
    const statement = this.getStatement();
    this.props.dispatch(statementActions.finish(statement.id, statement.virtual_olympiad));
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
              const { participantStatus, statementStatus } = getStatus(statement);
              if (statementStatus === STATEMENT_STATUS.NOT_STARTED) {
                return <span> (соревнование не началось)</span>;
              } else if (statementStatus === STATEMENT_STATUS.FINISHED) {
                return <span> (соревнование завершено)</span>;
              } else {
                switch (participantStatus) {
                  case PARTICIPANT_STATUS.NOT_STARTED:
                    return <button onClick={this.start} disabled={activeStatementId}>start</button>;
                  case PARTICIPANT_STATUS.ACTIVE:
                    return <button onClick={this.finish}>finish</button>;
                  case PARTICIPANT_STATUS.FINISHED:
                    return <span> (finished)</span>;
                }
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
