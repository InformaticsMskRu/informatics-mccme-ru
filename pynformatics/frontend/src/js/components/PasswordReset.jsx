import React from "react";
import PropTypes from "prop-types";
import {connect} from "react-redux";

import SearchForm from "./SearchForm";
import {resetPassword} from "../actions/userActions";


@connect(state => ({
  search: state.search
}))
export default class PasswordReset extends React.Component {
  static propTypes = {
    dispatch: PropTypes.func,
  };

  resetPassword = (user_id) => {
    this.props.dispatch(resetPassword(user_id))
      .then((response) => {
        console.log(response);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  handleClickResetPassword(user) {
    const confirmation = confirm("Reset password for user " + user.username + "?");
    if (confirmation) {
      this.resetPassword(user.id)
    }
  };

  render() {
    const usersRows = this.props.search.data.map(user => (
      <tr key={user.id}>
        <td>{user.id}</td>
        <td>{user.username}</td>
        <td>{user.email}</td>
        <td>{user.firstname}</td>
        <td>{user.lastname}</td>
        <td>
          <button onClick={() => {
            this.handleClickResetPassword(user)
          }}>reset password
          </button>
        </td>
      </tr>
    ));
    return (
      <div>
        <SearchForm mode='live'/>
        <table>
          <thead>
          <tr>
            <th>ID</th>
            <th>username</th>
            <th>email</th>
            <th>firstname</th>
            <th>lastname</th>
            <th></th>
          </tr>
          </thead>
          <tbody>{usersRows}</tbody>
        </table>
      </div>
    )
  }
}