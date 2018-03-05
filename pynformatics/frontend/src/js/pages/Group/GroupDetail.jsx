import React from "react";
import { palette } from "styled-theme";
import BackButton from "../../components/BackButton";
import Button from "../../components/utility/Button";
import List from "../../components/utility/List";
import MainContentWrapper from "../../components/utility/MainContentWrapper";
import StyleWrapper from './style';

import { Row, Col } from '../../components/utility/Grid';

const GroupHeader = ({title}) => (
  <div className="group-header">
    <BackButton className="back-button"/>
    <div className="title-wrapper">
      <div className="title">{title}</div>
    </div>
  </div>
);


class GroupDetailPage extends React.Component {
  render() {
    // const { students } = this.props;
    const students = [
      {firstname: 'Stas', lastname: 'Tsepa'},
      {firstname: 'Stas', lastname: 'Tsepa'},
      {firstname: 'Stas', lastname: 'Tsepa'},
    ];
    const studentsComponents = students.map((s, i) => (
      <List.Item key={i}>{i+1}, {s.firstname} {s.lastname}</List.Item>
    ));
    return (
      <MainContentWrapper>
        <StyleWrapper>
          <div className="root-wrapper">
            <GroupHeader title="Группа №1"/>
            <Row className="group-body">
              <Col md={8} xs={12} className="group-body_column">
                <div className="header">Ученики</div>
                <Button type="secondary" size="small">Добавить</Button>
                <List>
                  { studentsComponents }
                </List>
              </Col>
              <Col md={8} xs={12} className="group-body_column">
                <div className="header">Учителя</div>
                <Button type="secondary" size="small">Добавить</Button>
              </Col>
              <Col md={8} xs={12} className="group-body_column">
                <div className="header">Пригласить</div>
                <Button type="secondary" size="small">Добавить</Button>
              </Col>
            </Row>
          </div>
        </StyleWrapper>
      </MainContentWrapper>
    );
  }
}

export default GroupDetailPage;