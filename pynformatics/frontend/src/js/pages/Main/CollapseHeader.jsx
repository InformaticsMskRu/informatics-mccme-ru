import React from 'react';
import styled from 'styled-components';

import {
  gutter,
  rowStyle,
  Col,
  Row,
} from '../../components/utility/Grid';
import Button from '../../components/utility/Button';


const CollapseHeaderWrapper = styled.div`
  h3 {
    font-size: 22px;
    padding: 0 20px;
    margin: 0;
  }
  
  .collapseButton {
    position: absolute;
    top: -3px;
    right: 20px;
    
    @media (max-width: 576px) {
      display: none;
    }
  }
`;

const CollapseHeader = ({ open }) => (
  <CollapseHeaderWrapper>
    <Row gutter={gutter} style={rowStyle}>
      <Col md={12} xs={24}>
        <h3>
          Мои активности
        </h3>
      </Col>
      <Col md={12} xs={0}>
        <h3>
          Мои группы
        </h3>
      </Col>
    </Row>
    <Button className="collapseButton" type="primary" size="small">
      { open ? 'Свернуть' : 'Развернуть' }
    </Button>
  </CollapseHeaderWrapper>
);

export default CollapseHeader;
