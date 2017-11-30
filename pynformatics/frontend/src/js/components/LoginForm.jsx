import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { reduxForm, formValueSelector, Field } from 'redux-form';

import { getRedirectUrl } from '../utils/oauth';
import * as userActions from '../actions/userActions';


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
}))
export default class LoginForm extends React.Component {
  static propTypes = {
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
      const { code, state: provider } = params;
      props.dispatch(userActions.oauthLogin(provider, code));
      props.history.replace(props.location.path);
    }
    this.login = this.login.bind(this);
  }

  login() {
    const { username, password } = this.props.formValues;
    this.props.dispatch(userActions.login(username, password)).then(() => {
      alert('Successful login');
    }).catch((error) => {
      const errorMessage = error.response.data.message;
      alert(errorMessage);
    });
  }

  render() {
    const { handleSubmit } = this.props;

    return (
      <div>
        <form onSubmit={handleSubmit(this.login)}>
          <div>
            <Field component="input" type="text" name="username" placeholder="username" />
          </div>
          <div>
            <Field component="input" type="password" name="password" placeholder="password" />
          </div>
          <div>
            <input type="submit" value="submit" />
          </div>
        </form>
        <hr />
        <div>
          Login through
          <ul>
            <li><a href={getRedirectUrl('vk')}>VK</a></li>
            <li><a href={getRedirectUrl('google')}>google</a></li>
          </ul>
        </div>
      </div>
    );
  }
}
