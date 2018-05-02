import PropTypes from 'prop-types';
import React from 'react';
import WindowResizeListener from 'react-window-size-listener';
import loadScript from 'load-script';
import { Debounce } from 'react-throttle';
import { Switch, Route, withRouter } from 'react-router-dom';
import { ThemeProvider } from 'styled-components';
import { Layout, Spin } from 'antd';
import { connect } from 'react-redux';

import Login from './LoginForm';
import MainContentWrapper from './utility/MainContentWrapper';
import ProtectedRoute from './utility/ProtectedRoute';
import Sidebar from './Sidebar/Sidebar';
import Topbar from './Topbar/Topbar';
import theme from '../theme';

import AboutPage from '../pages/About/About';
import Auth from '../pages/Auth/Auth';
import GroupInvitePage from '../pages/GroupInvite/GroupInvite';
import MainPage from '../pages/Main/Main';
import NotFound from '../pages/Errors/NotFound';
import ProblemPage from '../pages/Problem/Problem';
import StatementPage from '../pages/Statement/Statement';
import TempGotoProblemPage from '../pages/TempGotoProblem';

import * as bootstrapActions from '../actions/bootstrapActions';
import * as uiActions from '../actions/uiActions';

import 'antd/dist/antd.css';
import '../isomorphic/containers/App/global.css';
import '../../css/style.css';
import '../../css/ionicons.min.css';

import ProblemRequestsList from './ProblemRequest/ProblemRequestsList';
import ProblemRequestReview from './ProblemRequest/ProblemRequestReview';

const MATHJAX_CDN = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.3/MathJax.js?config=TeX-MML-AM_CHTML';

const MATHJAX_CONFIG = {
  tex2jax: {
    inlineMath: [ ['$','$'], ['\\(','\\)'] ],
    displayMath: [ ['$$','$$'], ['\[','\]'] ]
  },
  showMathMenu: false,
  showMathMenuMSIE: false
};


@withRouter
@connect(state => ({
  user: state.user,
  rehydrated: state._persist.rehydrated
}))
export default class App extends React.Component {
  static propTypes = {
    dispatch: PropTypes.func,
  };

  constructor(props) {
    super(props);

    loadScript(MATHJAX_CDN, () => {
      window.MathJax.Hub.Config(MATHJAX_CONFIG);
    });
  }

  componentDidMount() {
    this.props.dispatch(bootstrapActions.fetchBootstrap());
  }

  render() {
    const { Content } = Layout;
    const { user } = this.props;

    return (
      <ThemeProvider theme={theme}>
        <Layout style={{ height: '100vh', background: '#f3f5f7' }}>
          <Debounce time="1000" handler="onResize">
            <WindowResizeListener
              onResize={windowSize => this.props.dispatch(uiActions.windowResize(
                windowSize.windowWidth,
                windowSize.windowHeight
              ))}
            />
          </Debounce>
          <Topbar />
          <Layout style={{ flexDirection: 'row', overflowX: 'hidden' }}>
            <Sidebar />
            <Content
              className="isomorphicContent"
              style={{ height: '100vh', overflowY: 'scroll' }}
            >
              { user.bootstrapPending
                ? (
                  <MainContentWrapper style={{ display: 'flex', alignContent: 'center', justifyContent: 'center' }}>
                      <Spin size="large" style={{ margin: '20% auto' }} />
                  </MainContentWrapper>
                ) : (
                  <Switch>
                    <Route exact path="/" component={MainPage} />
                    <Route path="/auth" component={Auth} />
                    <Route exact path="/contest/:statementId" component={StatementPage} />
                    <Route exact path="/contest/:statementId/standings" component={StatementPage} />
                    <Route exact path="/contest/:statementId/problem/:problemRank" component={StatementPage} />
                    <Route exact path="/goto" component={TempGotoProblemPage} />
                    <Route exact path="/login" component={Login} />
                    <Route exact path="/problem/:problemId" component={ProblemPage} />
                    <Route exact path="/about" component={AboutPage} />
                    <ProtectedRoute exact path="/join/:groupInviteUrl" component={GroupInvitePage} />
                    <Route exact path="/problem_requests" component={ProblemRequestsList}/>
                    <Route exact path="/problem_request/:requestId" component={ProblemRequestReview}/>
                    <Route path="*" component={NotFound}/>
                  </Switch>
                ) }
            </Content>
          </Layout>
        </Layout>
      </ThemeProvider>
    );
  }

  // render() {
  //   return (
  //     <div>
  //       <div>
  //         {
  //           (() => {
  //             const { firstname, lastname } = this.props.user;
  //             if (firstname && lastname) {
  //               return (
  //                 <div>
  //                   Logged in as {firstname} {lastname} &nbsp;
  //                   <button onClick={() => { this.props.dispatch(userActions.logout()); }}>
  //                     logout
  //                   </button>
  //                 </div>
  //               );
  //             }
  //           })()
  //         }
  //       </div>
  //       <div className="main-content">
  //         <Switch>
  //           <Route exact path="/example" component={Example} />
  //           <Route exact path="/statement/:statementId" component={Statement} />
  //           <Route exact path="/statement/:statementId/problem/:problemRank" component={Statement} />
  //           <Route
  //             exact
  //             path="/problem/:problemId"
  //             render={props =>
  //               <Problem {...props} problemId={parseInt(props.match.params.problemId, 10)} />
  //             }
  //           />
  //           <Route exact path="/login" component={Login} />
  //           <Route
  //             exact
  //             path="/admin/statement/:statementId"
  //             render={props =>
  //               (
  //                 <StatementSettingsForm
  //                   {...props}
  //                   statementId={parseInt(props.match.params.statementId, 10)}
  //                 />
  //               )
  //             }
  //           />
  //         </Switch>
  //       </div>
  //     </div>
  //   );
  // }
}
