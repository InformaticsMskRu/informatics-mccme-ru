import React from 'react';
import { withRouter } from 'react-router-dom';

import MainContentWrapper from '../components/utility/MainContentWrapper';
import Input from '../components/utility/Input';
import Box from '../components/utility/Box';
import Button from '../components/utility/Button';


@withRouter
export default class TempGotoProblem extends React.Component {
  constructor() {
    super();

    this.goto = this.goto.bind(this);
  }

  goto() {
    if (this.problemId) {
      this.props.history.push(`/problem/${this.problemId}`);
    }
  }

  render() {
    return (
      <MainContentWrapper>
        <Box
          title="Введите номер задачи и нажмите на кнопку, чтобы перейти к ней"
          style={{ height: 'auto' }}
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
      </MainContentWrapper>
    );
  }
}
