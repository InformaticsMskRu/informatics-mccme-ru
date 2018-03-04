import React from "react";
import { connect } from "react-redux";
import { NavLink, Route } from "react-router-dom";

import { Menu } from "antd";
import isUserLoggedIn from "../../utils/isUserLoggedIn";

import Login from "./Login";
import Logout from "./Logout";
import RegisterAsStudent from "./RegisterAsStudent";
import RegisterAsTeacher from "./RegisterAsTeacher";
import RegisterAsTeam from "./RegisterAsTeam";
import ResetPassword from "./ResetPassword";

import MainContentWrapper from '../../components/utility/MainContentWrapper';
import { Col, Row } from '../../components/utility/Grid';
import Telegram from "../../components/Sidebar/Telegram";

import StyleWrapper from './style';


@connect(state => ({
  isLoggedIn: isUserLoggedIn(state.user),
}))
export default class LoginPage extends React.Component {
  render() {
    const { match, isLoggedIn } = this.props;

    const usersArrays = [
      [{ key: 'johnn', username: 'johnn', firstname: 'John', lastname: 'Doe' },
        { key: 'doee', username: 'doee', firstname: 'Doe', lastname: 'John' },
        { key: 'dojo', username: 'dojo', firstname: 'Jo', lastname: 'Do' }],
      [], []
    ];

    const options = [
      {
        url: `${match.url}/login`,
        linkText: "Вход",
        component: Login
      },
      {
        url: `${match.url}/register_as_student`,
        linkText: "Регистрация как ученик",
        component: RegisterAsStudent
      },
      {
        url: `${match.url}/register_as_teacher`,
        linkText: "Регистрация как учитель",
        component: RegisterAsTeacher
      },
      {
        url: `${match.url}/register_as_team`,
        linkText: "Регистрация команды",
        component: () => <RegisterAsTeam usersArrays={usersArrays}/>
      },
      {
        url: `${match.url}/reset_password`,
        linkText: "Восстановление пароля",
        component: ResetPassword
      },
    ];
    if (isLoggedIn) {
      options.push({
        url: `${match.url}/logout`,
        linkText: "Выйти",
        component: Logout
      });
    }

    const menuItems = options.map(option => (
      <Menu.Item key={option.url}>
        <NavLink
          exact to={option.url}
          className="link"
          activeClassName="linkActive"
        >
          {option.linkText}
        </NavLink>
      </Menu.Item>
    ));

    const routes = options.map(option => (
      <Route exact path={option.url} component={option.component} key={option.url}/>
    ));

    return (
      <MainContentWrapper>
        <Row type="flex" justify="center">
          <Col xs={22} md={20} style={{ marginBottom: "16px" }}>
            <StyleWrapper>
              <Row type="flex" className="wrapper">
                <Col xs={{ span: 22, offset: 1, order: 2 }} md={{ span: 8, offset: 1, order: 1 }}>
                  <div className="leftColumn">
                    <Menu className="menu">
                      {menuItems}
                    </Menu>
                    <Telegram/>
                  </div>
                </Col>
                <Col xs={{ span: 22, offset: 1, order: 1 }} md={{ span: 13, offset: 1, order: 2 }}>
                  {routes}
                </Col>
              </Row>
            </StyleWrapper>
          </Col>
        </Row>
      </MainContentWrapper>
    )
  }
}