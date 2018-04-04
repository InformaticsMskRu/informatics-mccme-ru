import PropTypes from 'prop-types';
import React from 'react';
import ReactDOM from 'react-dom';
import styled from 'styled-components';
import { Link } from 'react-router-dom';
import { Menu as AntdMenu } from 'antd';
import { palette } from 'styled-theme';
import * as _ from 'lodash';

import Button from '../../components/utility/Button';
import MenuTime from './MenuTime';
import Status from '../../components/Runs/Status';
import { ToggleDrawerIcon } from '../../components/Icon';
import { borderRadius, transition } from '../../isomorphic/config/style-util';
import { getProblemShortNameByNumber } from '../../utils/functions';


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
    
    .statementTitle {
      font-size: 16px;
      margin-bottom: 15px;
      padding-right: 40px;
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
            width: 19px;
            margin: auto 18px auto 0;
          }
          
          .problemTitle {
            margin: auto 0;
            white-space: normal;
            line-height: normal;
          }
          
          .problemStatus {
            margin: auto 0 auto auto;
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
              margin: auto auto 3px 0px;
            }
          }
        }
      }
    }
  }
`;


const MenuProblem = ({letter, rank, score, status, title, collapsed}) => (
  <div className="problemMenuItem">
    <div className="problemSelected" />
    <div className="problemLetter">{letter}</div>
    <div className="problemTitle">{title}</div>
    <div className="problemStatus">
      {
        typeof status !== 'undefined'
        ? <Status score={score} status={status} collapsed={collapsed}/>
        : null
      }
    </div>
  </div>
);


export class Menu extends React.Component {
  static contextTypes = {
    statementId: PropTypes.number,
  };

  static propTypes = {
    collapsed: PropTypes.bool.isRequired,
    statement: PropTypes.object.isRequired,
    user: PropTypes.object.isRequired,
    onCollapse: PropTypes.func,
    onSelect: PropTypes.func,
  };

  static childContextTypes = {
    siderCollapsed: PropTypes.bool, // hack to hide tooltips in collapsed menu items
  };

  constructor() {
    super();

    this.state = {
      headerHeight: null,
      hovered: false,
    }
  }

  componentDidMount() {
    const headerHeight = ReactDOM.findDOMNode(this)
      .getElementsByClassName('header')[0].clientHeight;
    this.setState({
      ...this.state,
      headerHeight,
    });
    if (window.innerWidth < 1280) {
      this.props.onCollapse();
    }
  }


  getChildContext() {
    return {
      siderCollapsed: false,
    };
  }

  render() {
    const { statementId } = this.context;
    const {
      collapsed,
      selectedKeys,
      statement,
      user,
      onCollapse,
      onSelect,
    } = this.props;
    const { headerHeight, hovered } = this.state;

    const {
      problems,
      name: statementTitle,
      participant,
      olympiad,
      virtual_olympiad: virtualOlympiad,
      course: bootcamp,
    } = statement;
    const { full_name: bootcampTitle } = bootcamp;

    const userId = _.get(user, 'id')
    const userResults = _.get(statement, `processed[${userId}].processed.problems`, {});

    const problemItems = _.map(problems, ({ id, name: title }, key) => {
      const { score, status } = userResults[id] || {};
      return (
        <AntdMenu.Item key={key}>
          <MenuProblem
            letter={getProblemShortNameByNumber(parseInt(key))}
            rank={key}
            title={title}
            score={score}
            status={status}
            collapsed={collapsed || !hovered}
          />
        </AntdMenu.Item>
      );
    });

    return (
      <MenuWrapper
        className={collapsed ? 'collapsed' : null}
        onMouseEnter={() => this.setState({...this.state, hovered: true})}
        onMouseLeave={() => this.setState({...this.state, hovered: false})}
      >
        <div
          className="header"
          style={headerHeight ? { height: headerHeight } : {}}
        >
          <div className="title">
            <div className="toggleDrawer" onClick={onCollapse}><ToggleDrawerIcon /></div>
            <div className="bootcampTitle">{bootcampTitle}</div>
            <div className="statementTitle">{statementTitle}</div>
            <Link to={`/contest/${statementId}/standings`}><Button type="secondary" size="small">Результаты контеста</Button></Link>
          </div>

          { (olympiad || virtualOlympiad) && typeof participant !== 'undefined'
            ? <MenuTime
                start={participant.start * 1000}
                duration={participant.duration * 1000}
                collapsed={collapsed}
                headerHeight={headerHeight}
              />
            : null }

          <div className="info">
            Данные вводятся с&nbsp;клавиатуры или из&nbsp;файла input.txt, выводятся на экран или в&nbsp;файл output.txt. 
            Первые тесты не&nbsp;всегда совпадают с&nbsp;примерами из&nbsp;условия.
          </div>
        </div>
        <div className="problems">
          <AntdMenu onSelect={onSelect} selectedKeys={selectedKeys}>
            {problemItems}
          </AntdMenu>
        </div>
      </MenuWrapper>
    );
  }
}

export default Menu;
