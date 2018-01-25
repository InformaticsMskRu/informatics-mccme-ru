import React from "react";

import FormWrapper from "./FormWrapper";

import Button from '../../components/utility/Button';
import Input from "../../components/utility/Input";


const ResetPassword = () => (
  <FormWrapper
    title="Восстановление пароля"
    subtitle={"Введите логин, под которым Вы регистрировались в системе."
              + " На Вашу почту будет отправлено письмо с дальнейшими инструкциями."}
  >
    <Input
      size="large"
      placeholder="Логин"
    />
    <Button type="primary">Отправить письмо</Button>
  </FormWrapper>
);

export default ResetPassword;