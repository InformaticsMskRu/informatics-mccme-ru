import React from 'react';
import styled from 'styled-components';

import Popover from '../utility/Popover';


const BufferWrapper = styled.div`
  cursor: pointer;
  display: flex;
`;


export default class Buffer extends React.Component {
  render() {
    return (
      <div>
        <Popover
          trigger="click"
          content={<div>buffer</div>}
        >
          <BufferWrapper>
            <i className="material-icons">work</i>
          </BufferWrapper>
        </Popover></div>
    );
  }
}
