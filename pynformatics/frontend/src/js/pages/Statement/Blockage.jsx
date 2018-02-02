import { connect } from 'react-redux';
import { palette } from 'styled-theme'
import PropTypes from 'prop-types';
import React from 'react';

import BackButton from '../../components/BackButton';
import Box from '../../components/utility/Box';
import Button from '../../components/utility/Button';
import MainContentWrapper from '../../components/utility/MainContentWrapper';
import * as statementActions from '../../actions/statementActions';


const BlockageWrapper = MainContentWrapper.extend`
  .header {
    position: relative;
    text-align: center;
    margin: 10px 0 80px 0;
    padding-bottom: 25px;
    border-bottom: 1px solid ${palette('other', 9)};
  }
  
  .backBtn {
    position: absolute;
    z-index: 1;
    left: 0;
    top: 0;
    opacity: 0.5;
  }
  
  .bootcampTitle {
    color: ${palette('secondary', 2)};
    font-size: 12px;
    opacity: 0.5;
  }
  
  .contestTitle {
    color: ${palette('secondary', 0)};
    font-size: 22px;
  }
  
  
  .content {
    display: flex;
    flex-flow: row nowrap;
    justify-content: center;
    padding: 0 50px;
    margin-bottom: 100px;
  }
  
  .image {
    width: 167px;
    height: 191px;
    margin: 0 65px 0 0;
  }
  
  .text {
    color: ${palette('other', 7)};
    font-size: 14px;
  }
  .textHeader {
    color: ${palette('secondary', 0)};
    font-size: 22px;
    margin-bottom: 18px;
  }
  .textButtons {
    margin-top: 21px;
    
    > *:first-child { 
      margin: 0 23px 0 0;
    }
  }
  
  @media (max-width: 1023px) {
    .backBtn { display: none; }
  }
  
  @media (max-width: 767px) {
    .header { margin-bottom: 35px; }
    .content { flex-wrap: wrap; }
    .image { margin: 0 0 35px 0; }
  }
  
  @media (max-width: 575px) {
    .content { 
      padding: 0;
      margin-bottom: 60px; 
    }
    .textButtons {
      > *:first-child { 
        margin: 0 16px 16px 0; 
      }
    }
  }
`;

export class Blockage extends React.Component {
  static propTypes = {
    statement: PropTypes.object.isRequired,
    fetchStatement: PropTypes.func.isRequired,
  };

  constructor() {
    super();

    this.start = this.start.bind(this);
  }

  start() {
    const {
      id,
      olympiad,
      virtual_olympiad: virtualOlympiad,
    } = this.props.statement;

    this.props.dispatch(statementActions.start(id, virtualOlympiad)).then(() =>
      this.props.fetchStatement());
  }

  render() {
    const {
      name: statementTitle,
    } = this.props.statement;

    return (
      <BlockageWrapper>
        <Box style={{ height: 'auto' }}>
          <div className="header">
            <BackButton className="backBtn"/>
            <div className="bootcampTitle">Название сборов</div>
            <div className="contestTitle">{statementTitle}</div>
          </div>
          <div className="content">
            <img className="image" src="/images/contest_blockage.png"/>
            <div className="text">
              <div className="textHeader">
                Контест доступен только в режиме олимпиады
              </div>
              <div>
                В случае участия в ней, на время проведения олимпиады у вас не будет доступа
                к другим задачам на сайте. Прервать участие до оканчания олимпиады нельзя.
                <br /><br />
                Вы хотите принять участие в олимпиаде?
              </div>
              <div className="textButtons">
                <Button
                  type="primary"
                  onClick={this.start}
                >
                  Принять участие
                </Button>
                <Button type="secondary">Вернуться</Button>
              </div>
            </div>
          </div>
        </Box>
      </BlockageWrapper>
    );
  }
}

export default connect(null)(Blockage);
