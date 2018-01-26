import { compose } from 'redux';
import { connect } from 'react-redux';
import React from 'react';
import { Layout } from 'antd';
import { palette } from 'styled-theme';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import { withRouter } from 'react-router-dom';


import Box from '../../components/utility/Box';
import Menu from './Menu';
import Tabs, { TabPane } from '../../components/utility/Tabs';
import { ToggleDrawerIcon } from '../../components/Icon';
import SubmitForm from './SubmitForm';
import Runs from './Runs';
import * as problemActions from '../../actions/problemActions';


const { Sider } = Layout;

const ProblemPageWrapper = styled.div`
  max-width: 1280px;
  margin: auto;
  padding: 80px 70px 0;
  
  .problemSider {
    .ant-layout-sider {
      background: none;
    }
  }
  
  .problemContent {
    width: 100%;
    overflow-x: auto;
    margin-left: 30px;
    > div {
      height: auto;
    }
    
    .toggleDrawer {
      display: none;
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
      text-align: left;
    }
  }
  
  @media (max-width: 1279px) {  
    .problemSider { 
      position: absolute;
      z-index: 100; 
    }
    
    .problemContent { 
      margin-left: 0;
      
      .problemTitle {
        i { display: block; }
      } 
    }
  }
  
  @media (max-width: 767px) {
    padding: 80px 0 0;
  }
  
  .tabStatement > * { margin-bottom: 30px; }
  
`;

export class ProblemPage extends React.Component {
  static propTypes = {
    match: PropTypes.object.isRequired,
    problems: PropTypes.object.isRequired,
  };

  constructor(props) {
    super(props);

    const { problemId } = props.match.params;

    this.state = {
      problemId,
      collapsed: false,
    };

    this.fetchProblemData = this.fetchProblemData.bind(this);
    this.toggleCollapse = this.toggleCollapse.bind(this);

    this.fetchProblemData(problemId);
  }

  fetchProblemData() {
    const { problemId } = this.state;
    this.props.dispatch(problemActions.fetchProblem(problemId));
    this.props.dispatch(problemActions.fetchProblemRuns(problemId));
  }

  toggleCollapse() {
    this.setState({
      ...this.state,
      collapsed: !this.state.collapsed,
    });
  }

  render() {
    const { collapsed, problemId } = this.state;
    const { windowWidth } = this.props;

    const problemData = _.get(this.props.problems[problemId], 'data', {});
    const {
      name: problemTitle,
      content: problemStatement,
      sample_tests_html: problemSamples,
    } = problemData;
    const problemRuns = _.get(this.props.problems[problemId], 'runs', {});

    return (
      <ProblemPageWrapper>
        <Layout style={{ position: 'relative' }}>
          <div className="problemSider">
            <Sider
              width={320}
              collapsible={true}
              collapsed={collapsed}
              trigger={null}
              collapsedWidth={windowWidth < 1280 ? 0 : 46}
            >
              <Box
                style={collapsed
                  ? {
                    paddingLeft: 4,
                    paddingRight: 4,
                  }
                  : {}}
              >
                <Menu collapsed={collapsed} onCollapse={this.toggleCollapse}/>
              </Box>
            </Sider>
          </div>
          <div className="problemContent">
          <Box>
            <div className="problemTitle">
              <ToggleDrawerIcon onClick={this.toggleCollapse} />
              <span>Задача №{problemId}. {problemTitle}</span>
            </div>

            <Tabs defaultActiveKey="statement" style={{ textAlign: 'center' }}>
              <TabPane className="tabStatement" tab="Условие" key="statement">
                <div className="problemStatement" dangerouslySetInnerHTML={{ __html: problemStatement }} />
                {/*<div className="problemSamples" dangerouslySetInnerHTML={{ __html: problemSamples }} />*/}
                <SubmitForm problemId={parseInt(problemId)}/>
                <Runs problemId={parseInt(problemId)} runs={problemRuns} />
              </TabPane>
              <TabPane tab="Результаты" key="standings" />
              <TabPane tab="Посылки" key="runs" />
              <TabPane tab="Решение" key="solution" />
              <TabPane tab="Темы и источники" key="sources" />
            </Tabs>

          </Box>
          </div>
        </Layout>
      </ProblemPageWrapper>
    );
  }
}

export default compose(
  withRouter,
  connect(state => ({
    problems: state.problems,
    windowWidth: state.ui.width,
  }))
)(ProblemPage);
