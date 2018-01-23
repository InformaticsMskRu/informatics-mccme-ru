import React from 'react';
import * as _ from 'lodash';

import Box from '../../components/utility/Box';
import Button from '../../components/utility/Button';
import Collapse, { Panel } from '../../components/utility/Collapse';
import MainContentWrapper from '../../components/utility/MainContentWrapper';
import {
  gutter,
  colStyle,
  rowStyle,
  Col,
  Row,
} from '../../components/utility/Grid';

import CollapseHeader from './CollapseHeader';
import Search from './Search';


export default class MainPage extends React.Component {
  constructor() {
    super();

    this.uiState = localStorage.getItem('uiState');
    try {
      this.uiState = JSON.parse(this.uiState) || {};
    } catch (e) {
      this.uiState = {};
    }

    const panels = _.get(this.uiState, 'mainPage.panels');

    this.state = {
      panels,
    };

    this.toggleCollapse = this.toggleCollapse.bind(this);
  }

  toggleCollapse(panels) {
    _.set(this.uiState, 'mainPage.panels', panels);
    localStorage.setItem('uiState', JSON.stringify(this.uiState));
    this.setState({...this.state, panels});
  }

  render() {
    const { panels } = this.state;

    return (
      <MainContentWrapper>
        <Row>
          <Col xs={24} style={colStyle}>
            <Box style={{ paddingLeft: '0', paddingRight: '0' }}>
              <Collapse
                bordered={false}
                onChange={this.toggleCollapse}
                activeKey={panels}
              >
                <Panel
                  showArrow={false}
                  header={<CollapseHeader open={_.includes(panels, '1')} />}
                  key="1"
                >
                  <Row gutter={gutter} style={{...rowStyle, paddingTop: '20px'}}>
                    <Col md={12} xss={24} style={{colStyle}}>
                      <Row style={{...rowStyle, paddingLeft: '20px', paddingRight: '20px'}}>
                        <Col xs={24} style={colStyle}>
                          Подготовка к окружному этапу
                        </Col>
                        <Col xs={24} style={colStyle}>
                          Февральская школа. Байтик
                        </Col>
                        <Col xs={24} style={colStyle}>
                          Информатика, Лицей №2, г.о. Нальчик
                        </Col>
                        <Col xs={24} style={colStyle}>
                          БОП - боевое олимпиадное программирование
                        </Col>
                        <Col xs={24}>
                          <Button type="primary" size="small">Посмотреть все</Button>
                        </Col>
                      </Row>
                    </Col>
                    <Col md={12} xs={0} style={{colStyle}}>
                      <Row style={{...rowStyle, paddingLeft: '20px', paddingRight: '20px'}}>
                        <Col xs={24} style={colStyle}>
                          Название группы 1
                        </Col>
                        <Col xs={24} style={colStyle}>
                          Название группы 2
                        </Col>
                        <Col xs={24} style={colStyle}>
                          Название группы 3
                        </Col>
                        <Col xs={24} style={colStyle}>
                          Название группы 4
                        </Col>
                      </Row>
                    </Col>
                  </Row>
                </Panel>
              </Collapse>
            </Box>
          </Col>
        </Row>
        <Row gutter={gutter} justify="start" style={rowStyle}>
          <Col md={12} xs={24} style={colStyle}>
            <Box title="Найти" subtitle="Задачи, курсы, сборы">
              <Search />
            </Box>
          </Col>
          <Col md={12} xs={24} style={colStyle}>
            <Box title="Каталог" subtitle="Все сборы, курсы и уроки">
              <Button
                type="primary"
                style={{
                  marginRight: '12px',
                  marginBottom: '14px',
                }}
              >
                Дерево курсов и сборов
              </Button>
              <Button type="primary">
                Рубрикатор по темам
              </Button>
            </Box>
          </Col>
        </Row>
        <Row>
          <Col xs={24} style={colStyle}>
            <Box title="Изучение языка программирования">
              <Row><Col xs={24} style={colStyle}>
                <div>Ввод-вывод, оператор присваивания, арифметические операции</div>
              </Col></Row>
              <Row><Col xs={24} style={colStyle}>
                <div>Условный оператор</div>
              </Col></Row>
              <Row><Col xs={24} style={colStyle}>
                <div>Операторы цикла</div>
              </Col></Row>
              <Row><Col xs={24} style={colStyle}>
                <Button type="primary" size="small">Показать еще</Button>
              </Col></Row>
            </Box>
          </Col>
        </Row>
        <Row>
          <Col xs={24} style={colStyle}>
            <Box title="Изучение языка программирования">
              <Row><Col xs={24} style={colStyle}>
                <div>Ввод-вывод, оператор присваивания, арифметические операции</div>
              </Col></Row>
              <Row><Col xs={24} style={colStyle}>
                <div>Условный оператор</div>
              </Col></Row>
              <Row><Col xs={24} style={colStyle}>
                <div>Операторы цикла</div>
              </Col></Row>
              <Row><Col xs={24} style={colStyle}>
                <Button type="primary" size="small">Показать еще</Button>
              </Col></Row>
            </Box>
          </Col>
        </Row>
        <Row>
          <Col xs={24} style={colStyle}>
            <Box title="Изучение языка программирования">
              <Row><Col xs={24} style={colStyle}>
                <div>Ввод-вывод, оператор присваивания, арифметические операции</div>
              </Col></Row>
              <Row><Col xs={24} style={colStyle}>
                <div>Условный оператор</div>
              </Col></Row>
              <Row><Col xs={24} style={colStyle}>
                <div>Операторы цикла</div>
              </Col></Row>
              <Row><Col xs={24} style={colStyle}>
                <Button type="primary" size="small">Показать еще</Button>
              </Col></Row>
            </Box>
          </Col>
        </Row>
      </MainContentWrapper>
    );
  }
}
