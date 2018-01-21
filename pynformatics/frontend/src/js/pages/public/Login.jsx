import React from "react";

import {Icon, Menu} from "antd";

import style from '../../../css/pages/public/login.css';

import Button from '../../components/utility/Button';
import Input, {InputGroup} from "../../components/utility/Input";
import Checkbox from "../../components/utility/Checkbox";
import Telegram from "../../components/Sidebar/Telegram";

import MainContentWrapper from '../../components/utility/MainContentWrapper';

import {
  Col,
  Row,
} from '../../components/utility/Grid';


export default class LoginPage extends React.Component {
  render() {
    return (
      <MainContentWrapper>
        <Row type="flex" justify="center">
          <Col xs={{span: 22}} md={16} style={{marginBottom: "16px"}}>
            <Row type="flex" className={style.wrapper}>
              <Col xs={{span: 22, offset: 1, order: 2}} md={{span: 9, offset: 1, order: 1}}>
                <div className={style.leftColumn}>
                  <Menu defaultSelectedKeys={["1"]} className={style.menu}>
                    <Menu.Item key="1">Вход</Menu.Item>
                    <Menu.Item key="2">Регистрация как ученик</Menu.Item>
                    <Menu.Item key="3">Регистрация как учитель</Menu.Item>
                    <Menu.Item key="4">Регистрация комнады</Menu.Item>
                    <Menu.Item key="5">Восстановить пароль</Menu.Item>
                  </Menu>
                  <Telegram/>
                </div>
              </Col>
              <Col xs={{span: 22, offset: 1, order: 1}} md={{span: 12, offset: 1, order: 2}}>
                <div className={style.form}>
                  <div className={style.formTitle}>Вход</div>
                  <div className={style.errorMessage}>
                     <span><Icon type="exclamation-circle-o" /></span>Сообщение об ошибке, если есть
                  </div>
                  <Input
                    size="large"
                    placeholder="Логин"
                  />
                  <Input
                    size="large"
                    placeholder="Пароль"
                    type="password"
                  />
                  <InputGroup className={style.inputGroup}>
                    <Button type="primary">Войти</Button>
                    <Checkbox>Запомнить меня</Checkbox>
                  </InputGroup>
                </div>
                <Row>
                  <Col span={"24"} className={style.socialButtonGroup}>
                    <Button className={style.VKButton}>Войти через ВКонтакте</Button>
                    <Button className={style.GmailButton}>Войти через Gmail</Button>
                  </Col>
                </Row>
              </Col>
            </Row>
          </Col>
        </Row>
      </MainContentWrapper>
    )
  }
}