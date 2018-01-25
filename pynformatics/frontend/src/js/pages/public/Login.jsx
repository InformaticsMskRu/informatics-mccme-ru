import React from "react";
import {connect} from "react-redux";

import * as userActions from "../../actions/userActions";

import {AutoComplete, Icon, Menu, Form} from "antd";

import style from '../../../css/pages/public/login.css';

import Button from '../../components/utility/Button';
import Input, {InputGroup} from "../../components/utility/Input";
import Checkbox from "../../components/utility/Checkbox";
import Telegram from "../../components/Sidebar/Telegram";

import MainContentWrapper from '../../components/utility/MainContentWrapper';

import {Col, Row} from '../../components/utility/Grid';
import {NavLink, Route, Redirect} from "react-router-dom";


const FormWrapper = ({title, subtitle, errorMessage, children}) => (
  <div className={style.form}>
    <div className={style.formTitle}>{title}</div>
    {subtitle
      ? <div className={style.formSubtitle}>{subtitle}</div>
      : null}
    {errorMessage
      ? <div className={style.errorMessage}>
          <span><Icon type="exclamation-circle-o"/></span>{errorMessage}
        </div>
      : null}
    {children}
  </div>
);

@connect(state => ({}))
class Login extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      errorMessage: '',
      usernameTouched: false,
      passwordTouched: false,
      successfulLogin: false,
    }
  }

  login(username, password) {
    this.props.dispatch(userActions.login(username, password)).then(() => {
      this.setState({
        successfulLogin: true,
        errorMessage: ''
      });
    }).catch((error) => {
      if (error.response && error.response.status == 403 && error.response.data) {
        if (error.response.data.message === "Wrong username or password") { // TODO убрать костыль
          this.setState({errorMessage: "Неправильное имя пользователя или пароль"});
        } else {
          this.setState({errorMessage: error.response.data.message});
        }
      } else {
        this.setState({errorMessage: "Похоже что-то пошло не так"});
      }
    });
  }

  validate = () => {
    this.props.form.validateFields((errors, value) => {
      if (!errors) {
        this.setState({errorMessage: ''});
        return;
      }
      if (this.state.usernameTouched && errors.username) {
        this.setState({errorMessage: this.props.form.getFieldError("username")})
        return;
      }
      if (this.state.passwordTouched && errors.password && errors.password.errors.length > 0) {
        this.setState({errorMessage: errors.password.errors[0].message})
      }
    })
  };

  handleUsernameChange = (e) => {
    this.props.form.setFieldsValue({username: e.target.value});
    this.setState({usernameTouched: true});
    this.validate();
  };

  handlePasswordChange = (e) => {
    this.props.form.setFieldsValue({password: e.target.value});
    this.setState({passwordTouched: true});
    this.validate();
  };

  handleSubmit = (e) => {
    this.props.form.validateFields((err, values) => {
      if (!err) {
        this.login(values.username, values.password);
      } else {
        this.setState({errorMessage: 'Не все обязательные поля заполнены'});
      }
    });
  };

  render() {
    const { getFieldDecorator } = this.props.form;
    return (
      <FormWrapper title="Вход" errorMessage={this.state.errorMessage}> 
        {this.state.successfulLogin ? <Redirect to="/"/> : null}
        {getFieldDecorator('username', {
          rules: [{ required: true, message: 'Введите логин' }],
        })(<Input
          size="large"
          placeholder="Логин"
          onChange={this.handleUsernameChange}
        />)}
        {getFieldDecorator('password', {
          rules: [{ required: true, message: 'Введите пароль' }],
        })(<Input
          size="large"
          placeholder="Пароль"
          type="password"
          onChange={this.handlePasswordChange}
        />)}
        <InputGroup className={style.inputGroup}>
          <Button 
            type="primary" 
            htmlType="submit" 
            onClick={this.handleSubmit} 
            className={style.mainButton}
          >Войти</Button>
          {getFieldDecorator('remember', {
            valuePropName: 'checked',
            initialValue: true,
          })(<Checkbox>Запомнить меня</Checkbox>)}
        </InputGroup>
        <Row>
          <Col span={"24"} className={style.inputGroup}>
            <Button className={style.VKButton}>Войти через ВКонтакте</Button>
            <Button className={style.GmailButton}>Войти через Gmail</Button>
          </Col>
        </Row>
      </FormWrapper>
    );
  }
}

Login = Form.create()(Login);

const RegisterAsStudent = () => (
  <FormWrapper
    title="Привет, ученик!"
    subtitle={"Ученик может решать задачи, принимать участие в курсах," 
              + " олимпиадах и сборах, видеть задачи недоступные для гостей"}
    errorMessage="Сообщение об ошибке если есть"
  >
    <Input size="large" placeholder="Логин"/>
    <InputGroup className={style.inputGroup}>
      <Col xs={14} md={16}>
        <Input
          size="large"
          placeholder="Пароль"
          type="password"
        />
      </Col>
      <Col xs={10} md={8}>
        <Button className={style.generateButton}>Сгенерировать</Button>
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

const RegisterAsTeacher = () => (
  <FormWrapper
    title="Привет, учитель!"
    subtitle={"Учитель может создавать сборы, олимпиады, курсы, группы и решать задачи."
              + " Чтобы получить доступ к ответам и скачиваниям задач, нужно подтверидть,"
              + " что Вы действительно учитель."}
  >
    <Input size="large" placeholder="Логин"/>
    <InputGroup className={style.inputGroup}>
      <Col xs={14} md={16}>
        <Input
          size="large"
          placeholder="Пароль"
          type="password"
        />
      </Col>
      <Col xs={10} md={8}>
        <Button className={style.generateButton}>Сгенерировать</Button>
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

const RegisterAsTeam = ({usersArrays}) => {
  console.log(usersArrays);
  const autoCompletes = usersArrays.map((users, i) => (
    <AutoComplete
      size="large"
      key={i + 1}
      dataSource={users.map(user => user.username + ' ' + user.firstname + ' ' + user.lastname)}
      placeholder={"Участник " + (i + 1)}
      className={style.autoComplete}
    >
    </AutoComplete>
  ));
  return (<FormWrapper title="Новая команда" errorMessage="Сообщение об ошибке если есть">
    <Input
      size="large"
      placeholder="Название команды"
    />
    <div>Состав команды</div>
    {autoCompletes}
    <Button type="primary">Зарегистрировать команду</Button>
  </FormWrapper>);
};

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


export default class LoginPage extends React.Component {
  render() {
    const { match } = this.props;

    const usersArrays = [
      [{key: 'johnn', username: 'johnn', firstname: 'John', lastname: 'Doe'},
        {key: 'doee', username: 'doee', firstname: 'Doe', lastname: 'John'},
        {key: 'dojo', username: 'dojo', firstname: 'Jo', lastname: 'Do'}],
      [], []
    ];

    const options = [
      {
        url: `${match.url}`,
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

    const menuItems = options.map(option => (
      <Menu.Item key={option.url}>
        <NavLink
          exact to={option.url}
          className={style.link}
          activeClassName={style.linkActive}
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
          <Col xs={22} md={20} style={{marginBottom: "16px"}}>
            <Row type="flex" className={style.wrapper}>
              <Col xs={{span: 22, offset: 1, order: 2}} md={{span: 8, offset: 1, order: 1}}>
                <div className={style.leftColumn}>
                  <Menu className={style.menu}>
                    {menuItems}
                  </Menu>
                  <Telegram/>
                </div>
              </Col>
              <Col xs={{span: 22, offset: 1, order: 1}} md={{span: 13, offset: 1, order: 2}}>
                {routes}
              </Col>
            </Row>
          </Col>
        </Row>
      </MainContentWrapper>
    )
  }
}