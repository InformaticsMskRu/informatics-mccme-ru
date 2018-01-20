import React from "react";
import styled from 'styled-components';

import Box from '../../components/utility/Box';
import Button from '../../components/utility/Button';
import MainContentWrapper from '../../components/utility/MainContentWrapper';
import ContentHolder from '../../isomorphic/components/utility/contentHolder';
import {
  gutter,
  colStyle,
  rowStyle,
  Col,
  Row,
} from '../../components/utility/Grid';
import Input from "../../components/utility/Input";
import {Icon} from "antd";
import {InputGroup} from "../../isomorphic/components/uielements/input";
import IsoCheckbox from "../../isomorphic/components/uielements/checkbox";
import IsoButton from '../../isomorphic/components/uielements/button';
import Telegram from "../../components/Sidebar/Telegram";

let Wrapper = styled.div`
  
  border-radius: 6px;
  background-color: #ffffff;
  box-shadow: 0 0 24px 0 rgba(182, 189, 197, 0.42);
`;

let Wrapper2 = styled.div`
  margin-top: 16px;
  margin-bottom: 16px;
  padding: 20px;
  border-radius: 4px;
  background-color: #f3f5f7;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
`;

let Wrapper3 = styled.div`
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

let Text = styled.div`
  font-family: Roboto;
  font-size: 12px;
  font-weight: normal;
  font-style: normal;
  font-stretch: normal;
  line-height: 1.5;
  letter-spacing: normal;
  text-align: left;
  color: #676b7a;
  margin-bottom: 8px;
`;

let FormWrapper = styled.div`
  margin-top: 32px;
  margin-bottom: 16px;
`;

let ErrorMessage = styled.div`
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
              <Row style={{height: "100%"}}>
                <Col xs={{span: 22, offset: 1, order: 2}} md={{span: 9, offset: 1, order: 1}}>
                  <Wrapper2>
                    <div>
                      <Wrapper3>Вход</Wrapper3>
                      <Wrapper3>Регистрация как ученик</Wrapper3>
                      <Wrapper3>Регистрация как учитель</Wrapper3>
                      <Wrapper3>Регистрация комнады</Wrapper3>
                      <Wrapper3>Восстановить пароль</Wrapper3>
                    </div>
                    {/*<div>*/}
                      {/*<Text>По всем текущим вопросам, а также в случае, если у вас что-то не работает, пишите на форум или в группу telegram</Text>*/}
                      {/*<PrimaryButton>Telegram</PrimaryButton>*/}
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
                      placeholder="Логин"
                      style={{marginBottom: '16px'}}
                    />
                    <Input
                      placeholder="Пароль"
                      type="password"
                      style={{marginBottom: '16px'}}
                    />
                    <InputGroup style={{
                      marginBottom:	'16p',
                      display: 'inline-flex',
                      justifyContent: 'flex-start',
                      flexWrap: 'wrap',
                      gutter: '8px',
                      alignItems: 'center'
                    }}>
                      <Button	type="primary" style={{marginRight: '8px'}}>Войти</Button>
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