import React from 'react';
import PropTypes from 'prop-types';

import Runs from '../Runs/Runs';


export default class SubmissionsPane extends React.Component {
  static propTypes = {
    problemId: PropTypes.number.isRequired,
    runs: PropTypes.object.isRequired,
  };

  render() {
    return (
      <Runs
        problemId={this.props.problemId}
        runs={this.props.runs}
        showRows={15}
        showUserInfo={true}
      />
    );
  };
}
