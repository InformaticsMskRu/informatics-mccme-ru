import PropTypes from 'prop-types';
import React from 'react';
import { Layout } from 'antd';
import { Route, Switch, withRouter } from 'react-router-dom';
import { compose } from 'redux';
import { connect } from 'react-redux';

import Box from '../../components/utility/Box';
import Blockage from "./Blockage";
import MainContentWrapper from '../../components/utility/MainContentWrapper';
import Menu from './Menu';
import Problem from '../../components/Problem/Problem';
import Standings from './Standings';
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
      z-index: 99;
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
    
    .problemTitle { padding-left: 30px; }
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
    user: PropTypes.object.isRequired,
  };

  constructor(props, context) {
    super(props, context);

    this.state = {
      collapsed: false,
    };

    this.fetchStandings = this.fetchStandings.bind(this);
    this.fetchStatement = this.fetchStatement.bind(this);
    this.toggleCollapse = this.toggleCollapse.bind(this);
    this.changeProblemRank = this.changeProblemRank.bind(this);
  }

  componentDidMount() {
    const statementId = _.get(this.props, 'match.params.statementId');
    this.fetchStatement(statementId);
  }

  componentWillReceiveProps(props, context) {
    const filterGroupId = _.get(props, 'filterGroup.id');
    const oldFilterGroupId = _.get(this.props, 'filterGroup.id');

    const statementId = _.get(props, 'match.params.statementId');
    const oldStatementId = _.get(props, 'match.params.statementId');

    const location = _.get(props, 'location.pathname');
    const oldLocation = _.get(this.props, 'location.pathname');

    if (statementId !== oldStatementId) {
      this.fetchStatement(statementId);
    } else if (filterGroupId !== oldFilterGroupId) {
      this.fetchStandings(statementId, filterGroupId);
    }
  }

  getChildContext() {
    const { statementId } = this.props.match.params;
    return { statementId: parseInt(statementId) };
  }

  fetchStatement(statementId) {
    const { filterGroup } = this.props;
    const { problemRank } = this.props.match.params;
    const showStandings = this.props.location.pathname.indexOf('standings') !== -1;

    this.props.dispatch(statementActions.fetchStatement(statementId)).then(result => {
      const {
        participant,
        olympiad,
        problems,
        virtual_olympiad: virtualOlympiad,
      } = result.value.data;

      if ((olympiad || virtualOlympiad) && typeof participant === 'undefined') {
        this.props.history.replace(`/contest/${statementId}`);
      } else if (problems && typeof problemRank === 'undefined' && !showStandings) {
        this.changeProblemRank(_.keys(problems)[0]);
      }
    });

    this.fetchStandings(statementId, _.get(filterGroup, 'id'));
  }

  fetchStandings(statementId, filterGroupId) {
    this.props.dispatch(statementActions.fetchStatementStandings(
      statementId, filterGroupId
    )).then(() => this.props.dispatch(statementActions.processStandings(statementId)));
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
    const { filterGroup, user, windowWidth } = this.props;

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
          fetchStatement={this.fetchStatement.bind(this, statementId)}
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
                  user={user}
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
            <Route exact path="/contest/:statementId/standings" component={Standings} />
            <Route exact path="/contest/:statementId/problem/:problemRank">
              {
                problemRank
                  ? (
                    <Problem 
                      problemId={problems[problemRank].id} 
                      statementId={parseInt(statementId)} 
                      // onTabChange={() => console.log('tab changed', statementId, _.get(filterGroup, 'id'))}
                      onTabChange={() => this.fetchStandings(statementId, _.get(filterGroup, 'id'))}
                    />
                  ) : null
              }
            </Route>

          </div>
        </Layout>
      </StatementPageWrapper>
    );
  }
}

export default compose(
  withRouter,
  connect(state => ({
    filterGroup: state.group.filterGroup,
    statements: state.statements,
    user: state.user,
    windowWidth: state.ui.width,
  }))
)(StatementPage);
