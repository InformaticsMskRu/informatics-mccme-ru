import React from 'react';
import {Col, colStyle, Row} from '../../components/utility/Grid';
import MainContentWrapper from '../../components/utility/MainContentWrapper';
import Box from '../../components/utility/Box';
import styled from 'styled-components';
import {List} from 'antd';
import {Panel} from '../../components/utility/Collapse';
import IsoCollapses from '../../isomorphic/components/uielements/collapse';
import IsoCollapseWrapper from '../../isomorphic/containers/Uielements/Collapse/collapse.style';
import {Link} from 'react-router-dom';

const TeamProfileWrapper = MainContentWrapper.extend``;

const Text = styled.div`
  font-family: Roboto, serif;
  font-weight: normal;
  font-style: normal;
  font-stretch: normal;
  line-height: normal;
  letter-spacing: normal;
  text-align: center;
`;

const Header = Text.extend`
  font-size: 24px;
  color: #343a40;
`;

const HeaderWithMargin = Header.extend`
  margin-top: 20px;
  margin-bottom: 30px;
`;
const TeamDescription = Text.extend`
  opacity: 0.5;
  font-size: 12px;
  color: #788195;
`;

const Divider = styled.div`
  width: 100%;
  height: 1px;
  opacity: 0.3;
  border-bottom: solid 1px #979797;
  margin: 30px 0;
`;

const Rating = Text.extend`
  font-size: 14px;
  color: #676b7a;
  margin-bottom: 30px;
`;

const RatingIcon = () => <i style={{color: '#ff9d61'}} className='material-icons'>stars</i>;

const Block = styled.div`
  height: 80px;
  width: 100%;
  line-height: 100%;
  border-radius: 4px;
  background-color: #407eff;
  display: inline-block;
`;

const Name = Text.extend`
  font-size: 14px;
  color: #ffffff;
  margin-top: calc((80px - 14px) / 2);
  float: left;
`;

const StubIcon = styled.div`
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: red;
  float: left;
  margin: 15px;
`;

const Date = Text.extend`
  opacity: 0.5;
  font-size: 12px;
  color: #343a40;
`;

const ContestItem = Text.extend`
  font-size: 14px;
  color: #788195;
`;

export default class TeamProfile extends React.Component {

  constructor() {
    super();
  }

  render() {
    const text = 'Text';
    return (
      <TeamProfileWrapper>
        <Row>
          <Col xs={24} style={colStyle}>
            <Box>
              <Header>Название команды</Header>
              <TeamDescription>Команда</TeamDescription>
              <Row justify={'center'} type={'flex'}>
                <Col span={22}>
                  <Divider/>
                </Col>
              </Row>
              <Rating><RatingIcon/>1532 в рейтинге, 34 задач решено</Rating>

              <Row justify={'center'} type={'flex'}>
                <Col span={16}>
                  <Row gutter={16}>
                    {[...Array(3)].map(() =>
                      <Col xs={{span: 24}} md={{span: 8}}>
                        <Block>
                          <StubIcon/>
                          <Name>Edward Bridges</Name>
                        </Block>
                      </Col>
                    )}
                  </Row>
                  <Row>
                    <HeaderWithMargin>Сборы</HeaderWithMargin>
                  </Row>
                  <Row>
                    <Col>
                      <IsoCollapseWrapper>
                        <IsoCollapses accordion>
                          <Panel header={'Название сборов'} key='1'>
                            <List
                              dataSource={['Название контеста', 'Название контеста', 'Название контеста']}
                              renderItem={item => (
                                <List.Item>
                                  <List.Item.Meta title={<Link to={'/'}><ContestItem>{item}</ContestItem></Link>}/>
                                  <Date>Дата и время</Date>
                                </List.Item>
                              )}>
                            </List>
                          </Panel>
                          <Panel header={'Название сборов'} key='2'>
                            <p>{text}</p>
                          </Panel>
                          <Panel header={'Название сборов'} key='3'>
                            <p>{text}</p>
                          </Panel>
                        </IsoCollapses>
                      </IsoCollapseWrapper>
                    </Col>
                  </Row>
                </Col>
              </Row>
            </Box>
          </Col>
        </Row>
      </TeamProfileWrapper>
    );
  }
}
