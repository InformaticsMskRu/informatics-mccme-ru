import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import { connect } from 'react-redux';
import { palette } from 'styled-theme';
import * as _ from 'lodash';

import Box from '../../components/utility/Box';
import GroupFilter from '../../components/GroupFilter/GroupFilter';
import Header from '../../components/utility/Header';
import Runs from '../Runs/Runs';
import Sample from './Sample';
import StandingsPane from './StandingsPane';
import SubmissionsPane from './SubmissionsPane';
import SubmitForm from './SubmitForm';
import Tabs, { TabPane } from '../../components/utility/Tabs';
import * as problemActions from '../../actions/problemActions';


const ProblemWrapper = styled.div`
  > div {
    height: auto;
  }

  .problemTitle {
    display: flex;
    flex-flow: row nowrap;
    margin: 10px 0 34px 0;
    font-size: 18px;
    color: ${palette('secondary', 0)};
    width: 100%;
    text-align: center;
    
    i {
      cursor: pointer;
      display: none;
    }
    span { margin: auto; }
  }

  .problemLimits {
    display: flex;
    flex-flow: row wrap;
    justify-content: space-around;
    padding: 10px;

    background: #f8f8f8;
    color: ${palette('other', 13)};
    border-radius: 4px;

    @media (max-width: 575px) {
      flex-flow: column nowrap;
    }
  }
    
  .problemStatement {
    text-align: left;
    color: ${palette('other', 7)};
    
    .legend {
      p { margin-bottom: 34px; }  
    }
    
    div { 
      margin-bottom: 34px;
    
      .section-title {
        width: 100%;
        margin-bottom: 20px;
        
        display: flex;
        align-items: center;
        
        font-size: 19px;
        font-weight: 500;
        color: ${palette('secondary', 2)};
        white-space: nowrap;
        
        &:before {
          content: '';
          width: 5px;
          height: 40px;
          background: ${palette('secondary', 3)};
          display: flex;
          margin-right: 15px;
        }
        
        &:after {
          content: '';
          width: 100%;
          height: 1px;
          background: ${palette('secondary', 3)};
          display: flex;
          margin-left: 15px;
        }
      }
    }
  }
  
  .problemSamples {
    > *:not(:last-child) { margin-bottom: 34px; }
  }
  
  .tabStatement > * { margin-bottom: 30px; }
`;


export class Problem extends React.Component {
  static contextTypes = {
    statementId: PropTypes.number,
  };

  static propTypes = {
    problemId: PropTypes.number.isRequired,
  };

  constructor(props, context) {
    super(props, context);

    this.problemId = this.props.problemId;

    this.fetchProblemData = this.fetchProblemData.bind(this);
    this.fetchProblemData(props.problemId);
  }

  componentWillReceiveProps(nextProps) {
    const { problemId } = this.props;
    const { problemId: nextProblemId } = nextProps;

    if (problemId !== nextProblemId) {
      this.fetchProblemData(nextProblemId);
    }
  }

  componentDidUpdate() {
    this.problemId = this.props.problemId;
  }

  fetchProblemData(problemId) {
    this.props.dispatch(problemActions.fetchProblem(problemId));
    this.props.dispatch(problemActions.fetchProblemRuns(problemId, this.context.statementId));
  }

  render() {
    const { problemId } = this.props;
    const {
      name: problemTitle,
      content: problemStatement,
      sample_tests_json: problemSamples,
      timelimit: problemTimeLimit,
      memorylimit: problemMemoryLimit,
      show_limits: problemShowLimits,
    } = _.get(this.props.problems, `[${problemId}].data`, {});
    const problemRuns = _.get(this.props.problems[problemId], 'runs', {});
    const userProblemRuns = _.pickBy(problemRuns, (value) => typeof value.user === 'undefined');

    const additionalTabsProps = (problemId !== this.problemId)
      ? { activeKey: 'statement' }
      : {};

    return (
      <ProblemWrapper>
        <Box>
          <div className="problemTitle">
            <span>Задача №{problemId}. {problemTitle}</span>
          </div>

          <Tabs
            defaultActiveKey="statement"
            style={{ textAlign: 'center' }}
            {...additionalTabsProps}
          >
            <TabPane className="tabStatement" tab="Условие" key="statement">
              {
                problemShowLimits
                ? (
                  <div className="problemLimits">
                    <div>Ограничение по времени, сек: {problemTimeLimit}</div>
                    <div>Ограничение по памяти, мегабайт: {problemMemoryLimit / 1024 / 1024}</div>
                  </div>
                ) : null
              }
              <div className="problemStatement" dangerouslySetInnerHTML={{ __html: problemStatement }} />
              <Header style={{ marginBottom: 30 }}>Примеры</Header>
              <div className="problemSamples">
                { _.map(problemSamples, ({input, correct}, id) => <Sample key={id} input={input} correct={correct}/>) }
              </div>
              <SubmitForm problemId={problemId} />
              <Runs problemId={problemId} runs={userProblemRuns} />
            </TabPane>
            <TabPane tab="Результаты" key="standings">
              <StandingsPane problemId={problemId} />
            </TabPane>
            <TabPane tab="Посылки" key="runs">
              <SubmissionsPane problemId={problemId} runs={problemRuns} />
            </TabPane>
            <TabPane tab="Решение" key="solution" disabled />
            <TabPane tab="Темы и источники" key="sources" disabled />
          </Tabs>
        </Box>
      </ProblemWrapper>
    );
  }
}

export default connect(state => ({
  problems: state.problems,
}))(Problem);
