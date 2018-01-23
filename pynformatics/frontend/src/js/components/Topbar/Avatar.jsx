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
          <img src="https://avatars0.githubusercontent.com/u/7108312?s=400&u=2539cc56457c0e10d6ff79d13c1e6d6cc654e284&v=4"/>
        </AvatarWrapper>
      </Popover>
    );
  }
}
