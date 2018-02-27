import React from 'react';
import styled from 'styled-components';
import { Layout } from 'antd';
import { connect } from 'react-redux';

import IsoTopbarWrapper from '../../isomorphic/containers/Topbar/topbar.style';

import Avatar from './Avatar';
import Buffer from './Buffer';
import Button from '../utility/Button';
import Notifications from './Notifications';
import Search from './Search';
import * as uiActions from '../../actions/uiActions';

const { Header } = Layout;

const TopbarWrapper = styled(IsoTopbarWrapper)`
  .isomorphicTopbar {
    &.collapsed {
      padding: 0 61px 0 68px;
    }
    &:not(.collapsed) {
      padding: 0 61px 0 68px;
      @media (min-width: 1280px) {
        padding-left: calc(68px + 320px);
      }
      @media (max-width: 767px) {
        padding: 0 15px !important;
      }
    }
    @media (max-width: 767px) {
      padding: 0 15px;
    }
    
    .isoLeft {
      flex: 2;
      
      .triggerBtn {
        &:before {
          font-size: 36px;
        }
      }
    }
    
    .isoRight {
      flex: 2;
      justify-content: flex-end;
      
      & > * {
        margin-left: 15px;
        margin-right: 15px;
      }
    }
    
    .leftTitle {
      font-size: 18px;
      margin-left: 19px;
    }
    .centerTitle {
      font-size: 18px;
    }
    
    .backBtn {
      margin-left: 28px;
    }
    
    .loginBtn > * {
      font-size: 14px;
      height: 34px; 
    }
    
    @media (max-width: 575px) {
      .bufferBtn, .notificationBtn { display: none; } 
      & > * { margin: 0; }
      .backBtn { margin-left: 28px; }
    }
    @media (max-width: 1279px) {
      .searchInput, .leftTitle { display: none; }
    }
    @media (min-width: 1280px) {
      .centerTitle, .backBtn { display: none; }
    }
  }
`;

export class Topbar extends React.Component {
  render() {
    const styling = {
      background: '#333b50',
      height: 60,
      width: '100%',
      position: 'fixed',
      color: '#ffffff',
    };

    const loggedIn = true;

    const rightContent = loggedIn ? [
      <div className="bufferBtn" key={0}><Buffer /></div>,
      <div className="notificationBtn" key={1}><Notifications /></div>,
      <div className="userAvatar" key={2}><Avatar /></div>,
    ] : [
      <div className="loginBtn"><Button type="primary" size={"small"}>ВОЙТИ</Button></div>
    ];


    return (
      <TopbarWrapper>
        <Header
          style={styling}
          className={
            this.props.sidebarCollapsed ? 'isomorphicTopbar collapsed' : 'isomorphicTopbar'
          }
        >

          <div className="isoLeft">
            <i
              className="material-icons md-24"
              onClick={() => this.props.dispatch(uiActions.toggleSidebar())}
              style={{ cursor: 'pointer' }}
            >
              menu
            </i>
            <i className="material-icons md-24 backBtn">keyboard_arrow_left</i>
            <div className="leftTitle">Информатикс</div>
          </div>

          <div className="centerTitle">Информатикс</div>

          <div className="isoRight">
            <div className="searchInput">
              <Search />
            </div>
            {rightContent}
          </div>
        </Header>
      </TopbarWrapper>
    );
  }
}

export default connect(state => ({
  sidebarCollapsed: state.ui.sidebarCollapsed,
}))(Topbar);
