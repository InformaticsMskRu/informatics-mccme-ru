import React from "react";
import styled from "styled-components";
import {Icon, Menu} from "antd";


import {InputGroup} from "../../isomorphic/components/uielements/input";
import IsoCheckbox from "../../isomorphic/components/uielements/checkbox";

import Button from '../../components/utility/Button';
import Input from "../../components/utility/Input";
import Telegram from "../../components/Sidebar/Telegram";

import MainContentWrapper from '../../components/utility/MainContentWrapper';

import {
  Col,
  Row,
} from '../../components/utility/Grid';


const Wrapper = styled.div`
  border-radius: 6px;
  background-color: #ffffff;
  box-shadow: 0 0 24px 0 rgba(182, 189, 197, 0.42);
`;

const Wrapper2 = styled.div`
  margin-top: 16px;
  margin-bottom: 16px;
  padding: 20px;
  border-radius: 4px;
  background-color: #f3f5f7;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  
  .ant-menu-vertical {
    border-right: 0;
  }
  
  .ant-menu {
    background-color: #f3f5f7;
    color: #788195;
  }
  
  .ant-menu-vertical .ant-menu-item {
    padding: 0;
    margin-top: 0;
  }
  
  .ant-menu:not(.ant-menu-horizontal) .ant-menu-item-selected {
    background-color: #f3f5f7;
    color: #4482ff;
  }
`;

const Wrapper3 = styled.div`
  margin: 5px 0;
  font-family: Roboto;
  font-size: 14px;
  font-weight: normal;
  font-style: normal;
  font-stretch: normal;
  line-height: 2.14;
  letter-spacing: normal;
  text-align: left;
  color: #788195;
`;

const FormWrapper = styled.div`
  margin-top: 32px;
  margin-bottom: 16px;
`;

const ErrorMessage = styled.div`
  border-radius: 4px;
  background-color: #fffbee;
  border: solid 1px #fff5d5;
  padding-left: 8px;
  
  font-family: Roboto;
  font-size: 14px;
  font-weight: normal;
  font-style: normal;
  font-stretch: normal;
  line-height: 2.14;
  letter-spacing: normal;
  text-align: left;
  color: #788195;
`;

const VKButton = styled(Button)`
  &.ant-btn {
    padding: 0 14px;
  
    border-radius: 3px;
    background-color: #527daf;
    font-family: Roboto;
    font-size: 12px;
    font-weight: normal;
    font-style: normal;
    font-stretch: normal;
    line-height: normal;
    letter-spacing: normal;
    text-align: left;
    color: #ffffff;
  }
`;


const GmailButton = styled(Button)`
  &.ant-btn {
    padding: 0 14px;
  
    border-radius: 3px;
    background-color: #4890f8;
    font-family: Roboto;
    font-size: 12px;
    font-weight: normal;
    font-style: normal;
    font-stretch: normal;
    line-height: normal;
    letter-spacing: normal;
    text-align: left;
    color: #ffffff;
  }
`;

export default class LoginPage extends React.Component {
  render() {
    return (
      <MainContentWrapper>
        <Row type="flex" justify="center">
          <Col xs={{span: 22}} md={16} style={{marginBottom: "16px"}}>
            <Wrapper>
              <Row type="flex" style={{height: "100%"}}>
                <Col xs={{span: 22, offset: 1, order: 2}} md={{span: 9, offset: 1, order: 1}}>
                  <Wrapper2>
                    <Menu defaultSelectedKeys={["1"]}>
                      <Menu.Item key="1">Вход</Menu.Item>
                      <Menu.Item key="2">Регистрация как ученик</Menu.Item>
                      <Menu.Item key="3">Регистрация как учитель</Menu.Item>
                      <Menu.Item key="4">Регистрация комнады</Menu.Item>
                      <Menu.Item key="5">Восстановить пароль</Menu.Item>
                    </Menu>
                    {/*<div style={{marginBottom: "16px"}}>*/}
                      {/*<Wrapper3>Вход</Wrapper3>*/}
                      {/*<Wrapper3>Регистрация как ученик</Wrapper3>*/}
                      {/*<Wrapper3>Регистрация как учитель</Wrapper3>*/}
                      {/*<Wrapper3>Регистрация комнады</Wrapper3>*/}
                      {/*<Wrapper3>Восстановить пароль</Wrapper3>*/}
                    {/*</div>*/}
                    <Telegram/>
                  </Wrapper2>
                </Col>
                <Col xs={{span: 22, offset: 1, order: 1}} md={{span: 12, offset: 1, order: 2}}>
                  <FormWrapper>
                    <div style={{fontFamily: "Roboto", fontSize: "22px", color: "#2d3446", marginBottom: "16px"}}>Вход</div>
                    <ErrorMessage style={{marginBottom: "16px"}}>
                       <span><Icon type="exclamation-circle-o" /></span> Сообщение об ошибке, если есть
                    </ErrorMessage>
                    <Input
                      size="large"
                      placeholder="Логин"
                      style={{marginBottom: '16px'}}
                    />
                    <Input
                      size="large"
                      placeholder="Пароль"
                      type="password"
                      style={{marginBottom: '16px'}}
                    />
                    <InputGroup style={{
                      marginBottom:	'16p',
                      display: 'inline-flex',
                      justifyContent: 'flex-start',
                      flexWrap: 'wrap',
                      alignItems: 'center'
                    }}>
                      <Button	type="primary" style={{marginRight: '16px'}}>Войти</Button>
                      <IsoCheckbox>Запомнить меня</IsoCheckbox>
                    </InputGroup>
                  </FormWrapper>
                  <Row>
                    <Col span={"24"} style={{
                      display: 'inline-flex',
                      justifyContent: 'flex-start',
                      flexWrap: 'wrap',
                      marginBottom: '16px'
                    }}>
                      <VKButton style={{marginRight: '8px'}}>Войти через ВКонтакте</VKButton>
                      <GmailButton>Войти через Gmail</GmailButton>
                    </Col>
                  </Row>
                </Col>
              </Row>
            </Wrapper>
          </Col>
        </Row>
      </MainContentWrapper>
    )
  }
}