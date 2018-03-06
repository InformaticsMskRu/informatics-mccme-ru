import { Icon, Popconfirm, Spin } from "antd";
import message from "antd/es/message/index";
import React from "react";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import { CopyToClipboard } from 'react-copy-to-clipboard'
import BackButton from "../../components/BackButton";
import Button from "../../components/utility/Button";
import List from "../../components/utility/List";
import MainContentWrapper from "../../components/utility/MainContentWrapper";
import StyleWrapper from './style';
import { fetchGroup, getGroupInvites, getGroupStudents, getGroupTeachers } from '../../actions/groupActions';

import { Row, Col } from '../../components/utility/Grid';

const GroupHeader = ({title}) => (
  <div className="group-header">
    <BackButton className="back-button"/>
    <div className="title-wrapper">
      <div className="title">{title}</div>
    </div>
  </div>
);

const RedirectLink = ({ redirect }) => {
  switch(redirect.type) {
    case("CONTEST"):
      return <Link to={`/contest/${redirect.id}`}>контест {redirect.id}</Link>;
    case("STATEMENT"):
      return <Link to={`/statement/${redirect.id}`}>турнир {redirect.id}</Link>;
    case("COURSE"):
      return <Link to={`/course/${redirect.id}`}>курс {redirect.id}</Link>;
    default:
      return <Link to={`/${redirect.type}/${redirect.id}`}>{redirect.type} {redirect.id}</Link>;
  }
};


@connect(state => ({
  rmatics_url: "rmatics.info",
  groups: state.group.groups,
  students: [
    {firstname: 'Stas', lastname: 'Tsepa'},
    {firstname: 'Stas', lastname: 'Tsepa'},
    {firstname: 'Stas', lastname: 'Tsepa'},
  ],
  teachers: [
    {firstname: 'Stas', lastname: 'Tsepa'},
    {firstname: 'Stas', lastname: 'Tsepa'},
    {firstname: 'Stas', lastname: 'Tsepa'},
  ],
  invites: [
    {link: 'abJSa', redirect: {type: 'CONTEST', id: 10}},
    {link: 'kaAml'},
  ]
}))
class GroupDetailPage extends React.Component {

  componentDidUpdate = () => {
    if (this.props.groups === undefined || this.props.groups[this.props.match.params.groupId] === undefined) {
      this.props.dispatch(fetchGroup(this.props.match.params.groupId));
    } else {
      if (this.props.groups[this.props.match.params.groupId].students === undefined) {
        this.props.dispatch(getGroupStudents(this.props.match.params.groupId));
      }
      if (this.props.groups[this.props.match.params.groupId].teachers === undefined) {
        this.props.dispatch(getGroupTeachers(this.props.match.params.groupId));
      }
      if (this.props.groups[this.props.match.params.groupId].invites === undefined) {
        this.props.dispatch(getGroupInvites(this.props.match.params.groupId));
      }
    }
  };

  render() {
    const { groups } = this.props;
    if (groups === undefined || groups[this.props.match.params.groupId] === undefined) {
      return <Spin size="large"/>;
    }
    const group = groups[this.props.match.params.groupId];
    const students = group.students !== undefined ? group.students : [];
    const teachers = group.teachers !== undefined ? group.teachers : [];
    const invites = group.invites !== undefined ? group.invites : [];

    const studentsItems = students.map((s, i) => (
      <List.Item
        key={i}
        actions={[
          <Popconfirm
            title="Уверены что хотите удалить ученика?"
            okText="Да"
            cancelText="Нет"
            okType="danger"
          >
            <Icon type="close" />
          </Popconfirm>
        ]}
      >
        <List.Item.Meta
          title={`${s.firstname} ${s.lastname}`}
        />
      </List.Item>
    ));
    const teachersItems = teachers.map((s, i) => (
      <List.Item
        key={i}
        actions={[
          <Popconfirm
            title="Уверены что хотите удалить учителя?"
            okText="Да"
            cancelText="Нет"
            okType="danger"
          >
            <Icon type="close" />
          </Popconfirm>
        ]}
      >
        <List.Item.Meta
          title={`${s.firstname} ${s.lastname}`}
        />
      </List.Item>
    ));
    const invitesItems = invites.map((s, i) => {
      return (
        <List.Item
          key={i}
          actions={[
            <CopyToClipboard
              text={`${this.props.rmatics_url}/invite/${s.link}`}
              onCopy={() => message.info("Ссылка скопирована в буфер обмена", 1)}
            >
              <Icon type="copy"/>
            </CopyToClipboard>,
            <Popconfirm
              title="Уверены что хотите удалить ссылку?"
              okText="Да"
              cancelText="Нет"
              okType="danger"
            >
              <Icon type="close" />
            </Popconfirm>
          ]}
          extra={
            s.redirect !== undefined && s.redirect !== null ?
              <div>Ссылка ведет на <RedirectLink redirect={s.redirect}/></div> :
              ''
          }
        >
          <List.Item.Meta
            title={`${this.props.rmatics_url}/invite/${s.link}`}
          />
        </List.Item>
      )
    });
    return (
      <MainContentWrapper>
        <StyleWrapper>
          <div className="root-wrapper">
            <GroupHeader title={`№${group.id}: ${group.name}`}/>
            <Row className="group-body">
              <Col md={8} sm={12} xs={24} className="group-body_column">
                <div className="header">Ученики</div>
                <List>{ studentsItems }</List>
              </Col>
              <Col md={8} sm={12} xs={24} className="group-body_column">
                <div className="header">Преподаватели</div>
                <List>{ teachersItems }</List>
              </Col>
              <Col md={8} sm={12} xs={24} className="group-body_column">
                <div className="header">Пригласить</div>
                <List>{ invitesItems }</List>
              </Col>
            </Row>
            <Row className="group-add">
              <Col md={8} sm={12} xs={24} className="group-add_column">
                <Button type="secondary" size="small">Добавить ученика</Button>
              </Col>
              <Col md={8} sm={12} xs={24} className="group-add_column">
                <Button type="secondary" size="small">Добавить преподавателя</Button>
              </Col>
              <Col md={8} sm={12} xs={24} className="group-add_column">
                <Button type="secondary" size="small">Добавить ссылку</Button>
              </Col>
            </Row>
          </div>
        </StyleWrapper>
      </MainContentWrapper>
    );
  }
}

export default GroupDetailPage;