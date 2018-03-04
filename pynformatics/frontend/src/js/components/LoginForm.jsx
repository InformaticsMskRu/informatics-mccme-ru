import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { reduxForm, formValueSelector, Field } from 'redux-form';
import * as _ from 'lodash';

import { getRedirectUrl } from '../utils/oauth';
import * as userActions from '../actions/userActions';
import MainContentWrapper from '../components/utility/MainContentWrapper';

import isUserLoggedIn from "../utils/isUserLoggedIn";

const formName = 'loginForm';
const valueSelector = formValueSelector(formName);


@reduxForm({
  form: formName,
})
@withRouter
@connect(state => ({
  formValues: {
    username: valueSelector(state, 'username'),
    password: valueSelector(state, 'password'),
  },
  user: state.user,
}))
export default class LoginForm extends React.Component {
  static propTypes = {
    user: PropTypes.any,
    handleSubmit: PropTypes.func,
    dispatch: PropTypes.func,
    formValues: PropTypes.any,
    location: PropTypes.any,
    history: PropTypes.any,
  };

  constructor(props) {
    super(props);
    if (props.location.search) {
      const params = _.fromPairs(_.map(
        props.location.search.slice(1).split('&'),
        param => param.split('='),
      ));
      const { code, state } = params;
      const { provider, loggedIn } = JSON.parse(decodeURI(state));

      if (!loggedIn) {
        props.dispatch(userActions.oauthLogin(provider, code));
      } else {
        props.dispatch(userActions.oauthConnect(provider, code));
      }
      props.history.replace(props.location.path);
    }
    this.login = this.login.bind(this);
  }

  login() {
    const { username, password } = this.props.formValues;
    this.props.dispatch(userActions.login(username, password)).then(() => {
      // alert('Successful login');
      this.props.history.push('/goto');
    }).catch((error) => {
      const errorMessage = error.response.data.message;
      alert(errorMessage);
    });
  }

  render() {
    const { handleSubmit, user } = this.props;

    if (isUserLoggedIn(user)) {
      return (
        <MainContentWrapper>
          {/*Connect account*/}
          {/*<ul>*/}
            {/*<li><a href={getRedirectUrl('vk', { loggedIn: true })}>VK</a></li>*/}
            {/*<li><a href={getRedirectUrl('google', { loggedIn: true })}>google</a></li>*/}
          {/*</ul>*/}
        </MainContentWrapper>
      );
    }

    return (
      <MainContentWrapper>
        <form onSubmit={handleSubmit(this.login)}>
          <div>
            <Field component="input" type="text" name="username" placeholder="логин" />
          </div>
          <div>
            <Field component="input" type="password" name="password" placeholder="пароль" />
          </div>
          <div>
            <input type="submit" value="Войти" />
          </div>
        </form>
        <hr />
        {/*<div>*/}
          {/*Login through*/}
          {/*<ul>*/}
            {/*<li><a href={getRedirectUrl('vk')}>VK</a></li>*/}
            {/*<li><a href={getRedirectUrl('google')}>google</a></li>*/}
          {/*</ul>*/}
        {/*</div>*/}
      </MainContentWrapper>
    );
  }
}
