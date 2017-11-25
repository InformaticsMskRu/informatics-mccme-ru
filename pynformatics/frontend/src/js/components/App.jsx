import PropTypes from 'prop-types';
import React from 'react';
import { Switch, Route, withRouter } from 'react-router-dom';
import { connect } from 'react-redux';

import Problem from './Problem';
import Statement from './Statement';
import StatementAdmin from '../pages/StatementAdmin';
import * as bootstrapActions from '../actions/bootstrapActions';


@withRouter
@connect(() => ({}))
export default class App extends React.Component {
  static propTypes = {
    dispatch: PropTypes.func,
  };

  componentDidMount() {
    this.props.dispatch(bootstrapActions.fetchBootstrap());
  }

  render() {
    return (
      <div>
        <div className="main-content">
          <Switch>
            <Route exact path="/statement/:statementId" component={Statement} />
            <Route exact path="/statement/:statementId/problem/:problemRank" component={Statement} />
            <Route
              exact
              path="/problem/:problemId"
              render={props =>
                <Problem {...props} problemId={parseInt(props.match.params.problemId)} />
              }
            />
            <Route exact path="/admin/statement/:statementId" component={StatementAdmin} />
          </Switch>
        </div>
      </div>
    );
  }
}
