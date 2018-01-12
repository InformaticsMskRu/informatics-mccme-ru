import React from 'react';
import styled from 'styled-components';

import Popover from '../utility/Popover';


const NotificationsWrapper = styled.div`
  cursor: pointer;
  display: flex;
`;


export default class Notification extends React.Component {
  render() {
    return (
      <div>
      <Popover
        trigger="click"
        content={<div>notifications</div>}
      >
        <NotificationsWrapper>
          <i className="material-icons">notifications_active</i>
        </NotificationsWrapper>
      </Popover></div>
    );
  }
}
