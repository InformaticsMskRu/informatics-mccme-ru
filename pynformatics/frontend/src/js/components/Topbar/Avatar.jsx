import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import { Link, withRouter } from 'react-router-dom';
import { connect } from 'react-redux';

import Popover from '../utility/Popover';
import DropdownWrapper from './DropdownWrapper';
import isUserLoggedIn from '../../utils/isUserLoggedIn';


const AvatarWrapper = styled.div`
  cursor: pointer;
  display: flex;
  
  img {
    width: 30px;
    height: 30px;
    border-radius: 15px;
    background: #FFFFFF;
  }
`;


export class Avatar extends React.Component {
  static propTypes = {
    user: PropTypes.object.isRequired,
  };

  constructor() {
    super();

    this.state = {
      popoverVisible: false,
    };

    this.togglePopoverVisible = this.togglePopoverVisible.bind(this);
  }

  togglePopoverVisible() {
    this.setState({...this.state, popoverVisible: !this.state.popoverVisible})
  }

  render() {
    const loggedIn = isUserLoggedIn(this.props.user);

    const content = loggedIn
      ? (
        <DropdownWrapper className="isoUserDropdown">
          <Link 
            className="isoDropdownLink"
            to="/" 
          >
            Профиль
          </Link>
          <Link 
            className="isoDropdownLink"
            to="/auth/logout"
            onClick={this.togglePopoverVisible}
          >
            Выйти
          </Link>
        </DropdownWrapper>
      ) : (
        <DropdownWrapper className="isoUserDropdown">
          <Link 
            className="isoDropdownLink"
            to={{
              pathname: '/auth/login',
              state: { from: this.props.location.pathname },
            }}
            onClick={this.togglePopoverVisible}
          >
            Войти
          </Link>
        </DropdownWrapper>
      );

    return (
      <Popover
        trigger="click"
        content={content}
        placement="bottomLeft"
        arrowPointAtCenter={true}
        visible={this.state.popoverVisible}
        onVisibleChange={this.togglePopoverVisible}
      >
        <AvatarWrapper>
          { loggedIn
            ? <img src="/images/ladybug.png"/>
            : <img src="/images/dog.png"/> }
        </AvatarWrapper>
      </Popover>
    );
  }
}


export default withRouter(connect(state => ({
  user: state.user,
}))(Avatar));
