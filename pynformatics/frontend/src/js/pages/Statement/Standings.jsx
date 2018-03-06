import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import { palette } from 'styled-theme';
import * as _ from 'lodash';

import Box from '../../components/utility/Box';
import Button from '../../components/utility/Button';
import ContentHeader from './ContentHeader';
import GroupFilter from '../../components/GroupFilter/GroupFilter';
import MainContentWrapper from '../../components/utility/MainContentWrapper';
import Slider from '../../components/utility/Slider';
import StandingsTable from '../../components/StandingsTable/StandingsTable';
import moment from '../../utils/moment';
import { RadioButton, RadioGroup } from '../../components/utility/Radio';
import { Row, Col, rowStyle, colStyle, gutter } from '../../components/utility/Grid';

import { createGroupSelect } from '../../components/GroupSelect/GroupSelect';


const StandingsWrapper = MainContentWrapper.extend`
  max-width: 1280px;
  padding-top: 0;

  @media (max-width: 575px) { 
    padding-top: 0; 
  }

  .standingsRadioCol {
    overflow-x: auto;

    .ant-radio-group {
      display: flex;
      flex-flow: row nowrap;
      white-space: nowrap;
    }
  }

  .sliderBox {
    background: ${palette('other', 15)};
    padding: 0;
    margin-bottom: 16px !important;
  }

  .sliderBefore, .sliderAfter {
    font-size: 12px;
    color: ${palette('other', 7)};
    text-align: center;
  }
`;

export class Standings extends React.Component {
  static contextTypes = {
    statementId: PropTypes.number.isRequired,
  };

  static propTypes = {
    statements: PropTypes.object.isRequired,
    filterGroup: PropTypes.object,
  };

  constructor(props, context) {
    super(props, context);

    this.state = {
      dateFilterMode: 'end',
      date: undefined,
    };

    this.handleDateFilterModeChange = this.handleDateFilterModeChange.bind(this);
  }

  handleDateFilterModeChange(mode) {
    let date;
    switch (mode) {
      case 'start':
        date = this.startDate;
        break;
      case 'end':
        date = this.endDate;
        break;
      case 'custom':
        date = moment(this.startDate).add(this.slider || 0, 'minutes').toDate();
        break;
    }
    this.setState({...this.state, dateFilterMode: mode, date});
  }

  render() {
    const { statementId } = this.context;
    const { dateFilterMode, date } = this.state;
    const { filterGroup } = this.props;

    const statement = this.props.statements[statementId];
    const bootcampTitle = _.get(statement, 'course.full_name', null);

    const { olympiad, virtual_olympiad: virtualOlympiad } = statement;

    const { start, duration } = _.get(statement, 'participant', {});
    if (start && duration) {
      this.startDate = new Date(start * 1000);
      this.endDate = new Date((start + duration) * 1000);
      this.sliderStart = 0;
      this.sliderEnd = Math.floor(duration / 60);
      this.slider = this.sliderEnd;
    }

    return (
      <StandingsWrapper>
        <Box>
          <ContentHeader statementTitle="Результаты контеста" bootcampTitle={bootcampTitle}/>
          <Row style={rowStyle} gutter={gutter}>
            <Col xs={24} style={colStyle}>
              <GroupFilter/>
            </Col>
          </Row>
          {
            olympiad || virtualOlympiad
            ? (
              <Row style={rowStyle} gutter={gutter}>
                <Col className="standingsRadioCol" style={colStyle}>
                  <RadioGroup 
                    value={dateFilterMode} 
                    onChange={(event) => this.handleDateFilterModeChange(event.target.value)}
                  >
                    <RadioButton value="before" disabled>До старта</RadioButton>
                    <RadioButton value="start">Старт</RadioButton>
                    <RadioButton value="freeze" disabled>Заморозка</RadioButton>
                    <RadioButton value="end">Конец</RadioButton>
                    <RadioButton value="upsolving">Дорешивание</RadioButton>
                  </RadioGroup>
                </Col>
                <Col style={colStyle}>
                  <Button 
                    size="small" 
                    type={dateFilterMode === 'custom' ? 'primary' : 'secondary'}
                    onClick={() => this.handleDateFilterModeChange('custom')}
                    disabled={!this.sliderEnd}
                  >
                    Выбрать момент
                  </Button>
                </Col>
              </Row>
            ) : null
          }
          {
            (olympiad || virtualOlympiad) && dateFilterMode === 'custom'
            ? (
              <Box className="sliderBox">
                <Row 
                  type="flex" 
                  style={rowStyle} 
                  gutter={gutter} 
                  align="middle"
                  justify="space-around"
                >
                  <Col xs={0} sm={3} md={2} className="sliderBefore">
                    {moment(this.startDate).format('HH:mm')}
                  </Col>
                  <Col xs={22} sm={18} md={20}>
                    <Slider 
                      min={this.sliderStart}
                      max={this.sliderEnd}
                      defaultValue={this.sliderEnd}
                      tipFormatter={(shift) => moment(this.startDate).add(shift, 'minutes').format('HH:mm')}
                      onAfterChange={(shift) => {this.slider = shift; this.handleDateFilterModeChange('custom')}}
                    />
                  </Col>
                  <Col xs={0} sm={3} md={2} className="sliderAfter">
                    {moment(this.endDate).format('HH:mm')}
                  </Col>
                </Row>
              </Box>
            ) : null
          }
          <StandingsTable 
            maxDate={date} 
            filterGroupId={_.get(filterGroup, 'id')} 
          />
        </Box>
      </StandingsWrapper>
    );
  }
}

export default connect(state => ({
  statements: state.statements,
  filterGroup: state.group.filterGroup,
}))(Standings);
