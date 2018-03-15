import React from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import { logout } from "../../actions/userActions";

import isUserLoggedIn from "../../utils/isUserLoggedIn";

@connect(state => ({
  isLoggedIn: isUserLoggedIn(state.user)
}))
class Logout extends React.Component {
  componentDidMount = () => {
    this.props.dispatch(logout())
  };

  render() {
    const  { isUserLoggedIn } = this.props;
    const { from } = this.props.location.state || { from: { pathname: "/" } };

    if (isUserLoggedIn) {
      return <div>This is logout page</div>
    }
    return <Redirect to={from}/>
  };
}

export default Logout;
