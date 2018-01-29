import React from 'react';
import styled from 'styled-components';
import { palette } from 'styled-theme';

import { STATUSES } from '../../constants';
import Tooltip from '../../components/utility/Tooltip';
import { borderRadius } from '../../isomorphic/config/style-util';



const StatusWrapper = styled.div`
  display: flex;
  justify-content: center;
  color: white;
  cursor: default;
  
  > * {
    background: black;
    background: ${props => ({
      'orange': palette('other', 3),
      'green': palette('other', 4),
      'blue': palette('other', 5),
    })[props.color]};
  }
  
  .short:not(.animated) {
    margin: auto;
    width: 30px;
    height: 20px;
    ${borderRadius('10px')}
    text-align: center;
  }
`;

export default ({status, animated = false}) => (
  <StatusWrapper color={STATUSES[status].color}>
    <Tooltip placement="right" title={STATUSES[status].long}>
      <div
        className={`short ${animated ? 'animated' : ''}`}
      >
        {STATUSES[status].short}
      </div>
    </Tooltip>
  </StatusWrapper>
);
