import { compose } from 'redux';
import { connect } from 'react-redux';
import React from 'react';
import { Layout } from 'antd';
import PropTypes from 'prop-types';
import { withRouter } from 'react-router-dom';

import Box from '../../components/utility/Box';
import Blockage from "./Blockage";
import MainContentWrapper from '../../components/utility/MainContentWrapper';
import Menu from './Menu';
import Problem from '../../components/Problem/Problem';
import { ToggleDrawerIcon } from '../../components/Icon';
import * as contextActions from '../../actions/contextActions';
import * as statementActions from '../../actions/statementActions';


const { Sider } = Layout;

const StatementPageWrapper = MainContentWrapper.extend`
  max-width: 1280px;
  
  .statementSider {
    .ant-layout-sider {
      background: none;
    }
  }
  
  .statementContent {
    position: relative;
    width: 100%;
    overflow-x: auto;
    margin-left: 30px;
    > div {
      height: auto;
    }
    
    .toggleDrawer {
      display: none;
      position: absolute;
      left: 20px;
      top: 30px;
      cursor: pointer;
    }
  }
  
  @media (max-width: 1279px) {  
    .statementSider { 
      position: absolute;
      z-index: 100; 
    }
    
    .statementContent { 
      margin-left: 0;
      
      .toggleDrawer {
        display: block;
      }
    }
  }
  
  @media (max-width: 767px) {
    padding: 80px 0 0;
  }
`;

export class StatementPage extends React.Component {
  static childContextTypes = {
    statementId: PropTypes.number,
  };

  static propTypes = {
    match: PropTypes.object.isRequired,
    statements: PropTypes.object.isRequired,
  };

  constructor(props) {
    super(props);

    this.state = {
      collapsed: false,
    };

    this.fetchStatement = this.fetchStatement.bind(this);
    this.toggleCollapse = this.toggleCollapse.bind(this);
    this.changeProblemRank = this.changeProblemRank.bind(this);
  }

  componentDidMount() {
    this.fetchStatement();
  }

  getChildContext() {
    const { statementId } = this.props.match.params;
    return { statementId: parseInt(statementId) };
  }

  fetchStatement() {
    const { statementId, problemRank } = this.props.match.params;
    this.props.dispatch(statementActions.fetchStatement(statementId)).then(result => {
      const {
        participant,
        olympiad,
        problems,
        virtual_olympiad: virtualOlympiad,
      } = result.value.data;

      if ((olympiad || virtualOlympiad) && typeof participant === 'undefined') {
        this.props.history.replace(`/contest/${statementId}`);
      } else if (problems && typeof problemRank === 'undefined') {
        this.changeProblemRank(_.keys(problems)[0]);
      }
    });
  }

  toggleCollapse() {
    this.setState({
      ...this.state,
      collapsed: !this.state.collapsed,
    });
  }

  changeProblemRank(nextProblemRank) {
    const { statementId, problemRank } = this.props.match.params;
    const nextLocation = `/contest/${statementId}/problem/${nextProblemRank}`;
    if (typeof problemRank === 'undefined') {
      this.props.history.replace(nextLocation);
    } else {
      this.props.history.push(nextLocation);
    }
  }

  render() {
    const { statementId, problemRank } = this.props.match.params;
    const { collapsed } = this.state;
    const { windowWidth } = this.props;

    const statement = this.props.statements[statementId] || {};
    const {
      fetched,
      olympiad,
      virtual_olympiad: virtualOlympiad,
      participant,
    } = statement;

    if (!fetched) {
      return <div>fetching</div>;
    } else if ((olympiad || virtualOlympiad) && typeof participant === 'undefined') {
      return (
        <Blockage
          statement={statement}
          fetchStatement={this.fetchStatement}
        />
      );
    }

    const { problems } = statement;

    return (
      <StatementPageWrapper>
        <Layout style={{ position: 'relative' }}>
          <div className="statementSider">
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
                <Menu
                  collapsed={collapsed}
                  selectedKeys={ [problemRank] }
                  statement={statement}
                  onCollapse={this.toggleCollapse}
                  onSelect={({ key }) => this.changeProblemRank(key)}
                />
              </Box>
            </Sider>
          </div>
          <div className="statementContent">
            <ToggleDrawerIcon
              className="toggleDrawer"
              onClick={this.toggleCollapse}
            />
            {
              problemRank
                ? <Problem problemId={problems[problemRank].id} statementId={parseInt(statementId)} />
                : null
            }
          </div>
        </Layout>
      </StatementPageWrapper>
    );
  }
}

export default compose(
  withRouter,
  connect(state => ({
    statements: state.statements,
    windowWidth: state.ui.width,
  }))
)(StatementPage);
