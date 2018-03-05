import React from 'react';
import styled from 'styled-components';
import { palette } from 'styled-theme';

import Box from '../../components/utility/Box';
import BackButton from '../../components/BackButton';
import MainContentWrapper from '../../components/utility/MainContentWrapper';


const ContentHeaderWrapper = styled.div`
  position: relative;
  text-align: center;
  margin: 10px 0 25px 0;
  padding-bottom: 25px;
  border-bottom: 1px solid ${palette('other', 9)};

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

  .statementTitle {
    color: ${palette('secondary', 0)};
    font-size: 22px;
  }

  @media (max-width: 1279px) {
    .backBtn { display: none; }
  }

  @media (max-width: 767px) {
    .header { margin-bottom: 35px; }
  }
`;

export default ({statementTitle, bootcampTitle, className}) => (
  <ContentHeaderWrapper className={className}>
    <BackButton className="backBtn"/>
    <div className="bootcampTitle">{bootcampTitle}</div>
    <div className="statementTitle">{statementTitle}</div>
  </ContentHeaderWrapper>
)
