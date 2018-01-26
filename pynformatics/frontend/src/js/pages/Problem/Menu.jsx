import { Layout } from 'antd';
import { Link } from 'react-router-dom';
import React from 'react';
import ReactDOM from 'react-dom';
import styled from 'styled-components';
import { palette } from 'styled-theme';
import PropTypes from 'prop-types';
import { Menu as AntdMenu } from 'antd';


import { borderRadius, transition } from '../../isomorphic/config/style-util';

import Button from '../../components/utility/Button';
import Progress from '../../components/utility/Progress';
import { STATUSES } from '../../constants';
import { ToggleDrawerIcon } from '../../components/Icon';
import Tooltip from '../../components/utility/Tooltip';

const { Sider } = Layout;


const MenuWrapper = styled.div`
  color: #393A39;
  
  .header { position: relative; }
  
  .title {
    border-bottom: 1px solid ${palette('other', 1)};
    padding-bottom: 17px;
    
    .bootcampTitle {
      font-size: 12px;
      color: ${palette('secondary', 2)};
      margin-bottom: 6px;
      padding-right: 40px;
    }
    
    .contestTitle {
      font-size: 16px;
      margin-bottom: 15px;
    }
    
    .toggleDrawer {
      width: 36px;
      height: 36px;
      border: 1px solid #e6e5e5;
      ${borderRadius('3px')};
      padding: 8px 6px;
      cursor: pointer;
      
      position: absolute;
      z-index: 1;
      top: 0;
      right: 0;
      
      i { height: auto; }
    }
  }
  
  .time {
    font-size: 14px;
    margin-top: 16px;
    
    > div:not(:last-child) { margin-bottom: 10px }
    
    .ant-progress-bg { background: ${palette('other', 0)}; }
  }
  
  .info {
    border-bottom: 1px solid ${palette('other', 1)};
    padding-bottom: 17px;
  
    margin-top: 16px;
    font-size: 14px;
    color: ${palette('secondary', 2)};
  }
  
  .problems {
    margin-bottom: 40px;
  
    .ant-menu {
      border: none;
      
      .ant-menu-item {
        margin-left: -20px;
        padding: 0 0 0 20px;
        min-height: 40px;
        height: auto;
        
        &.ant-menu-item-selected {
          color: ${palette('other', 6)};
          font-weight: bold;
          background: none;
          
          .problemSelected { display: block !important; }
        }
        
        .ant-menu-inline-collapsed-tooltip { display: none !important; }
        
        &.ant-menu-item-active {
          background: none;
        }
        
        .problemMenuItem {
          display: flex;
          flex-flow: row nowrap;
          
          .problemSelected { 
            display: none;
            position: absolute;
            left: 0px;
            top: 0px;
            width: 6px;
            height: 100%;
            background: ${palette('other', 6)}; 
          }
          
          .problemLetter {
            margin: auto 18px auto 0;
          }
          
          .problemTitle {
            margin: auto 0;
            white-space: normal;
            line-height: normal;
          }
          
          .problemStatus {
            flex: 0 0 30px;
            margin: auto 0 auto auto;
            height: 20px;
            display: flex;
            align-content: center;
            justify-content: center;
            
            .problemStatusContainer {
              width: 8px;
              height: 8px;
              ${borderRadius('4px')}
              margin: auto;
              ${transition()}
              text-align: right;
              
              &.problem-orange { background: ${palette('other', 3)}; }
              &.problem-green { background: ${palette('other', 4)}; }
              &.problem-blue { background: ${palette('other', 5)}; }
            
              > div {
                opacity: 0;
                color: #ffffff;
                font-size: 12px;
                font-weight: normal;
                line-height: 20px;
              }
            }
          }
        }
      }
    }
  }
  
    
  &:hover:not(.collapsed) {
    .problems {
      .ant-menu {
        .ant-menu-item {
          .problemMenuItem {
            .problemStatus {
            
              .problemStatusContainer {
                width: 30px;
                height: 20px;
                text-align: center;
                ${borderRadius('10px')}
                
                > div {
                  opacity: 1;
                }
              }
            
            }
          }
        }
      }
    }
  }
  
  &.collapsed {
    .title {
      border: none;
      
      > *:not(.toggleDrawer) { display: none; }
      > a > button { transition: none; }
      
      .toggleDrawer {
        border: none;
        right: 0x;
      }
    }
    
    .time {
      > *:not(.ant-progress) { display: none;  }
    
      .ant-progress {        
        position: absolute;
        bottom: 4px;
        left: 17px;
        
        transform-origin: 0 50%;
        transform: rotate(-90deg);
      }
    }
    
    .info { display: none; }
    
    .problems {
      .ant-menu {
      
        .ant-menu-item {
          margin-left: -4px;
          padding: 0 0 0 18px;
        
          .problemMenuItem {
            .problemLetter {
              margin: 0;
              width: 10px;
              text-align: center;
            }
          
            .problemTitle { display: none; }
            
            .problemStatus {
              flex: 8px 0 0;
              margin: auto auto 1px -1px;
            }
          }
        }
      }
    }
  }
`;


const MenuProblem = ({letter, title, status}) => (
  <Link to="/problem">
    <div className="problemMenuItem">
      <div className="problemSelected" />
      <div className="problemLetter">{letter}</div>
      <div className="problemTitle">{title}</div>
      <div className="problemStatus">
        <Tooltip placement="right" title={STATUSES[status].long}>
          <div
            className={`problemStatusContainer problem-${STATUSES[status].color}`}
          >
            <div>{STATUSES[status].short}</div>
          </div>
        </Tooltip>
      </div>
    </div>
  </Link>
);


export class Menu extends React.Component {
  static propTypes = {
    collapsed: PropTypes.bool.isRequired,
    onCollapse: PropTypes.func.isRequired,
  };

  static childContextTypes = {
    siderCollapsed: PropTypes.bool, // hack to hide tooltips in collapsed menu items
  };

  constructor() {
    super();

    this.state = {
      headerHeight: null,
    }
  }

  componentDidMount() {
    const headerHeight = ReactDOM.findDOMNode(this)
      .getElementsByClassName('header')[0].clientHeight;
    this.setState({
      ...this.state,
      headerHeight,
    });
  }


  getChildContext() {
    return {
      siderCollapsed: false,
    };
  }

  render() {
    const { collapsed, onCollapse } = this.props;
    const { headerHeight } = this.state;

    return (
      <MenuWrapper className={collapsed ? 'collapsed' : null}>
        <div
          className="header"
          style={headerHeight ? { height: headerHeight } : {}}
        >
          <div className="title">
            <div className="toggleDrawer" onClick={onCollapse}><ToggleDrawerIcon /></div>
            <div className="bootcampTitle">Название сборов</div>
            <div className="contestTitle">Название контеста</div>
            <Link to='/'><Button type="secondary" size="small">Результаты контеста</Button></Link>
          </div>

          <div className="time">
            <div>12 декабря 16:00 &mdash; 21:00</div>
            <div>Сейчас {(new Date()).toTimeString().slice(0, 5)}</div>
            <Progress
              percent={60}
              showInfo={false}
              style={(collapsed && headerHeight)
                ? { width: headerHeight - 71 }
                : {}}
            />
          </div>

          <div className="info">
            Количество элементов во всех структурах данных не превышает 10000, если это не указано особо.
          </div>
        </div>
        <div className="problems">
          <AntdMenu>
            <AntdMenu.Item>
              <MenuProblem letter="A" title="Двойной переворот" status={0} />
            </AntdMenu.Item>
            <AntdMenu.Item>
              <MenuProblem letter="B" title="Вывести четные элементы" status={1}/>
            </AntdMenu.Item>
            <AntdMenu.Item>
              <MenuProblem letter="C" title="Количество положительных элементов" status={7}/>
            </AntdMenu.Item>
          </AntdMenu>
        </div>
      </MenuWrapper>
    );
  }
}

export default Menu;
