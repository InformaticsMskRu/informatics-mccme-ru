import React from "react";

import FormWrapper from "./FormWrapper";

import Button from '../../components/utility/Button';
import Input, {InputGroup} from "../../components/utility/Input";
import {Col} from '../../components/utility/Grid';


const RegisterAsStudent = () => (
  <FormWrapper
    title="Привет, ученик!"
    subtitle={"Ученик может решать задачи, принимать участие в курсах,"
              + " олимпиадах и сборах, видеть задачи недоступные для гостей"}
    errorMessage="Сообщение об ошибке если есть"
  >
    <Input size="large" placeholder="Логин"/>
    <InputGroup className="inputGroup">
      <Col xs={14} md={16}>
        <Input
          size="large"
          placeholder="Пароль"
          type="password"
        />
      </Col>
      <Col xs={10} md={8}>
        <Button className="generateButton">Сгенерировать</Button>
      </Col>
    </InputGroup>
    <br/>
    <Input size="large" placeholder="Фамилия"/>
    <Input size="large" placeholder="Имя"/>
    <InputGroup>
      <Col span={12}><Input size="large" placeholder="Город"/></Col>
      <Col span={12}><Input size="large" placeholder="Страна"/></Col>
    </InputGroup>
    <Input size="large" placeholder="E-mail"/>
    <Input size="large" placeholder="Учебное заведение"/>
    <Button type="primary">Зарегистрироваться</Button>
  </FormWrapper>
);

export default RegisterAsStudent;