import React from 'react';
import { withRouter } from 'react-router-dom';


import Problem from '../../components/Problem/Problem';
import MainContentWrapper from '../../components/utility/MainContentWrapper';


export class ProblemPage extends React.Component {
  constructor(props) {
    super(props);

    const { problemId } = props.match.params;

    this.state = {
      problemId: parseInt(problemId),
      collapsed: false,
    };
  }

  render() {
    const { problemId } = this.state;

    return (
      <MainContentWrapper>
        <Problem problemId={problemId} />
      </MainContentWrapper>
    );
  }
}

export default withRouter(ProblemPage);
