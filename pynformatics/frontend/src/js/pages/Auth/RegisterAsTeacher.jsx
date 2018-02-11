import React from "react";

import FormWrapper from "./FormWrapper";

import Button from '../../components/utility/Button';
import Input, {InputGroup} from "../../components/utility/Input";
import {Col} from '../../components/utility/Grid';


const RegisterAsTeacher = () => (
  <FormWrapper
    title="Привет, учитель!"
    subtitle={"Учитель может создавать сборы, олимпиады, курсы, группы и решать задачи."
              + " Чтобы получить доступ к ответам и скачиваниям задач, нужно подтверидть,"
              + " что Вы действительно учитель."}
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

export default RegisterAsTeacher;