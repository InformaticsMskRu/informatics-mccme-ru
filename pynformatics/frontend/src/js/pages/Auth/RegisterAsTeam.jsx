import React from "react";
import {AutoComplete} from "antd";

import FormWrapper from "./FormWrapper";

import Button from '../../components/utility/Button';
import Input from "../../components/utility/Input";


const RegisterAsTeam = ({usersArrays}) => {
  console.log(usersArrays);
  const autoCompletes = usersArrays.map((users, i) => (
    <AutoComplete
      size="large"
      key={i + 1}
      dataSource={users.map(user => user.username + ' ' + user.firstname + ' ' + user.lastname)}
      placeholder={"Участник " + (i + 1)}
      className="autoComplete"
    >
    </AutoComplete>
  ));
  return (
    <FormWrapper title="Новая команда" errorMessage="Сообщение об ошибке если есть">
      <Input
        size="large"
        placeholder="Название команды"
      />
      <div>Состав команды</div>
      {autoCompletes}
      <Button type="primary">Зарегистрировать команду</Button>
    </FormWrapper>
  );
};

export default RegisterAsTeam;