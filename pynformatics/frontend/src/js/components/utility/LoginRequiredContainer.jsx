import * as React from "react";
import Redirect from "react-router-dom/es/Redirect";

import {connect} from "react-redux";
import {setRedirectUrl} from "../../actions/routingActions";


const LOGIN_URL = "/auth/login";
const LoginRequiredContainer = (props) => {
  if (!props.isLoggedIn) {
    props.dispatch(setRedirectUrl(props.currentURL));
    return <Redirect to={LOGIN_URL}/>
  }
  return props.children;
};

function mapStateToProps(state, ownProps) {
  return {
    isLoggedIn: !_.isEmpty(state.user),
    currentURL: ownProps.location.pathname
  }
}

export default connect(mapStateToProps)(LoginRequiredContainer)
