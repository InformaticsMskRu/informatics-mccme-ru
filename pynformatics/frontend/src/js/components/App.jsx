import PropTypes from 'prop-types';
import React from 'react';
import { Switch, Route, withRouter } from 'react-router-dom';
import { connect } from 'react-redux';

import Problem from './Problem';
import Statement from './Statement';
import Login from './LoginForm';

import MainPage from '../pages/Main/Main';

import StatementAdmin from '../pages/StatementAdmin';
import StatementSettingsForm from './StatementSettingsForm';

import * as bootstrapActions from '../actions/bootstrapActions';
import * as userActions from '../actions/userActions';

import { ThemeProvider } from 'styled-components';
import themes from '../isomorphic/config/themes';
import { Layout } from 'antd';

import 'antd/dist/antd.css';
import '../isomorphic/containers/App/global.css';
import '../../css/style.css';


@withRouter
@connect(state => ({
  user: state.user,
}))
export default class App extends React.Component {
  static propTypes = {
    dispatch: PropTypes.func,
  };

  componentDidMount() {
    this.props.dispatch(bootstrapActions.fetchBootstrap());
  }

  render() {
    const { Content } = Layout;

    return (
      <ThemeProvider theme={themes.themedefault}>
        <Layout style={{ height: '100%', background: '#f3f5f7' }}>
          <div style={{ height: '59px', backgroundColor: '#333b50' }} />
          <Content
            className="isomorphicContent"
          >
            <Switch><Route exact path="/" component={MainPage} /></Switch>
          </Content>
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
