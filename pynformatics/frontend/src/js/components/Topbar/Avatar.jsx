import React from 'react';
import styled from 'styled-components';
import { Link } from 'react-router-dom';

import Popover from '../utility/Popover';
import DropdownWrapper from './DropdownWrapper';


const AvatarWrapper = styled.div`
  cursor: pointer;
  display: flex;
  
  img {
    width: 30px;
    height: 30px;
    border-radius: 15px;
  }
`;


export default class Avatar extends React.Component {
  render() {
    const content = (
      <DropdownWrapper className="isoUserDropdown">
        <Link to="/" className="isoDropdownLink">Профиль</Link>
        <Link to="/" className="isoDropdownLink">Выйти</Link>
      </DropdownWrapper>
    );

    return (
      <Popover
        trigger="click"
        content={content}
        placement="bottomLeft"
        arrowPointAtCenter={true}
      >
        <AvatarWrapper>
          <img src="invalid url"/>
        </AvatarWrapper>
      </Popover>
    );
  }
}
