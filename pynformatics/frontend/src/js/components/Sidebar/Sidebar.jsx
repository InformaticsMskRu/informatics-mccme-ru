import React from 'react';
import styled from 'styled-components';
import { connect } from 'react-redux';
import { Layout, Menu } from 'antd';
import { Link } from 'react-router-dom';
import { Scrollbars } from 'react-custom-scrollbars';
import { transition } from '../../isomorphic/config/style-util';
import IsoSidebarWrapper from '../../isomorphic/containers/Sidebar/sidebar.style';

import * as uiActions from '../../actions/uiActions';
import Header from './Header';
import Telegram from './Telegram';
import {
  MenuAdminIcon,
  MenuCoursesIcon,
  MenuGroupsIcon,
  MenuMonitorsIcon,
  MenuManualIcon,
  MenuFireIcon,
  MenuSendingsIcon,
  MenuSettingsIcon,
  MenuTopIcon,
  MenuRatingIcon,
  MenuFreshIcon,
  MenuFAQIcon,
  MenuAboutIcon,
} from '../Icon';


const { Sider } = Layout;

const SidebarWrapper = styled(IsoSidebarWrapper)`
  background: rgb(75, 83, 104);
  @media (max-width: 1279px) {
    position: absolute;
  }
  
  .isomorphicSidebar {
    background: rgb(75, 83, 104);
    width: 100%;
    // flex: 0 0 375px;
    // @media (max-width: 767px) {
    //   width: 375px !important;
    //   flex: 0 0 375px !important;
    // }
    
    .closeBtn {
      position: absolute;
      right: 24px;
      top: 18px;
      color: white;
      cursor: pointer;
      
      @media (min-width: 1280px) { display: none; }
    }
  
    .isoLogoWrapper {
      height: 60px;
      text-align: left;
      padding: 0 24px;
      background: rgb(51, 59, 80);
      @media (max-width: 1279px) {
        background: rgb(75, 83, 104);
      }
      
      h3 {
        a {
          font-size: 16px;
          font-weight: normal;
          text-transform: none;
          line-height: 60px;
          color: rgb(255, 255, 255);
        }
      }
    }
    
    .isoDashboardMenu {
      padding-top: 18px;
    
      .ant-menu-item {
        height: 46px;
        
        a {
          color: rgb(168, 177, 196);
        }
        
        &.ant-menu-item-active {
          svg {
            fill: #ffffff;
          }
        }
        
        &.ant-menu-item-selected {
          background-color: rgb(29, 34, 48) !important;
          svg {
            fill: #ffffff;
          }
        }
        
        .nav-text {
          font-size: 15px;
          line-height: normal;
        }
      }
      
      
      i {
        font-size: 0;
        width: 24px;
        height: 24px;
        margin-right: 20px;
        svg {
          ${transition()}
          fill: rgb(130, 139, 158);
        }
      }
    }
  }
`;


export class Sidebar extends React.Component {
  renderView({ style, ...props }) {
    return (
      <div
        className="box"
        style={{
          ...style,
          marginRight: -17,
          marginLeft: 0,
          paddingRight: 9,
          paddingLeft: 0,
        }}
        {...props}
      />
    )
  }

  render() {
    const { collapsed } = this.props;
    const mode = collapsed ? 'vertical' : 'inline';

    return (
      <SidebarWrapper className="">
        <Sider
          className="isomorphicSidebar"
          collapsible={true}
          collapsed={collapsed}
          trigger={null}
          width="320"
          collapsedWidth="0"
        >
          <i
            className="closeBtn material-icons"
            onClick={() => this.props.dispatch(uiActions.toggleSidebar())}
          >
            close
          </i>
          <Header collapsed={collapsed} />
          <Scrollbars
            renderView={this.renderView}
            style={{
              height: this.props.windowHeight - 60,
            }}
          >
            <Menu
            theme="dark"
            mode={mode}
            className="isoDashboardMenu"
          >
            <Menu.Item key={'admin'}>
              <Link to="/">
                <span className="isoMenuHolder">
                  <MenuAdminIcon />
                  <span className="nav-text">
                    Административный раздел
                  </span>
                </span>
              </Link>
            </Menu.Item>
            <Menu.Item key={'admin_courses'}>
              <Link to="/">
                <span className="isoMenuHolder">
                  <MenuCoursesIcon />
                  <span className="nav-text">
                    Мои курсы
                  </span>
                </span>
              </Link>
            </Menu.Item>
            <Menu.Item key={'admin_groups'}>
              <Link to="/">
                <span className="isoMenuHolder">
                  <MenuGroupsIcon />
                  <span className="nav-text">
                    Управление группами
                  </span>
                </span>
              </Link>
            </Menu.Item>
            <Menu.Item key={'admin_monitors'}>
              <Link to="/">
                <span className="isoMenuHolder">
                  <MenuMonitorsIcon />
                  <span className="nav-text">
                    Управление мониторами
                  </span>
                </span>
              </Link>
            </Menu.Item>
            <Menu.Item key={'admin_manual'}>
              <Link to="/">
                <span className="isoMenuHolder">
                  <MenuManualIcon />
                  <span className="nav-text">
                    Инструкция для учителей
                  </span>
                </span>
              </Link>
            </Menu.Item>

            <Menu.Item key={'my_meetups'} style={{ marginTop: 24 }}>
              <Link to="/">
                <span className="isoMenuHolder">
                  <MenuFireIcon />
                  <span className="nav-text">
                    Мои сборы
                  </span>
                </span>
              </Link>
            </Menu.Item>
            <Menu.Item key={'my_sendings'}>
              <Link to="/">
                <span className="isoMenuHolder">
                  <MenuSendingsIcon />
                  <span className="nav-text">
                    Мои посылки
                  </span>
                </span>
              </Link>
            </Menu.Item>
            <Menu.Item key={'my_settings'}>
              <Link to="/">
                <span className="isoMenuHolder">
                  <MenuSettingsIcon />
                  <span className="nav-text">
                    Мои настройки
                  </span>
                </span>
              </Link>
            </Menu.Item>
            <Menu.Item key={'my_groups'}>
              <Link to="/">
                <span className="isoMenuHolder">
                  <MenuGroupsIcon />
                  <span className="nav-text">
                    Мои группы
                  </span>
                </span>
              </Link>
            </Menu.Item>

            <Menu.Item key={'top'} style={{ marginTop: 24 }}>
              <Link to="/">
                <span className="isoMenuHolder">
                  <MenuTopIcon />
                  <span className="nav-text">
                    Топ решений
                  </span>
                </span>
              </Link>
            </Menu.Item>
            <Menu.Item key={'raiting'}>
              <Link to="/">
                <span className="isoMenuHolder">
                  <MenuRatingIcon />
                  <span className="nav-text">
                    Рейтинг пользователей
                  </span>
                </span>
              </Link>
            </Menu.Item>
            <Menu.Item key={'fresh'}>
              <Link to="/">
                <span className="isoMenuHolder">
                  <MenuFreshIcon />
                  <span className="nav-text">
                    Новые материалы
                  </span>
                </span>
              </Link>
            </Menu.Item>
            <Menu.Item key={'faq'}>
              <Link to="/">
                <span className="isoMenuHolder">
                  <MenuFAQIcon />
                  <span className="nav-text">
                    FAQ
                  </span>
                </span>
              </Link>
            </Menu.Item>
            <Menu.Item key={'about'}>
              <Link to="/about">
                <span className="isoMenuHolder">
                  <MenuAboutIcon />
                  <span className="nav-text">
                    О сайте, команде и<br />организациях-разработчиках
                  </span>
                </span>
              </Link>
            </Menu.Item>

            <Menu.Item
              disabled={true}
              style={{
                height: 'auto',
                cursor: 'default',
                marginTop: 18,
              }}
            >
              <Telegram />
            </Menu.Item>
          </Menu>
          </Scrollbars>
        </Sider>
      </SidebarWrapper>
    );
  }
}


export default connect(state => ({
  collapsed: state.ui.sidebarCollapsed,
  windowHeight: state.ui.height,
}))(Sidebar);
