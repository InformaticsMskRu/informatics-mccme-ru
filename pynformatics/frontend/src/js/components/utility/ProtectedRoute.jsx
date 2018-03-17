import React from "react";
import { Route, Redirect, withRouter } from "react-router-dom";
import { connect } from "react-redux";

import isUserLoggedIn from "../../utils/isUserLoggedIn";


const LOGIN_URL = "/auth/login";

@withRouter
@connect(state => ({
  isLoggedIn: isUserLoggedIn(state.user),
}))
class ProtectedRoute extends React.Component {
  render() {
    const { component: Component, isLoggedIn, ...rest } = this.props;
    if (!isLoggedIn) {
      return (
        <Route 
          {...rest}
          render={props => 
            <Redirect to={{
              pathname: LOGIN_URL,
              state: { from: props.location }
            }}/>
          }
        />
      );
    }
    return (
      <Route {...rest} render={props => <Component {...props} />}/>
    );

  }
}

export default ProtectedRoute;