import React from 'react';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';

import MainContentWrapper from '../components/utility/MainContentWrapper';
import Input from '../components/utility/Input';
import Box from '../components/utility/Box';
import Button from '../components/utility/Button';
import * as statementActions from '../actions/statementActions';


@withRouter
@connect(null)
export default class TempGotoProblem extends React.Component {
  constructor() {
    super();

    this.goto = this.goto.bind(this);
    this.gotoStatement = this.gotoStatement.bind(this);
  }

  goto() {
    if (this.problemId) {
      this.props.history.push(`/problem/${this.problemId}`);
    }
  }

  gotoStatement() {
    if (this.courseModuleId) {
      this.props.dispatch(
        statementActions.fetchStatementByCourseModuleId(this.courseModuleId)
      ).then(({value}) =>
          this.props.history.push(`/contest/${value.data.id}`)
      );
    }
  }

  render() {
    return (
      <MainContentWrapper>
        <Box
          title="Переход к задаче по номеру"
          style={{ height: 'auto', marginBottom: 16 }}
        >
          <div style={{ display: 'flex' }}>
            <Input
              placeholder="номер задачи"
              style={{ width: 200, marginRight: 15 }}
              onChange={e => this.problemId = e.target.value}
              onPressEnter={this.goto}
            />
            <Button
              style={{ display: 'flex' }}
              type="primary"
              onClick={this.goto}
            >
              <i className="material-icons">keyboard_arrow_right</i>
            </Button>
          </div>
        </Box>
        <Box
          title="Переход к контесту по номеру"
          style={{ height: 'auto' }}
        >
          <div style={{ display: 'flex' }}>
            <Input
              placeholder="номер контеста"
              style={{ width: 200, marginRight: 15 }}
              onChange={e => this.courseModuleId = e.target.value}
              onPressEnter={this.gotoStatement}
            />
            <Button
              style={{ display: 'flex' }}
              type="primary"
              onClick={this.gotoStatement}
            >
              <i className="material-icons">keyboard_arrow_right</i>
            </Button>
          </div>
        </Box>
      </MainContentWrapper>
    );
  }
}
