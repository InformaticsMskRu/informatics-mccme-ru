import React from 'react';
import styled from 'styled-components'

import Button from '../utility/Button';

const TelegramWrapper = styled.div`
  white-space: normal;
  line-height: 1.5;
  font-size: 12px;
  color: rgb(131, 140, 159);
  
  .telegramText {
    margin-bottom: 15px;
  }
`;

const Telegram = () => (
    <TelegramWrapper>
      <div className="telegramText">
        По всем текущим вопросам, а также в случае, если у вас что-то не работает, пишите на форум или в группу telegram
      </div>
      <Button
        type="primary"
      >
        Телеграм
      </Button>
    </TelegramWrapper>
);

export default Telegram;
